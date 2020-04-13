# Funções importadas da biblioteca padrão do Flask
from flask import Flask, request, render_template, redirect, url_for, session

# Funções importadas da biblioteca Flask-Login
from flask_login import LoginManager, UserMixin, login_required, login_user

#from markupsafe import escape

app = Flask("__name__")

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Definindo a chave secreta para usar na sessão
app.secret_key = 'chave_privada'

# Página Inicial
@app.route("/")
def incio():
    return render_template("index.html")

# Página na qual o usuário irá informar os dados do documento a ser gerado
@app.route("/gerardocumento")
#@login_required
def docs():
   return render_template('docs.html')

# Página com o histórico de documentos gerados
@app.route("/meusdocumentos")
#@login_required
def myDocs():
    return render_template('myDocs.html')

# Função que inicia a aplicação
if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True, threaded=True)