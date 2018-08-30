# Imports
from database import Database
from aux_pro import Process
from flask import Flask
from flask import render_template
from flask import url_for
from flask import redirect
from flask import jsonify
import datetime
import os

app = Flask(__name__)
db = Database()
pro = Process()

@app.route('/')
def index():
    pro.stop_process()
    return render_template('index.html', status='index')

@app.route('/monitor', methods = ["GET"])
def start_monitor():
    # Comienza a generar muestras si no lo estaba haciendo
    if not pro.is_running():
        pro.start_process()
    return render_template('monitor.html', status='monitor')

@app.route('/monitor/get_data', methods = ["GET"])
def monitor():
    # Recupera las ultimas diez muestras de la BD
    samples = db.get_last_samples()

    samples_number = len(samples)

    last = {}
    average = {}
    
    average['temperature'] = 0
    average['humidity'] = 0
    average['pressure'] = 0
    average['windspeed'] = 0

    # Promedio de las 10 (o menos, si no las hay) ultimas muestras tomadas
    for s in samples:
        average['temperature'] += s['temperature']
        average['humidity'] += s['humidity']
        average['pressure'] += s['pressure']
        average['windspeed'] += s['windspeed']

    # Ultima muestra tomada
    if samples_number > 0:
        last['temperature'] = samples[0]['temperature']
        last['humidity'] = samples[0]['humidity']
        last['pressure'] = samples[0]['pressure']
        last['windspeed'] = samples[0]['windspeed']
        average['temperature'] /= samples_number
        average['temperature'] = round(average['temperature'], 4)
        average['humidity'] /= samples_number
        average['humidity'] = round(average['humidity'], 4)
        average['pressure'] /= samples_number
        average['pressure'] = round(average['pressure'], 4)
        average['windspeed'] /= samples_number
        average['windspeed'] = round(average['windspeed'], 4)
    else:
        last['temperature'] = 0
        last['humidity'] = 0
        last['pressure'] = 0
        last['windspeed'] = 0

    # Normalizacion del formato de la respuesta de la funcion
    data = [{
        'temperature' : last['temperature'],
        'humidity' : last['humidity'],
        'pressure' : last['pressure'],
        'windspeed' : last['windspeed'] 
    },{
        'temperature' : average['temperature'],
        'humidity' : average['humidity'],
        'pressure' : average['pressure'],
        'windspeed' : average['windspeed']
    }]

    return jsonify(data)

@app.route('/monitor/stop', methods = ["GET"])
def stop_monitor():
    pro.stop_process()
    return index()

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8888)

