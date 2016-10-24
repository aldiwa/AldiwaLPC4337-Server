from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from basedados import VazaoAgua, FluxoAgua, Temperatura, Umidade, Log, Base
import datetime
import warnings
import json
from sqlalchemy.sql import func
from sqlalchemy.exc import SAWarning
warnings.filterwarnings('ignore',
 r"^Dialect sqlite\+pysqlite does \*not\* support Decimal objects natively\, "
 "and SQLAlchemy must convert from floating point - rounding errors and other "
 "issues may occur\. Please consider storing Decimal numbers as strings or "
 "integers on this platform for lossless storage\.$",
 SAWarning, r'^sqlalchemy\.sql\.type_api$')
from ConfigParser import SafeConfigParser

config = SafeConfigParser()
config.read('.env')
conexao = config.get('base_dados', 'conexao')

engine = create_engine(conexao)
Base.metadata.bind = engine 

app = Flask(__name__)

@app.route("/")
def main():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Temperatura
    dbTemperatura = session.query(Temperatura).order_by(Temperatura.id.desc()).first()
    if dbTemperatura is None:
        temperatura = 0
    else:
        temperatura = dbTemperatura.medicao

    # Umidade
    dbUmidade = session.query(Umidade).order_by(Umidade.id.desc()).first()
    if dbUmidade is None:
        umidade = 0
    else:
        umidade = dbUmidade.medicao    

    # Ultima Leitura de Vazao de Agua
    dbVazaoAgua = session.query(VazaoAgua).order_by(VazaoAgua.id.desc()).first()
    if dbVazaoAgua is None:
        vazaoagua = "Sem fluxo :("
    else:
        if dbVazaoAgua.medicao > 0:
            vazaoagua = "Fluxo de agua ativo ;)"
        else:
            vazaoagua = "Sem fluxo :("

    # Ultima Leitura de Fluxo de Agua
    dbFluxoAgua = session.query(FluxoAgua).order_by(FluxoAgua.id.desc()).first()
    if dbFluxoAgua is None:
        fluxoagua = 0
        dhFluxoagua = ""
    else:
        fluxoagua = dbFluxoAgua.medicao
        dhFluxoagua = dbFluxoAgua.datahora

    # Primeiro Fluxo de Agua
    dbFluxoInicio = session.query(FluxoAgua).order_by(FluxoAgua.id.asc()).first()
    if dbFluxoInicio is None:
        dhFluxoInicio = ""
    else:
        dhFluxoInicio = dbFluxoInicio.datahora

    # Ultimo Fluxo de Agua
    dbFluxoFim = session.query(FluxoAgua).order_by(FluxoAgua.id.desc()).first()
    if dbFluxoFim is None:
        dhFluxoFim = ""
    else:
        dhFluxoFim = dbFluxoFim.datahora
    
    # Acumulado do Fluxo de Agua
    dbPeriodoFluxoAgua = session.query(FluxoAgua).filter(FluxoAgua.datahora.between(dhFluxoInicio, dhFluxoFim)).order_by(FluxoAgua.datahora.asc())

    lstFluxo = []

    fluxoperiodo = 0

    for item in dbPeriodoFluxoAgua:
        if item.medicao != 0:
            fluxoperiodo += item.medicao

    return render_template('index.html',
        title='Aldiwa',
        temperatura=format(temperatura, '.2f'),
        umidade=format(umidade, '.2f'),
        fluxoagua=format(fluxoagua, '.7f'),
        vazaoagua=vazaoagua,
        datahora=dhFluxoagua,
        datahorainicio=dhFluxoInicio,
        datahorafim=dhFluxoFim,
        fluxoperiodo=fluxoperiodo
        )

@app.route('/log/sensor/<sensor>/mensagem/<mensagem>', methods=['POST'])
def api_logar(sensor, mensagem):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    registro = Log(sensor_id=sensor, mensagem=mensagem, datahora=datetime.datetime.now())
    session.add(registro)
    session.commit()
    return jsonify(retorno=1)

@app.route('/vazaoagua/sensor/<sensor>/medicao/<medicao>', methods=['POST'])
def api_vazaoagua(sensor, medicao):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    registro = VazaoAgua(sensor_id=sensor, medicao=medicao, datahora=datetime.datetime.now())
    session.add(registro)
    session.commit()
    return jsonify(retorno=1)

@app.route('/fluxoagua/sensor/<sensor>/medicao/<medicao>', methods=['POST'])
def api_fluxoagua(sensor, medicao):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    registro = FluxoAgua(sensor_id=sensor, medicao=medicao, datahora=datetime.datetime.now())
    session.add(registro)
    session.commit()
    return jsonify(retorno=1)

@app.route('/temperatura/sensor/<sensor>/medicao/<medicao>', methods=['POST'])
def api_temperatura(sensor, medicao):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    registro = Temperatura(sensor_id=sensor, medicao=medicao, datahora=datetime.datetime.now())
    session.add(registro)
    session.commit()
    return jsonify(retorno=1)

@app.route('/umidade/sensor/<sensor>/medicao/<medicao>', methods=['POST'])
def api_umidade(sensor, medicao):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    registro = Umidade(sensor_id=sensor, medicao=medicao, datahora=datetime.datetime.now())
    session.add(registro)
    session.commit()
    return jsonify(retorno=1)

@app.route('/aldiwa', methods=['GET'])
def api_aldiwa():
    return jsonify(aldiwa='servidor-aldiwa',
                   versao=config.get('servidor', 'versao'))

if __name__ == "__main__":
    #app.run(host=config.get('servidor', 'host'), port=config.get('servidor', 'porta'))
    from gevent.wsgi import WSGIServer
    http_server = WSGIServer(('', 4000), app)
    http_server.serve_forever()
