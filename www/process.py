from database import Database
from models import Samples

import random
import time
import signal
import sys

class GracefulKiller:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


def main(db):
    killer = GracefulKiller()
    session = db.get_session()
    temperature = 22
    humidity = 10
    pressure = 1013
    windspeed = 8
    while True:
        db.set_sample(temperature, humidity, pressure, windspeed)

        temperature += random.randint(0,3) * random.choice([-1,0,1])
        if temperature < -10:
            temperature = -10
        elif temperature > 35:
            temperature = 35
        
        humidity += random.randint(0,10) * random.choice([-1,0,1])
        if humidity < 0:
            humidity = 0
        elif humidity > 100:
            humidity = 100
        
        pressure += random.randrange(0,100,7) * random.choice([-1,0,1])
        
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
    