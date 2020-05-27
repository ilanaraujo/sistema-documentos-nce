# Funções importadas da biblioteca padrão do Flask
from flask import Flask, request, render_template, redirect, url_for, session, make_response

import pdfkit

# Biblioteca utilizada na manipulação do banco de dados através do Flask
from flask_sqlalchemy import SQLAlchemy

# Biblioteca utilizada para receber a data direto do sistema
from datetime import datetime

# Funções importadas da biblioteca Flask-Login
from flask_login import LoginManager, UserMixin, login_required, login_user
#from markupsafe import escape

from form import LoginForm

app = Flask("__name__")

# Banco de Dados com os documentos gerados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///documentos.db'

# Banco de Dados com os usuários criados
# OBS: A configuração é diferente pois são utilizados dois ou mais BDs
app.config['SQLALCHEMY_BINDS'] = {'usuarios' : 'sqlite:///usuarios.db'}

# Variável que armazena o Banco de Dados
db = SQLAlchemy(app)

# Obs: O VS Code aponta erros nessa classe, porém eles não impedem
# que a aplicação seja executada 
class documento(db.Model):

    # Atributos que recebem as informações do documento
    id = db.Column(db.Integer, primary_key=True)
    emissor = db.Column(db.String(255))
    cargo = db.Column(db.String(255))
    area = db.Column(db.String(255))
    assunto = db.Column(db.String(255))
    destinatario = db.Column(db.String(255))
    tipo = db.Column(db.String(255))
    data = db.Column(db.DateTime, default=datetime.utcnow)

    # Retorna a id do documento que acaba de ser gerado
    def __repr__(self):
        return '<docGerado %r>' % self.id

# Obs: O VS Code aponta erros nessa classe, porém eles não impedem
# que a aplicação seja executada 
class usuario(db.Model):
    __bind_key__ = 'usuarios'

    # Atributos que recebem as informações do usuário
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    senha = db.Column(db.String(255)) 
    nome = db.Column(db.String(255))
    cargo = db.Column(db.String(255))
    area = db.Column(db.String(255))
    divisao = db.Column(db.String(255))
    status = db.Column(db.Boolean, default=True)

    # Retorna a id do usuário criado
    def __repr__(self):
        return '<userCriado %r>' % self.id

login_manager = LoginManager()
login_manager.init_app(app)

@property
def is_authenticated(self):
    return True

@property
def is_active(self):
    return True

@property
def is_anonymous(self):
    return False

def get_id(self):
    return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Definindo a chave secreta para usar na sessão
app.secret_key = 'chave_privada'

# Página Inicial. Login ainda indisponível
@app.route("/")
def incio():
    return redirect('/login')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form['email']
        user = usuario.query.get_or_404(email)
        if user and user.senha == form.data.senha:
           #login_user(user)
           return 'Login realizado com sucesso'
        else: 
            return 'Ocorreu um erro.'
    return render_template('login.html', form=form)

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')

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

        # Caso ocorra um erro com o armazenamento do
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

# Página para alterações em um documento
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    docGerado = documento.query.get_or_404(id)
    if request.method == 'POST':
        docGerado.area = request.form['area']
        docGerado.emissor = request.form['emissor']
        docGerado.destinatario = request.form['destinatario']
        docGerado.cargo = request.form['cargo']
        docGerado.assunto = request.form['assunto']

        try:
            db.session.commit()
            return redirect('/meusdocumentos')

        # Caso ocorra um erro com o BD
        except:
            return 'Occorreu um erro ao editar o documento'
    else:
        return render_template('editar.html', documento = docGerado)

# Página com o PDF que será baixado
@app.route('/baixar/<int:id>')
def baixar(id):
    docGerado = documento.query.get_or_404(id)

    # Arquivo html que será convertido para PDF
    res = render_template('oficio.html', docGerado = docGerado)
    responsestring = pdfkit.from_string(res, False)
    response = make_response(responsestring)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'filename = output.pdf'
    return response

@app.route('/criarusuario', methods=['GET', 'POST'])
def criarusuario():
     # Quando um novo usuário é gerado
    if request.method == 'POST':

        # Recebe as informações passadas pelo usuário no formulário
        usuario_email = request.form['email']
        usuario_senha = request.form['senha']
        usuario_nome = request.form['nome']
        usuario_cargo = request.form['cargo']
        usuario_area = request.form['area']
        usuario_divisao = request.form['divisao']

        # Variável que armazena as informações do usuário gerado
        userCriado = usuario(
            email = usuario_email,
            senha = usuario_senha,
            nome = usuario_nome,
            cargo = usuario_cargo,
            area = usuario_area,
            divisao = usuario_divisao
        )

        # Salva as informações do novo documento no 
        # BD e redireciona para o histórico
        try:
            db.session.add(userCriado)
            db.session.commit()
            return redirect('/listausuarios')

        # Caso ocorra um erro com o BD
        except:
            return 'Occorreu um erro ao salvar o documento'

    # Quando a página é acessada
    else:
        return render_template('criarusuario.html')

@app.route("/listausuarios", methods=['POST', 'GET'])
def listausuarios():

    # Variável que armazena todos os documentos e os
    # disponibiliza na ordem que foram gerados 
    usuarios = usuario.query.order_by(usuario.id).all()

    return render_template('myUsuarios.html', usuarios = usuarios)

# Função que inicia a aplicação
if __name__ == "__main__":

    # Com essas configurações o endereço para utilizar a aplicação
    # no navegador sempre será "localhost:5000" 
    app.run(host="localhost", port=5000, debug=True)