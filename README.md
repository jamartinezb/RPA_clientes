# 🛸📨🚀 RPA_clientes 🚀📨🛸

Este proyecto se centra en la identificación de clientes con tres o más pedidos que han sido devueltos o cancelados en el mismo mes. Se proporciona un archivo de configuración que permite ajustar los parámetros esenciales para su operación. La aplicación tiene la capacidad de realizar tanto ejecuciones programadas como ejecuciones manuales, en caso de ser necesario es posible realizar programación de tareas programadas del sistema para iniciar la ejecución por ejemplo en un servidor, para que el proceso sea desatendido.

Durante el proceso de consulta, los resultados se almacenan en una tabla de la base de datos, lo que proporciona un registro detallado de cada consulta realizada. Además, el resultado de la consulta se genera en un archivo CSV y se envía por correo electrónico a las personas interesadas en la información.

## Cómo usar

Instalar las dependencias:

pip install -r requirements.txt

Ejecutar el script:

python main.py

## Resultados

El script generará un archivo CSV con los clientes que cumplen con los criterios de la consulta. El archivo se llamará clientes_con_tres_o_mas_pedidos.csv y se guardará en la raíz del proyecto, este archivo es el resultado de la consulta de la información alojada en la base de datos


## Deploy 🔧

Para desplegar el proyecto después de instalar las dependencias, en el archivo config,json se encuentran los parámetros para conexión con base de datos, configuración del correo y configuración de la programación 

Parámetros de MongoDB
mongodb_uri: Esta es la URI de MongoDB utilizada para establecer la conexión a la base de datos. Por defecto, se ha configurado para apuntar a una instancia local de MongoDB en el puerto 27017, en caso de utilizar autenticación debe configurar la cadena de conexión en la uri, ejemplo:
mongodb://usuario:password@localhost:27017/?authMechanism=SCRAM-SHA-1

nameDatabase: Nombre de la base de datos utilizada para almacenar los datos. En este caso, se llama "Rocket".

collectionResultado: Nombre de la colección en la base de datos donde se guardarán los resultados de la consulta. En este proyecto, la colección se llama "ResultadosConsulta".

collectionPedidos: Nombre de la colección en la base de datos que contiene los datos de los pedidos. En este caso, la colección se llama "Pedidos".

Parámetros de Correo Electrónico
smtp_host: Host SMTP utilizado para enviar correos electrónicos. Se ha configurado para utilizar el servidor SMTP de Gmail.

smtp_port: Puerto SMTP utilizado para la conexión. En este caso, el puerto es 587.

email: Tu dirección de correo electrónico desde la cual se enviarán los correos electrónicos.

emailto: Dirección de correo electrónico del destinatario de los informes generados.

password: Es la contraseñas de aplicaciones en Gmail

#Las Contraseñas de Aplicaciones de Gmail permiten a las aplicaciones o servicios acceder a tu cuenta de Gmail sin necesidad de proporcionar tu contraseña principal. A continuación, se detallan los pasos para configurar una Contraseña de Aplicaciones:

  1. Inicia sesión en tu cuenta de Gmail: Abre un navegador web y accede a tu cuenta de Gmail con tu nombre de usuario y contraseña.

  2. Acceso a la Configuración de la Cuenta: Haz clic en tu avatar en la esquina superior derecha de la pantalla y selecciona "Cuenta de Google."

  3. Seguridad: En la barra lateral izquierda, selecciona "Seguridad."

  4. Acceso de aplicaciones menos seguras: Asegúrate de que la opción "Acceso de aplicaciones menos seguras" esté desactivada. Si está habilitada, desactívala. Esto mejora la seguridad de tu cuenta.

  5. Contraseñas de Aplicaciones: En la sección "Iniciar sesión en Google," selecciona "Contraseñas de aplicaciones." Esto te llevará a la página de Contraseñas de Aplicaciones.

  6. Selecciona la Aplicación: Escoge la aplicación o servicio para el que deseas generar una contraseña. Si la aplicación no aparece en la lista, selecciona "Otra (personalizada)."

  7. Selecciona el Dispositivo: Elige el dispositivo o servicio al que se conectará la aplicación.

  8. Genera la Contraseña: Haz clic en "Generar" para obtener una contraseña única. Esta será la contraseña que la aplicación utilizará para acceder a tu cuenta de Gmail.

  9. Guarda la Contraseña: Anota la contraseña generada o cópiala en un lugar seguro. Esta contraseña es necesaria para configurar la aplicación o servicio.

  10. Configura la Aplicación: En la aplicación o servicio que deseas conectar a tu cuenta de Gmail, utiliza la contraseña generada en lugar de tu contraseña principal. Asegúrate de seguir las instrucciones de configuración de la aplicación.

asunto: Asunto del correo electrónico que se enviará.

cuerpo: El cuerpo del correo electrónico.

Configuración de Ejecución Programada
ejecucionProgramada: Permite configurar si deseas que el programa se ejecute automáticamente a intervalos regulares. Puede ser "si" o "no". Si se configura como "si", el programa se ejecutará de acuerdo con el intervalo especificado.

horaEjecucion: La hora en la que deseas que se ejecute el programa. Asegúrate de proporcionar la hora en el formato "HH:MM".

intervaloEjecucion: El intervalo de tiempo para la ejecución programada. Puede ser "diario", "semanal".

## Instrucciones detalladas para el despliegue y la ejecución en el entorno elegido

El proyecto se puede desplegar en cualquier entorno que tenga Python 3.7 o superior instalado. Para desplegar el proyecto en un entorno local, se puede seguir los siguientes pasos:

Clonar el repositorio de GitHub:
git clone [https://github.com/bard-ai/consulta-clientes.git](https://github.com/jamartinezb/RPA_clientes.git)
Instalar las dependencias:
pip install -r requirements.txt
Ejecutar el script:
python main.py
El script generará y se enviara al correo un archivo CSV con los clientes que cumplen con los criterios de la consulta. El archivo se llamará clientes_con_tres_o_mas_pedidos.csv y se guardará en la raíz del proyecto, se creará un histórico en la base de datos con las consultas realizadas en cada ejecución, con la finalidad de tener un registro del proceso


## Mejoras futuras

Se pueden realizar las siguientes mejoras en el proyecto:

Agregar más opciones de personalización
Se podrían agregar más opciones de personalización al script, como la posibilidad de especificar el intervalo de fechas a consultar o el nombre de la colección de MongoDB.
Agregar una interfaz para hacerlo más amigable al usuario final.

Espero que este README sea de tu agrado. Si tienes alguna sugerencia, no dudes en hacérmela saber.


