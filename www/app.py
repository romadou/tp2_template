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
    
    return render_template('index.html', samples=samples)

@app.route('/monitor', methods = ["POST"])
def start_monitor():
    if pro.is_running():
        return index()
    session = db.get_session()
    pro.start_process()
    # return render_template('monitor.html', ''' parametros ''')
    mean = {
        'temperature' = 21,
        'humidity' = 9,
        'pressure' = 1012,
        'windspeed' = 9
    }
    last = {
        'temperature' = 21,
        'humidity' = 9,
        'pressure' = 1012,
        'windspeed' = 9
    }
    return render_template('monitor.html', mean=mean, last=last)

@app.route('/monitor', methods = ["GET"])
def monitor():
    # TODO: esta función debe ser llamada cada n segundos (petición desde "monitor.js")
    # TODO: probar verificando que la serialización funciona según lo esperado
    samples = db.get_last_samples()

    last['temperature'] = samples[0]['temperature']
    last['humidity'] = samples[0]['humidity']
    last['pressure'] = samples[0]['pressure']
    last['windspeed'] = samples[0]['windspeed']
    
    mean['temperature'] = 0
    mean['humidity'] = 0
    mean['pressure'] = 0
    mean['windspeed'] = 0
    
    samples_number = range(len(samples))
    
    for i in samples_number:
        mean['temperature'] += samples[i]['temperature']
        mean['humidity'] += samples[i]['humidity']
        mean['pressure'] += samples[i]['pressure']
        mean['windspeed'] += samples[i]['windspeed']
    
    mean['temperature'] /= samples_number
    mean['humidity'] /= samples_number
    mean['pressure'] /= samples_number
    mean['windspeed'] /= samples_number
    return render_template('monitor.html', last=last, mean=mean)

@app.route('/monitor/stop', methods = ["GET"])
def stop_monitor():
    data = pro.stop_process()
    return jsonify({"status": data})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)

