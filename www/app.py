# Imports
from database import Database
from aux_pro import Process
from flask import Flask
from flask import render_template, url_for, redirect

app = Flask(__name__)
db = Database()
pro = Process()

@app.route('/')
def index():
    pro.stop_process()
    return render_template('index.html', status='index')

@app.route('/monitor', methods = ["GET"])
def start_monitor():
    if pro.is_running():
        return index()
    pro.start_process()
    return render_template('monitor.html', status='monitor')

@app.route('/monitor/get_data', methods = ["GET"])
def monitor():
    samples = db.get_last_samples()

    # Última muestra tomada
    last['temperature'] = samples[0]['temperature']
    last['humidity'] = samples[0]['humidity']
    last['pressure'] = samples[0]['pressure']
    last['windspeed'] = samples[0]['windspeed']
    
    average['temperature'] = 0
    average['humidity'] = 0
    average['pressure'] = 0
    average['windspeed'] = 0
    
    samples_number = range(len(samples))
    
    # Promedio de las 10 (o menos, si no las hay) últimas muestras tomadas
    for i in samples_number:
        average['temperature'] += samples[i]['temperature']
        average['humidity'] += samples[i]['humidity']
        average['pressure'] += samples[i]['pressure']
        average['windspeed'] += samples[i]['windspeed']
    
    average['temperature'] /= samples_number
    average['humidity'] /= samples_number
    average['pressure'] /= samples_number
    average['windspeed'] /= samples_number

    # TODO: check if well handling the dictionary with the jsonify; if not, do it like on tp2_exercise
    data = [last, average]
    return jsonify(data)

@app.route('/monitor/stop', methods = ["GET"])
def stop_monitor():
    pro.stop_process()
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)

