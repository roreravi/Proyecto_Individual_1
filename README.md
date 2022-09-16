# Proyecto_Individual_1
Implementación de FastAPI y SQL al dataset F1 World Championship (1950-2022)

# Requerimientos
La API esta desarrollada en Python y las librerias Pandas, Sqlite3, FastAPI, Uvicorn y Gunicorn. Tambien se usa la libreria Request para el consumo de los datos desde Heroku donse se hace el deploy.

# Implementacion
Para la implementación se instancia la clase FastAPI() 

app = FastAPI()

Luego se instancia una conexion a la base de datos para retornar su contenido a traves de la API

conn = sqlite3.connect("f2.db")

La base de datos se encuentra almacenada en el mismo directorio del script. Esto permite acceder a las tablas de la base de datos y disponibilizar los datos.

circuits = pd.read_sql('select * from circuits;', conn)
constructors = pd.read_sql('select * from constructors;', conn)
drivers = pd.read_sql('select * from drivers;', conn)
lap_times = pd.read_sql('select * from lap_times;', conn)
pit_stops = pd.read_sql('select * from pit_stops;', conn)
qualifying = pd.read_sql('select * from qualifying;', conn)
races = pd.read_sql('select * from races;', conn)
results = pd.read_sql('select * from results;', conn)

El contenido de las tablas se almacena en dataframes para ser retornado a través del método get de FastAPI pero previamente hay que pasarlos a formato Json con el método to_json de Pandas.

@app.get('/circuits')
def read_root():
    return circuits.to_json(orient="records")

Aqui estamos creando el enlace al json circuits el cual esta ordenado por registros gracias al argumento orient="records". Asi quedarian los enlaces local y remoto respectivamente:

http://127.0.0.1:8000/circuits
https://f1worldchampionship.herokuapp.com/circuits

mas adelante veremos como se levantan los links

En esta API además de los json derivados de la base de datos tambien se retornan 4 querys solicitadas en el proyecto

# 1. Año con mas carreras (Nota: en 2021 hay una carrera llamada TBC: significa "to be confirmed".. No cuenta)
year_max = pd.read_sql('select r.year as "Year", count(r.raceId) as "Races for Year" from races r group by "Year" order by "Races for Year" desc limit 2;', conn)
   
@app.get('/query_1')
def read_root():
    return year_max.to_json(orient="records")
    
Aqui vemos como a través de la libreria sqlite3 podemos recurrir a la sintaxis SQL para resolver la query la cual, luego, es almacenada en un dataframe. Al igual que el contenido de la base de datos, el contenido de la query se retorna en formato json.

Para levantar la API en un entorno local, desde la terminal y ubicados en el directorio donde almacenamos el scrip, ejecutamos:

$ uvicorn f1_db:app --reload

Donde f1_db es el nombre del script (f1_db.py) y app es el nombre de la variable donde esta instanciada la clase FastAPI(). La opción --reload permite que se recargue el enlace cada vez que hacemos algun cambio al script y guardamos.

Para hacer el deploy desde Heroku hacemos lo siguiente: 

1. Cargamos el script y la base de datos manteniendo la estructura de directorios. Pero ademas debemos subir un script sin extensión llamado Procfile con el siguiente contenido: 

web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker f1_db:app 

estamos invocando a las librerias gunicorn y uvicorn y especificando el nombre del scrip donde se define la API y el nombre de la variable donde esta instanciada. Ambas librerias deben estar instaladas en el entorno local o virtual donde se esté trabajando. Ademas del script Procfile debemos subir un archivo requirements.txt donde se especifican los requerimientos que se deben instalar en el servidor de Heroku para poder ejecutar el script y levantar la API. Éste archivo se crea ejecuntando:

$ pip freeze > requirements.txt

Una vez almacenados los archivos necesarios en el repositorio de GitHub procedemos a conectarnos a él desde Heroku:

Una vez creada la cuenta en Heroku seleccionamos la opción NEW APP y en el nombre escogemos aquel que queremos que aparezca en el link: En este caso para generar el link https://f1worldchampionship.herokuapp.com/circuits escogimos f1worldchampionship como nombre de la app y cliqueamos create app.

En la siguiente ventana debemos especificar que queremos conectarnos con un repositorio de github y cliqueamos el boton CONNECT TO GITHUB. Una vez realizada la conexión debemos especificar el nombre del repositorio y cliqueamos en SEARH para validar el nombre del repositorio. Luego seleccionamos la rama y al igual que la opción --reload de uvicorn en local Heroku tiene una opcion llamada ENABLE AUTOMATIC DEPLOYS que actualiza el link cada vez que hacemos algun cambio en el repositorio. Esta opción puede traer problemas con las limitaciones de las cuentas gratuitas por lo que recomendamos dejarla desactivada por lo menos hasta que tengamos cierta seguridad del fucionamiento de nuestra API.

Por último en este paso cliqueamos el boton DEPLOY BRANCH lo cual inicia la instalacion de los paquetes especificados en requirements.txt y ejecuta el script. Si no hay errores habilita el link de la API. Cliqueamos el boton VIEW y alli veremos la API funcionando o un mensaje de error.

En caso de haber errores conviene revisar los logs de Heroku a los cuales se puede acceder en el boton MORE que se encuentra en la parte superior derecha de la ventana donde configuramos nuestra app.

Una vez levantado nuestro link ya sea local o remoto podremos consumir los datos generados por API de la siguiente manera y con la ayuda de la libreria requests de Python:

# URL
url = 'http://f1worldchampionship.herokuapp.com/circuits'
# url = 'http://127.0.0.1:8000/circuits' en caso de tener la API en el entorno local

# Get content
r = requests.get(url)

# Decode JSON response into a Python dict:
content = r.json()
pd.read_json(content)

Esto nos va a permitir consumir los datos disponibles y realizar cualquier tipo de consulta sobre ellos bien sea con Pandas o SQL





