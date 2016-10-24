from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from basedados import Sensor, Base
from sqlalchemy import *
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('.env')
conexao = config.get('base_dados', 'conexao')

engine = create_engine(conexao)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Efetua o cadastro dos sensores

registro = Sensor(id=1, nome='Fluxo', identificador='FS300A-G3/4')
session.add(registro)

registro = Sensor(id=2, nome='Temperatura', identificador='DHT11')
session.add(registro)

session.commit()
