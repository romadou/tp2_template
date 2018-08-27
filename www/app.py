# Imports
from database import Database
from process import Process
from flask import Flask
from flask import render_template

app = Flask(__name__)
db = Database()
pro = Process()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/monitor', methods = ["POST"])
def start_monitor():
    if pro.is_running():
        return index()
    pro.start_process()
    # return render_template('monitor.html', ''' parametros ''')
    average = {
        'temperature' = 0,
        'humidity' = 0,
        'pressure' = 0,
        'windspeed' = 0
    }
    last = {
        'temperature' = 0,
        'humidity' = 0,
        'pressure' = 0,
        'windspeed' = 0
    }
    return render_template('monitor.html', last=last, average=average)

@app.route('/monitor', methods = ["GET"])
def monitor():
    # TODO: esta función debe ser llamada cada n segundos (petición desde "monitor.js")
    # TODO: probar verificando que la serialización funciona según lo esperado
    samples = db.get_last_samples()

    last['temperature'] = samples[0]['temperature']
    last['humidity'] = samples[0]['humidity']
    last['pressure'] = samples[0]['pressure']
    last['windspeed'] = samples[0]['windspeed']
    
    average['temperature'] = 0
    average['humidity'] = 0
    average['pressure'] = 0
    average['windspeed'] = 0
    
    samples_number = range(len(samples))
    
    for i in samples_number:
        average['temperature'] += samples[i]['temperature']
        average['humidity'] += samples[i]['humidity']
        average['pressure'] += samples[i]['pressure']
        average['windspeed'] += samples[i]['windspeed']
    
    average['temperature'] /= samples_number
    average['humidity'] /= samples_number
    average['pressure'] /= samples_number
    average['windspeed'] /= samples_number

    # TODO: check if well handling the dictionary with the jsonify
    data = [last, average]
    return jsonify(data)
    # return render_template('monitor.html', last=last, average=average)

@app.route('/monitor/stop', methods = ["GET"])
def stop_monitor():
    data = pro.stop_process()
    return redirect('/')
    # TODO: ver qué onda este otro return
    # return jsonify({"status": data})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)

