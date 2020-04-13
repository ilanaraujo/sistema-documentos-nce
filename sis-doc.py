# Imports da biblioteca padrão do Python
import json
import os
import sqlite3

# Imports das bibliotecas flask e flask_login
from flask import Flask, redirect, request, url_for, render_template
#from flask_login import (
#    LoginManager,
#    current_user,
#    login_required,
#    login_user,
#    logout_user,
#)
#from oauthlib.oauth2 import WebApplicationClient
#import requests

# Imports dos arquivos locais db.py e user.py
#from db import init_db_command
#from user import User

app = Flask("__name__")
#app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
#login_manager = LoginManager()
#login_manager.init_app(app)

# Naive database setup
#try:
#    init_db_command()
#except sqlite3.OperationalError:
#    # Assume it's already been created
#    pass

# OAuth 2 client setup
#client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
#@login_manager.user_loader
#def load_user(user_id):
#    return User.get(user_id)

# Configuração do sistema de login utilizando a API da Google
#GOOGLE_CLIENT_ID = os.environ.get("chave", None)
#GOOGLE_CLIENT_SECRET = os.environ.get("chave", None)
#GOOGLE_DISCOVERY_URL = ("url")

# Função para o login através do Google
#ef get_google_provider_cfg():
#    return requests.get(GOOGLE_DISCOVERY_URL).json()

# Tela inicial do sistema e tela de login
@app.route("/")
def incio():
    return render_template("login.html")

#@app
# 'Execução' do Login pelo Google
#@app.route("/logingoogle")
#def loginGoogle():
    # Find out what URL to hit for Google login
    #google_provider_cfg = get_google_provider_cfg()
    #authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
#    request_uri = client.prepare_request_uri(
#        authorization_endpoint,
#        redirect_uri=request.base_url + "/callback",
#        scope=["openid", "email", "profile"],
#    )
#    return redirect(request_uri)

# Callback do Login para dar get no código de autorização que o Google enviou
#@app.route("/login/callback")
#def callback():
    # Get authorization code Google sent back to you
#    code = request.args.get("code")

# Find out what URL to hit to get tokens that allow you to ask for
# things on behalf of a user
#google_provider_cfg = get_google_provider_cfg()
#token_endpoint = google_provider_cfg["token_endpoint"]

# Tela com o histórico com todos os documentos gerados que o usuário pode visualizar e editar
#@app.route('/historico')
#def historico():
#    return render_template('historico.html')

# Tela com a seleção do tipo de documento a ser gerado
#@app.route('/menu')
#def menu():
#    if current_user.is_authenticated:
#        return render_template('menu.html')
#    else:
#        return "Ocorreu um erro"

# Tela para a criação de um ofício
#@app.route('/documentos/oficio')
#def oficio():
#    return render_template('oficio.html')

# Tela para a criação de uma Comunicação Interna
#@app.route('/documentos/comunicacao_interna')
#def index():
#    return render_template('comunicacao_interna.html')

# Função que inicia o sistema
if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
