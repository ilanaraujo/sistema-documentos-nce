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

#from form import LoginForm

app = Flask("__name__")

# Banco de Dados com os usuários aprovados pelo administrador
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'

# Banco de Dados com os usuários aprovados pelo administrador
# OBS: A configuração é diferente pois são utilizados dois ou mais BDs
app.config['SQLALCHEMY_BINDS'] = {'comInterna' : 'sqlite:///comInternas.db',
                                  'oficio' : 'sqlite:///oficios.db',
                                  'usuarioNovo' : 'sqlite:///usuariosNovos.db'}

# Variável que gerencia o Banco de Dados
db = SQLAlchemy(app)

# Usuários aprovados pelo administrador
class usuario(db.Model):
    # Atributos que recebem as informações do usuário
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    senha = db.Column(db.String(50))
    nome = db.Column(db.String(50))
    cargo = db.Column(db.String(30))
    nivelCargo = db.Column(db.Integer)
    area = db.Column(db.String(30))
    divisao = db.Column(db.String(30))
    status = db.Column(db.Boolean, default=True)

    # Retorna a id do usuário criado
    def __repr__(self):
        return '<usuario %r>' % self.id

# Usuários novos sem aprovação do administrador
class usuarioNovo(db.Model):
    __bind_key__ = 'usuarioNovo'

    # Atributos que recebem as informações do usuário
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    senha = db.Column(db.String(50))
    nome = db.Column(db.String(50))
    cargo = db.Column(db.String(30))
    nivelCargo = db.Column(db.Integer)
    area = db.Column(db.String(30))
    divisao = db.Column(db.String(30))
    aprovacao = db.Column(db.Boolean, default=False)

    # Retorna a id do usuário criado
    def __repr__(self):
        return '<usuarioNovo %r>' % self.id

# Ofício
class oficio(db.Model):
    __bind_key__ = 'oficio'

    # Atributos que recebem as informações do ofício
    id = db.Column(db.Integer, primary_key=True)
    emissor = db.Column(db.String(100))
    cargo = db.Column(db.String(50))
    area = db.Column(db.String(50))
    assunto = db.Column(db.String(100))
    destinatario = db.Column(db.String(100))
    data = db.Column(db.DateTime, default=datetime.utcnow)
    mensagem = db.Column(db.String(1000))

    # Retorna a id do oficio que acaba de ser gerado
    def __repr__(self):
        return '<oficio %r>' % self

# Comunicação Interna
class comInterna(db.Model):
    __bind_key__ = 'comInterna'

    # Atributos que recebem as informações da comunicação interna
    id = db.Column(db.Integer, primary_key=True)
    emissor = db.Column(db.String(100))
    cargo = db.Column(db.String(50))
    area = db.Column(db.String(50))
    assunto = db.Column(db.String(100))
    destinatario = db.Column(db.String(100))
    data = db.Column(db.DateTime, default=datetime.utcnow)
    mensagem = db.Column(db.String(1000))

    # Retorna a id do oficio que acaba de ser gerado
    def __repr__(self):
        return '<comunicacaoInterna %r>' % self

#login_manager = LoginManager()
#login_manager.init_app(app)

#@property
#def is_authenticated(self):
#    return True

#@property
#def is_active(self):
#    return True

#@property
#def is_anonymous(self):
#    return False

#def get_id(self):
#    return str(self.id)

#@login_manager.user_loader
#def load_user(user_id):
#    return User.get(user_id)

# Definindo a chave secreta para usar na sessão
app.secret_key = 'chave_privada'

