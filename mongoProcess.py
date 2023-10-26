import logging
from pymongo import MongoClient, errors
from datetime import datetime


class MongoDBModel:
    def __init__(self, mongodb_uri, database_name, collection_pedidos, collection_resultado):
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.collection_pedidos = self.db[collection_pedidos]
        self.collection_resultado = self.db[collection_resultado]
        self.verificar_conexion_y_colecciones()

    def verificar_conexion_y_colecciones(self):
        try:
            # Verificar la conexión
            server_info = self.client.server_info()
            if not server_info:
                logging.error("Error de conexión a MongoDB")
                return ("Error de conexión a MongoDB")

            # Verificar la existencia de las colecciones
            if not self.collection_pedidos.name in self.db.list_collection_names() or not self.collection_resultado.name in self.db.list_collection_names():
                logging.error(
                    "Error las colecciones no existen en la base de datos")
                return ("Error las colecciones no existen en la base de datos")
            return ("Conexión OK")
        except Exception as e:
            logging.error(
                f"Error durante la verificación de conexión y colecciones: {e}")
            return (f"Error durante la verificación de conexión y colecciones: {e}")

    def clientes_cumplenRegla(self):
        try:
            # Lógica para obtener los clientes con tres o más pedidos
            pipeline = [
                {
                    "$project": {
                        "shipping_date": 1,
                        "shipping_status": 1,
                        "order_vendor_dbname": 1
                    }
                },
                {
                    "$match": {
                        "$or": [
                            {"shipping_status": "returned"},
                            {"shipping_status": "cancelled"}
                        ]
                    }
                }
            ]

            results = self.collection_pedidos.aggregate(pipeline)
            pedidos_por_cliente_mes = {}

            for result in results:
                fecha_envio = result["shipping_date"]
                mes = fecha_envio.month
                anio = fecha_envio.year
                cliente = result.get("order_vendor_dbname")

                clave = f"{cliente}_{anio}_{mes}"

                if clave in pedidos_por_cliente_mes:
                    pedidos_por_cliente_mes[clave] += 1
                else:
                    pedidos_por_cliente_mes[clave] = 1

            clientes_con_tres_o_mas_pedidos = [clave for clave, count in pedidos_por_cliente_mes.items() if
                                               count >= 3]

            return clientes_con_tres_o_mas_pedidos
        except errors.OperationFailure as op_err:
            logging.error(f"Error en la operación de consulta: {op_err}")
            return (f"Error en la operación de consulta: {op_err}")

    def guardar_resultados(self, datos):
        try:
            # Lógica para guardar resultados en MongoDB
            fecha_consulta = datetime.now()
            datos_a_insertar = [{"cliente": cliente, "fecha_consulta": fecha_consulta}
                                for cliente in datos]

            self.collection_resultado.insert_many(datos_a_insertar)
        except errors.OperationFailure as op_err:
            logging.error(f"Error al guardar resultados en la base de datos: {op_err}")
            raise Exception(f"Error al guardar resultados en la base de datos: {op_err}")

    def cerrar_conexion(self):
        self.client.close()
