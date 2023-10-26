import json
import csv
import time
import schedule
import logging
from datetime import datetime
from mongoProcess import MongoDBModel
from emailProcess import EmailView, ConsoleView

class Controller:
    
    log_filename = "log.txt"
    logging.basicConfig(filename=log_filename, level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    def __init__(self, mongodb_uri, database_name, collection_pedidos, collection_resultado, smtp_host, smtp_port, email, password):
        self.model = MongoDBModel(mongodb_uri, database_name, collection_pedidos, collection_resultado)
        self.email_view = EmailView(smtp_host, smtp_port, email, password)
        self.console_view = ConsoleView()

    def ejecutar_consulta_enviar_resultados(self,emailto, asuntoEmail, cuerpoEmail):

        # Lógica para obtener resultados del modelo
        datos = self.model.clientes_cumplenRegla()
        conexion = self.model.verificar_conexion_y_colecciones()
        if conexion.__contains__("Error"):
            self.email_view.enviar_correo(emailto, "Error","Novedad con base de datos")
            logging.error("Error","Novedad con base de datos")
        else:
            # Guardar resultados en MongoDB
            self.model.guardar_resultados(datos)

            # Mostrar resultados en la consola
            self.console_view.mostrar_mensaje(f"Clientes con 3 o más pedidos en estado 'returned' o 'cancelled' en un mismo mes:{len(datos)}")

            # Crear y escribir el archivo CSV
            csv_filename = 'clientes_con_tres_o_mas_pedidos.csv'
            with open(csv_filename, mode='w', newline='') as archivo_csv:
                writer = csv.writer(archivo_csv)
                writer.writerow(["Cliente"])
                for cliente in datos:
                    writer.writerow([cliente])
                        
            # Enviar correo electrónico con el archivo adjunto
            asunto = asuntoEmail
            cuerpo = cuerpoEmail
            adjunto = "clientes_con_tres_o_mas_pedidos.csv"
            destinatario = emailto
            self.email_view.enviar_correo_con_adjunto(destinatario, asunto, cuerpo, adjunto)

            # Cerrar la conexión a MongoDB
            self.model.cerrar_conexion()

def ejecutar_programa():
    try:
        with open('config.json', 'r') as archivo_config:
            configuracion = json.load(archivo_config)

        mongodb_uri = configuracion.get('mongodb_uri')
        database_name = configuracion.get('nameDatabase')
        collection_pedidos = configuracion.get('collectionPedidos')
        collection_resultado = configuracion.get('collectionResultado')
        smtp_host = configuracion.get('smtp_host')
        smtp_port = configuracion.get('smtp_port')
        email = configuracion.get('email')
        password = configuracion.get('password')
        emailto = configuracion.get('emailto')
        asuntoEmail = configuracion.get('asunto')
        cuerpoEmail = configuracion.get('cuerpo')

        controller = Controller(mongodb_uri, database_name, collection_pedidos, collection_resultado, smtp_host, smtp_port, email, password)
        controller.ejecutar_consulta_enviar_resultados(emailto,asuntoEmail,cuerpoEmail)
    except FileNotFoundError:
        logging.error("El archivo 'config.json' no se encontró.")
    except json.JSONDecodeError:
        logging.error("El archivo 'config.json' no es válido JSON.")
        

# Verificar si la ejecución programada está habilitada en el archivo de configuración
try:
    with open('config.json', 'r') as archivo_config:
        configuracion = json.load(archivo_config)
        ejecucionProgramada = configuracion.get('ejecucionProgramada')
        horaEjecucion = configuracion.get('horaEjecucion')
        intervaloEjecucion = configuracion.get('intervaloEjecucion')
        
    if ejecucionProgramada.lower() == "si":
        if intervaloEjecucion == "unico":
            # Programar la ejecución única a una hora específica
            schedule.every().day.at(horaEjecucion).do(ejecutar_programa)
        elif intervaloEjecucion.lower() == "diario":
            # Programar la ejecución diaria a una hora específica
            schedule.every().day.at(horaEjecucion).do(ejecutar_programa)
            while True:
                schedule.run_pending()
                time.sleep(1)
        elif intervaloEjecucion.isdigit():
            # Programar la ejecución cada N horas
            schedule.every(int(intervaloEjecucion)).hours.do(ejecutar_programa)
            while True:
                schedule.run_pending()
                time.sleep(1)
    else:
        # Ejecutar el programa una vez
        ejecutar_programa()
except Exception as e:
    logging.error("Ocurrió un error: %s", str(e))