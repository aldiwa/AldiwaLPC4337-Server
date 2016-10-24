# AldiwaLPC4337-Server
Servidor (API REST) do Aldiwa para o protótipo com a LPCXpresso4337

#Configuração do ambiente

Criei um arquivo com o nome .env, ajustando-o com as configurações do seu ambiente:

[base_dados]
conexao = mysql+pymysql://USUARIO:SENHA@SERVIDOR/BASE-DE-DADOS

[servidor]
host = 0.0.0.0
porta = 4000
versao = 0.1

#Executando o projeto

Execute o app.py, a API do Servidor.