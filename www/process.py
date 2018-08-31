from database import Database
from models import Samples

import random
import time
import signal
import sys

class GracefulKiller:
    kill_now = False
    def __init__(self):
        # Comportamiento ante una señal de terminacion
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    # Finalizacion del proceso
    def exit_gracefully(self, signum, frame):
        self.kill_now = True


def main(db):
    killer = GracefulKiller()
    session = db.get_session()

    # Valores iniciales por defecto para las variables atmosfericas
    temperature = 22
    humidity = 10
    pressure = 1013
    windspeed = 8
    while True:
        db.set_sample(temperature, humidity, pressure, windspeed)

        # "Muestreo" de temperatura (entre -10°C y 35°C)
        temperature += random.randint(0,3) * random.choice([-1,0,1])
        if temperature < -10:
            temperature = -10
        elif temperature > 35:
            temperature = 35
        
        # "Muestreo" de humedad (entre 0% y 100%)
        humidity += random.randint(0,10) * random.choice([-1,0,1])
        if humidity < 0:
            humidity = 0
        elif humidity > 100:
            humidity = 100
        
        # "Muestreo" de presion atmosférica
        pressure += random.randrange(0,100,7) * random.choice([-1,0,1])
        
        # "Muestreo" de velocidad del viento (entre 0 km/h y 300 km/h)
        windspeed += random.randint(0,5) * random.choice([-1,0,1])
        if windspeed < 0:
            windspeed = 0
        elif windspeed > 300:
            windspeed = 300
        
        time.sleep(1)
        if killer.kill_now:
           session.close()
           break

if __name__ == '__main__':
    if (len(sys.argv) != 1):
        sys.exit("Usage: python process.py")    
    db = Database()
    main(db)
    