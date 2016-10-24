import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('.env')
conexao = config.get('base_dados', 'conexao')

Base = declarative_base()

class Sensor(Base):
    __tablename__ = 'sensor'
    id = Column(Integer, primary_key=True)
    nome = Column(String(250), nullable=False)
    identificador = Column(String(250), nullable=False)
    terminal = Column(Integer, default=1)

class FluxoAgua(Base):
    __tablename__ = 'fluxoagua'
    id = Column(Integer, primary_key=True)
    medicao = Column(Numeric, default=0)
    datahora = Column(DateTime(timezone=True))
    sincronizado = Column(Integer, default=0)
    terminal = Column(Integer, default=1)
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    sensor = relationship(Sensor)

class VazaoAgua(Base):
    __tablename__ = 'vazaoagua'
    id = Column(Integer, primary_key=True)
    medicao = Column(Numeric, default=0)
    datahora = Column(DateTime(timezone=True))
    sincronizado = Column(Integer, default=0)
    terminal = Column(Integer, default=1)
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    sensor = relationship(Sensor)

class Temperatura(Base):
    __tablename__ = 'temperatura'
    id = Column(Integer, primary_key=True)
    medicao = Column(Numeric, default=0)
    datahora = Column(DateTime(timezone=True))
    sincronizado = Column(Integer, default=0)
    terminal = Column(Integer, default=1)
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    sensor = relationship(Sensor)

class Umidade(Base):
    __tablename__ = 'umidade'
    id = Column(Integer, primary_key=True)
    medicao = Column(Numeric, default=0)
    datahora = Column(DateTime(timezone=True))
    sincronizado = Column(Integer, default=0)
    terminal = Column(Integer, default=1)
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    sensor = relationship(Sensor)

class Log(Base):
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)
    mensagem = Column(String(1000), nullable=False)
    datahora = Column(DateTime(timezone=True))
    sincronizado = Column(Integer, default=0)
    terminal = Column(Integer, default=1)
    sensor_id = Column(Integer, ForeignKey('sensor.id'))
    sensor = relationship(Sensor)

engine = create_engine(conexao)

Base.metadata.create_all(engine)
