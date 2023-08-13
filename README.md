# Weather Data Analytics - Proximos 5 Días
Este proyecto se centra en la obtención y análisis de datos climáticos para una ubicación geográfica específica en los proximos 5 días. Se utiliza la API de clima para recopilar información meteorológica y luego se procesa y almacena en un base de datos PostgreSQL para su posterior análisis. Este proyecto es parte de un curso de análisis de datos y utiliza herramientas como Pandas, Requests y SQLAlchemy.

## Requisitos
Antes de ejecutar el código, asegúrate de tener instaladas las siguientes bibliotecas de Python:

* pandas
* requests
* sqlalchemy
* psycopg2

Además, necesitas obtener una clave de API de la fuente de datos meteorológicos. Puedes obtener una clave registrándote en la plataforma que proporciona los datos meteorológicos y luego colocarla en un archivo llamado credencial.py de la siguiente manera:
"tu_clave_de_api_aqui" (sin las comillas)

Por ultimo tambien debes crear un archivo config.py con los siguientes datos:

### Datos para la conexión a la base de datos
user = nombre de usuario de la base de datos

password = contraseña de la base de datos

host = host de la base de datos

port = puerto de la base de datos

database = nombre de la base de datos creada

## Configuración de la Ubicación
El código está configurado para obtener datos climáticos para un listado de ciudades definido, el mismo puede modificarse agregando o quitando ciudades.
Ademas, al variar las ciudades el codigo automaticamente va a tomar la nueva latitud y longitud en las variables lat y lon respectivamente,
para obtener datos para la ubicación de tu interés.

## Ejecución del Código
Para ejecutar el código, simplemente inicia el archivo Python "main.py". El script realizará lo siguiente:

Obtendrá la api_key almacenada en el archivo "credencial.txt".
Realizará llamadas a los endpoints de "Current Wheater" y "One CALL API" obteniendo los datos para cada ciudad que se encuentre en el listado de ciudades.
Normalizará los datos obtenidos y los almacenará en un DataFrame de Pandas.
Convertirá las marcas de tiempo a formato de fecha y hora.
Guardará los datos en una base de datos PostgreSQL utilizando SQLalchemy.

## Resultados
Después de la ejecución, obtendrás los datos de los proximos 5 dias a la fecha actual en tu base de datos. Puedes usar esta información para análisis posterior y visualización de datos.
