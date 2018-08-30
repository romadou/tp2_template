import datetime

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Samples(Base):
    __tablename__ = 'samples'
    id=Column(Integer, primary_key=True)
    temperature=Column('temperature', Integer)
    humidity=Column('humidity', Integer)
    pressure=Column('pressure', Integer)
    windspeed=Column('windspeed', Integer)

    def serialize(self):
        """Devuelve los datos del objeto en una forma interpretable facilmente"""
        return {
            'id'  : self.id,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'windspeed': self.windspeed
        }
