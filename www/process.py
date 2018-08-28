from database import Database
from models import Samples

import random
import time
import signal
import sys

class GracefulKiller:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


def main(db):
    killer = GracefulKiller()
    temperature = 22
    humidity = 10
    pressure = 1013
    windspeed = 8
    db.set_sample(temperature, humidity, pressure, windspeed)
    while(1):
        temperature += random.randint(0,3) * random.choice([-1,0,1])
        humidity += random.randint(0,10) * random.choice([-1,0,1])
        pressure += random.randrange(0,100,7) * random.choice([-1,0,1])
        windspeed += random.randint(0,5) * random.choice([-1,0,1])
        db.set_sample(temperature, humidity, pressure, windspeed)
        print("Nuevos valores obtenidos \n temperatura: %s ° | humedad: %s % | presion atmosferica: %s hPa | velocidad del viento: %s km/h" % (temperature, humidity, pressure, windspeed))
        time.sleep(1)
        if killer.kill_now:
            session.close()
            break

if __name__ == '__main__':
    if (len(sys.argv) != 1):
        sys.exit("Usage: python process.py")    
    db = Database()
    main(db)
    