# Página Inicial. Login ainda indisponível
@app.route("/")
def incio():
    return render_template('inicio.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
#    if request.method == 'POST':
#        form = LoginForm()
#        if form.validate_on_submit():
#            email = request.form['email']
#            user = usuario.query.get_or_404(email)
#            if user and user.senha == form.data.senha:
#                #login_user(user)
#                return 'Login realizado com sucesso'
#            else:
#                return 'Ocorreu um erro.'
#    else:
#        return render_template('login.html', form=form)

# Logout
#@app.route("/logout")
#@login_required
#def logout():
#    logout_user()
#    return redirect('/login')

# Página na qual o usuário irá informar os dados do documento a ser gerado
@app.route("/criardocumento", methods=['POST', 'GET'])
def criarDocumento():
    # Quando um novo documento é gerado
    if request.method == 'POST':
        # Recebe as informações passadas pelo usuário no formulário
        tipo = request.form['tipo']
        area = request.form['area']
        emissor = request.form['emissor']
        destinatario = request.form['destinatario']
        cargo = request.form['cargo']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']

        # Criando um novo ofício
        if(tipo == "oficio"):
            doc = oficio(
                area = area,
                emissor = emissor,
                destinatario = destinatario,
                cargo = cargo,
                assunto = assunto,
                mensagem = mensagem
            )

        # Criando uma nova comunicação interna
        else:
            doc = comInterna(
                area = area,
                emissor = emissor,
                destinatario = destinatario,
                cargo = cargo,
                assunto = assunto,
                mensagem = mensagem
            )

        # Salva as informações do novo documento no 
        # BD e redireciona para o histórico
        try:
            db.session.add(doc)
            db.session.commit()
            if(tipo == "oficio"):
                return redirect('/listaoficios')
            else:
                return redirect('/listacomunicacoesinternas')

        # Caso ocorra um erro com o armazenamento do
        except:
            return 'Occorreu um erro ao salvar o documento'

    # Quando a página é acessada
    else:
        return render_template('criarDocumento.html')

# Página com o histórico de documentos gerados
@app.route("/listaoficios", methods=['POST', 'GET'])
def listaOficios():
    # Ofícios ordenados do mais novo para o mais antigo
    oficios = oficio.query.order_by(oficio.id.desc()).all()
    return render_template('listaDocumentos.html', documentos = oficios, tipo = "oficio")

@app.route("/listacomunicacoesinternas", methods=['POST', 'GET'])
def listaComInternas():
    # Comunicações internas ordenadas da mais nova para a mais antiga 
    comInternas = comInterna.query.order_by(comInterna.id.desc()).all()
    return render_template('listaDocumentos.html', documentos = comInternas, tipo = "comInterna")

# Página para alterações em um documento
@app.route('/editaroficio/<int:id>', methods=['GET', 'POST'])
def editarOficio(id):
    doc = oficio.query.get_or_404(id)
    if request.method == 'POST':
        doc.area = request.form['area']
        doc.emissor = request.form['emissor']
        doc.destinatario = request.form['destinatario']
        doc.cargo = request.form['cargo']
        doc.assunto = request.form['assunto']
        doc.mensagem = request.form['mensagem']
        try:
            db.session.commit()
            return redirect('/listaoficios')

        # Caso ocorra um erro com o BD
        except:
            return 'Occorreu um erro ao editar o documento'
    else:
        return render_template('editarDocumento.html', documento = doc)

@app.route('/editarcomunicacaointerna/<int:id>', methods=['GET', 'POST'])
def editarComInterna(id):
    doc = comInterna.query.get_or_404(id)
    if request.method == 'POST':
        doc.area = request.form['area']
        doc.emissor = request.form['emissor']
        doc.destinatario = request.form['destinatario']
        doc.cargo = request.form['cargo']
        doc.assunto = request.form['assunto']
        doc.mensagem = request.form['mensagem']
        try:
            db.session.commit()
            return redirect('/listacomunicacoesinternas')
        # Caso ocorra um erro com o BD
        except:
            return 'Occorreu um erro ao editar o documento'
    else:
        return render_template('editarDocumento.html', documento = doc)

# Baixar um ofício
@app.route('/baixaroficio/<int:id>')
def baixarOficio(id):
    doc = oficio.query.get_or_404(id)
    tipo = "Oficio"

    # Arquivo html que será convertido para PDF
    res = render_template('modeloDocumento.html',tipo = tipo, documento = doc)
    responsestring = pdfkit.from_string(res, False)
    response = make_response(responsestring)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline;filename = output.pdf'
    return response

# Baixar uma comunicação interna
@app.route('/baixarcomunicacaointerna/<int:id>')
def baixarComInterna(id):
    doc = comInterna.query.get_or_404(id)
    tipo = "Comunicação interna"

    # Arquivo html que será convertido para PDF
    res = render_template('modeloDocumento.html', documento = doc)
    responsestring = pdfkit.from_string(res, False)
    response = make_response(responsestring)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline;filename = output.pdf'
    return response

@app.route('/criarusuario', methods=['GET', 'POST'])
def criarUsuario():
     # Quando um novo usuário é gerado
    if request.method == 'POST':

        # Recebe as informações passadas pelo usuário no formulário
        usuario_email = request.form['email']
        usuario_senha = request.form['senha']
        usuario_nome = request.form['nome']
        usuario_nivelCargo = request.form['nivelCargo']
        usuario_cargo = request.form['cargo']
        usuario_area = request.form['area']
        usuario_divisao = request.form['divisao']

        # Variável que armazena as informações do usuário gerado
        usuarioCadastrado = usuarioNovo(
            email = usuario_email,
            senha = usuario_senha,
            nome = usuario_nome,
            nivelCargo = usuario_nivelCargo,
            cargo = usuario_cargo,
            area = usuario_area,
            divisao = usuario_divisao
        )

        # Salva as informações do novo documento no 
        # BD e redireciona para o histórico
        try:
            db.session.add(usuarioCadastrado)
            db.session.commit()
            return redirect('/listausuarios')

        # Caso ocorra um erro com o BD
        except:
            return 'Occorreu um erro ao salvar o documento'

    # Quando a página é acessada
    else:
        return render_template('criarUsuario.html')

@app.route('/listausuarios', methods=['POST', 'GET'])
def listausuarios(): 
    usuarios = usuario.query.order_by(usuario.id).all()
    return render_template('listaUsuarios.html', usuarios = usuarios, novo=False)

@app.route('/listausuariosnovos', methods=['GET', 'POST'])
def listaUsuariosNovos():
    usuarios = usuarioNovo.query.order_by(usuarioNovo.id).all()
    return render_template('listaUsuarios.html', usuarios = usuarios, novo=True)

# Função que inicia a aplicação
if __name__ == "__main__":

    # Com essas configurações o endereço para utilizar a aplicação
    # no navegador sempre será "localhost:5000" 
    app.run(host="localhost", port=5000, debug=True)
