# Funções importadas da biblioteca padrão do Flask
from flask import Flask, request, render_template, redirect, url_for, session, request

# Biblioteca utilizada na manipulação do banco de dados através do Flask
from flask_sqlalchemy import SQLAlchemy

# Biblioteca utilizada para receber a data direto do sistema
from datetime import datetime

# Funções importadas da biblioteca Flask-Login
#from flask_login import LoginManager, UserMixin, login_required, login_user

#from markupsafe import escape

app = Flask("__name__")

# Configuração do banco de dados através do SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///documentos.db' #test.db = nome do bd
db = SQLAlchemy(app)

# Obs: O VS Code aponta erros nessa classe, porém eles não impedem
# que a aplicação seja executada   
class documento(db.Model):

    # Atributos que recebem as informações do documento
    id=db.Column(db.Integer, primary_key=True)
    emissor=db.Column(db.String(255))
    cargo=db.Column(db.String(255))
    area=db.Column(db.String(255))
    assunto=db.Column(db.String(255))
    destinatario=db.Column(db.String(255))
    tipo=db.Column(db.String(255))
    data=db.Column(db.DateTime, default=datetime.utcnow)

    # Retorna a id do documento que acaba de ser gerado
    def __repr__(self):
        return '<docGerado %r>' % self.id

#login_manager = LoginManager()
#login_manager.init_app(app)

#@login_manager.user_loader
#def load_user(user_id):
#    return User.get(user_id)

# Definindo a chave secreta para usar na sessão
#app.secret_key = 'chave_privada'

# Página Inicial. Login ainda indisponível
@app.route("/")
def incio():
    return render_template("index.html")

# Página na qual o usuário irá informar os dados do documento a ser gerado
@app.route("/gerardocumento", methods=['POST', 'GET'])
def docs():
    # Quando um novo documento é gerado
    if request.method == 'POST':

        # Recebe as informações passadas pelo usuário no formulário
        documento_area = request.form['area']
        documento_tipo = request.form['tipo']
        documento_emissor = request.form['emissor']
        documento_destinatario = request.form['destinatario']
        documento_cargo = request.form['cargo']
        documento_assunto = request.form['assunto']

        # Variável que armazena as informações do documento gerado
        docGerado = documento(
            area = documento_area,
            tipo = documento_tipo,
            emissor = documento_emissor,
            destinatario = documento_destinatario,
            cargo = documento_cargo,
            assunto = documento_assunto
        )

        # Salva as informações do novo documento no 
        # BD e redireciona para o histórico
        try:
            db.session.add(docGerado)
            db.session.commit()
            return redirect('/meusdocumentos')

        # Caso ocorra um erro com o BD
        except:
            return 'Occorreu um erro ao salvar o documento'

    # Quando a página é acessada
    else:
        return render_template('docs.html')

# Página com o histórico de documentos gerados
@app.route("/meusdocumentos", methods=['POST', 'GET'])
def myDocs():

    # Variável que armazena todos os documentos e os
    # disponibiliza na ordem que foram gerados 
    documentos = documento.query.order_by(documento.id).all()

    return render_template('myDocs.html', documentos = documentos)

# Função que inicia a aplicação
if __name__ == "__main__":

    # Com essas configurações o endereço para utilizar a aplicação
    # no navegador sempre será "localhost:5000" 
    app.run(host="localhost", port=5000, debug=True)
