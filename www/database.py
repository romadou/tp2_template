from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

from models import Samples

class Database(object):
    session = None
    db_user = os.getenv("DB_USER") if os.getenv("DB_USER") != None else "example"
    db_pass = os.getenv("DB_PASS") if os.getenv("DB_PASS") != None else "example"
    db_host = os.getenv("DB_HOST") if os.getenv("DB_HOST") != None else "db"
    db_name = os.getenv("DB_NAME") if os.getenv("DB_NAME") != None else "tp2"
    db_port = os.getenv("DB_PORT") if os.getenv("DB_PORT") != None else "3306"
    Base = declarative_base()
    
    def get_session(self):
        """Singleton de la conexion a la DB

        Returns:
            [db connection] -- [Singleton de la conexion a la DB]
        """
        if self.session == None:
            connection = 'mysql+mysqlconnector://%s:%s@%s:%s/%s' % (self.db_user,self.db_pass,self.db_host,self.db_port,self.db_name)
            engine = create_engine(connection,echo=True)
            connection = engine.connect()
            Session = sessionmaker(bind=engine)
            self.session = Session()
            self.Base.metadata.create_all(engine)
        return self.session
    
    def set_sample(self, temperature, humidity, pressure, windspeed):
        """Persiste una muestra a la DB
    
        Returns:
            [state] -- [True si la muestra fue guardada correctamente]
        """
        session = self.get_session()
        sample = Samples(temperature=temperature, humidity=humidity, pressure=pressure, windspeed=windspeed)
        session.add(sample)
        session.commit()
        session.close()
        return True

    def get_last_samples(self):
        """Devuelve la ultima muestra
        
        Returns:
            [array] -- [arreglo con las ultimas 10 muestras tomadas: id, temperatura, humedad, presion atmosferica y velocidad del viento]
        """
        session = self.get_session()
        samples = session.query(Samples).order_by(Samples.id.desc()).limit(10).all()
        session.close()
        return [s.serialize() for s in samples]
