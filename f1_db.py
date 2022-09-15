from fastapi import FastAPI
import sqlite3
import pandas as pd
import json

#instanciamos
app = FastAPI()

#conectamos con la base de datos e instanciamos
conn = sqlite3.connect("f1.db")
# conn = sqlite3.connect("f2.db") : f2 es la base de datos actualizada hasta 2022 
# donde se confirma que la carrera TBC (To Be Confirmed)no se realizó lo cual altera 
# la query 4 y de hecho la presencia de una carrera llamada TBC indica que se trata
# de un calendario y no de un registro de carreras realizadas por lo que se concluye
# que la data incluso puede ser de 2020



#leemos las tablas con pandas
circuits = pd.read_sql('select * from circuits;', conn)
constructors = pd.read_sql('select * from constructors;', conn)
drivers = pd.read_sql('select * from drivers;', conn)
lap_times = pd.read_sql('select * from lap_times;', conn)
pit_stops = pd.read_sql('select * from pit_stops;', conn)
qualifying = pd.read_sql('select * from qualifying;', conn)
races = pd.read_sql('select * from races;', conn)
results = pd.read_sql('select * from results;', conn)

#creamos los enlaces a cada una de las tablas
@app.get('/circuits')
def read_root():
    return circuits.to_json(orient="records")

@app.get('/constructors')
def read_root():
    return constructors.to_json(orient="records")

@app.get('/drivers')
def read_root():
    return drivers.to_json(orient="records")

@app.get('/lap_times')
def read_root():
    return lap_times.to_json(orient="records")

@app.get('/pit_stops')
def read_root():
    return pit_stops.to_json(orient="records")

@app.get('/qualifying')
def read_root():
    return qualifying.to_json(orient="records")

@app.get('/races')
def read_root():
    return races.to_json(orient="records")

@app.get('/results')
def read_root():
    return results.to_json(orient="records")

# Y por ultimo creamos enlaces a las querys solicitadas

# 1. Año con mas carreras (Nota: en 2021 hay una carrera llamada TBC: significa "to be confirmed".. No cuenta)
year_max = pd.read_sql('select r.year as "Year", count(r.raceId) as "Races for Year" from races r group by "Year" order by "Races for Year" desc limit 1;', conn)
   
@app.get('/query_1')
def read_root():
    return year_max.to_json(orient="records")

# 2. Piloto con mayor cantidad de primeros puestos
pilot_top = pd.read_sql('select ("forename" || " " || "surname") as "Name", count(r.driverId) as "Races Won" from drivers d, results r where r.driverId = d.driverId and r.position = 1 group by "Name" order by "Races Won" desc limit 1;', conn)

@app.get('/query_2')
def read_root():
    return pilot_top.to_json(orient="records")

# 3. Nombre del circuito mas corrido
cir_max = pd.read_sql('select c.name as "Circuit Name", count(r.circuitid) as "Races Hosted" from circuits c, races r where r.circuitid = c.circuitid group by "Circuit Name" order by "Races Hosted" desc limit 1;', conn)

@app.get('/query_3')
def read_root():
    return cir_max.to_json(orient="records")

# 4. Piloto con mayor cantidad de puntos en total, cuyo constructor sea de nacionalidad sea American o British
pilot = pd.read_sql('select ("forename" || " " || "surname") as "Name", c.nationality as "Constructor Nationality", sum(r.points) as "Total Points" from drivers d, results r, constructors c  where r.driverId = d.driverId and r.constructorId = c.constructorId and (c.nationality = "British" or d.nationality = "American") group by "Name" order by "Total Points" desc limit 1;', conn)

@app.get('/query_4')
def read_root():
    return pilot.to_json(orient="records")
