import requests
import json
import pandas as pd
from datetime import datetime
from config import *
from conversion import *
from conexion_bd import *

BASE_URL_CURRENT = f'https://api.openweathermap.org/data/2.5/weather?'
BASE_URL_OPEN = f'https://api.openweathermap.org/data/3.0/onecall?'

if __name__ == '__main__':

    # se lee el archivo credencial.txt donde se encuentra la API key
    with open("credencial.txt", 'r') as f:
        api_key = f.read()

    city_list = ["London", "New York", "Cordoba", "Taipei", "Buenos Aires", "Mexico City", "Dublin", "Tbilisi", "Bogota", "Tokio"]
    #coord_list = ["lat=31&lon=64", "lat=40&lon=-73", "lat=-31&lon=-64", "lat=25&lon=64", "lat=-34&lon=-58", "lat=19&lon=-99", "lat=53&lon=6", "lat=41&lon=44", "lat=4&lon=74", "lat=35&lon=139"]

    # se excluye minutely (minutos) y hourly (horas) para que no se muestren en el json (solamente se extraerá la informacion teniendo en cuenta el dia)
    exclude = 'minutely,hourly'

    # se define el lenguaje en el que se mostrará la descripcion del clima
    lang = 'es'

    # se crea un diccionario vacio para almacenar los datos de la ciudad completa
    data_dict = {}


    # Se busca la ciudad por su nombre, se almacena su longitud, latitud, id y nombre en variables
    for city in city_list:

        # se crea una lista vacia para almacenar los datos de los 5 dias
        data_list = []

        url = f'{BASE_URL_CURRENT}q={city}&appid={api_key}'
        request = requests.get(url)
        
        if request.status_code == 200:
            
            data = request.json()
            
            #almaceno en variables temporales los datos de la ciudad
            id_ciudad = data['id']
            nombre_ciudad = data['name']
            lon_ciudad = data['coord']['lon']
            lat_ciudad = data['coord']['lat']
        
        else:
            raise Exception("Error en la conexion con la API CURRENT - Status Code: ", request.status_code)
        

        # se realiza el request al endpoint de one call de openwheater con los datos de longitud y latitud de la ciudad para obtener los 5 dias

        url2 = f'{BASE_URL_OPEN}lat={lat_ciudad}&lon={lon_ciudad}&exclude={exclude}&lang={lang}&appid={api_key}'
        request2 = requests.get(url2)

        if request2.status_code == 200:
            data2 = request2.json()
            
            for i in range(5):

                # se almacena en variables la fecha y la temperatura maxima y minima de cada dia
                fecha = data2['daily'][i]['dt']
                temp_max = kelvin_a_celsius(data2['daily'][i]['temp']['max'])
                temp_min = kelvin_a_celsius(data2['daily'][i]['temp']['min'])
                sensacion_termica_dia = kelvin_a_celsius(data2['daily'][i]['feels_like']['day'])
                sensacion_termica_noche = kelvin_a_celsius(data2['daily'][i]['feels_like']['night'])
                presion = data2['daily'][i]['pressure']
                porcentaje_humedad = data2['daily'][i]['humidity']
                descripcion_clima = data2['daily'][i]['weather'][0]['description']
                
                # se convierte la fecha de unix a formato datetime
                fecha = datetime.fromtimestamp(fecha)
                
                # se formatea la fecha para que obtenga el formato de: DD/MM/YYYY
                fecha = fecha.strftime('%d/%m/%Y')

                # se almacenan los datos en el diccionario teniendo como clave principal el nombre de la ciudad "London"
                data_list.append({
                            'id': id_ciudad,
                            'ciudad': nombre_ciudad,
                            'lat': lat_ciudad,
                            'lon': lon_ciudad,
                            'temp_max': temp_max,
                            'temp_min': temp_min,
                            'sensacion_termica_dia': sensacion_termica_dia,
                            'sensacion_termica_noche': sensacion_termica_noche,
                            'presion (hPa)': presion,
                            'porcentaje_humedad': porcentaje_humedad,
                            'descripcion_clima': descripcion_clima,
                            'fecha': fecha,
                            })

            # se almacena en el diccionario la lista de datos de cada ciudad    
            data_dict[city] = data_list
            
        else:
            raise Exception("Error en la conexion con la API OPEN CALL - Status Code: ", request2.status_code)
    
    # se crea un DataFrame a partir del diccionario reestructurado, donde cada fila es un día de una ciudad
    filas = []
    for ciudad, data_ciudad in data_dict.items():
        # se itera sobre los diccionarios que contienen los datos del dia de cada ciudad (id,nombre,lat,lon,etc)
        for data_ciudad in data_ciudad:
            filas.append(data_ciudad)

    df = pd.DataFrame(filas)
    df.set_index('id', inplace=True)

    # se crea la conexion a la base de datos
    engine = create_engine(DATABASE_URL.format(user=user, password=password, host=host, port=port, database=database))

    # se crea una sesion para poder realizar la creación de la tabla y posterior inserción de datos
    Session = sessionmaker(bind=engine)

    session = Session()

    # se crea la tabla definida en el archivo conexion_bd.py en la base de datos
    Base.metadata.create_all(engine)

    try:
        for index, row in df.iterrows():

            # se verifica si los registros se encuentran ya cargados en la base utilizando id_ciudad, nombre y fecha

            existentes = session.query(Clima).filter_by(id_ciudad=index, ciudad=row['ciudad'], fecha=row['fecha']).first()

            # si existen registros, se actualizan los datos
            if existentes:
                existentes.lat = row['lat']
                existentes.lon = row['lon']
                existentes.temp_max = row['temp_max']
                existentes.temp_min = row['temp_min']
                existentes.sensacion_termica_dia = row['sensacion_termica_dia']
                existentes.sensacion_termica_noche = row['sensacion_termica_noche']
                existentes.presion = row['presion (hPa)']
                existentes.porcentaje_humedad = row['porcentaje_humedad']
                existentes.descripcion_clima = row['descripcion_clima']

            else:

                clima_data = Clima(id_ciudad= index, ciudad=row['ciudad'], lat=row['lat'],
                                    lon=row['lon'], temp_max=row['temp_max'], temp_min=row['temp_min'],
                                    sensacion_termica_dia=row['sensacion_termica_dia'],
                                    sensacion_termica_noche=row['sensacion_termica_noche'], presion=row['presion (hPa)'],
                                    porcentaje_humedad=row['porcentaje_humedad'], descripcion_clima=row['descripcion_clima'], fecha=row['fecha'])
                session.add(clima_data)

            session.commit()
    except Exception as e:
        print(f'No se pudieron insertar los datos, el error es: {e}')
        session.rollback()
    finally:
        #Se cierra la sesión
        session.close()

