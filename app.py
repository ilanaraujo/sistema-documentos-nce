# Funções importadas da biblioteca padrão do Flask
from flask import Flask, request, render_template, redirect, url_for, session, make_response

# Utilizada para gerar o PDF
import pdfkit

#Utilizadas na criação do Token
import jwt
from functools import wraps

# Biblioteca utilizada na manipulação do banco de dados através do Flask
from flask_sqlalchemy import SQLAlchemy

# Biblioteca utilizada para receber a data direto do sistema
from datetime import datetime, timedelta

# Utilizada para salvar a senha no BD com uma hash
from werkzeug.security import generate_password_hash, check_password_hash

# Biblioteca utulizada para envio de emails
from flask_mail import Mail, Message

# Variável que representa a aplicação
app = Flask("__name__")

# Configuração do Flask-Mail
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'adm@gmail.com'
app.config['MAIL_PASSWORD'] = 'senha'
app.config['MAIL_DEFAULT_SENDER'] = 'adm@gmail.com'
app.config['MAIL_MAX_MAILS'] = None
app.config['MAIL_SUPRESS_SEND']  = False
app.config['MAIL_ASCII_ATTACHEMENTS'] = False

mail = Mail(app)

# Configuração do Banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistemaDocumentos.db'
db = SQLAlchemy(app)

# Chave secreta
app.config['SECRET_KEY'] = 'chave_ultra_hiper_mega_secreta'

# Usuários aprovados pelo administrador
class usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    senha = db.Column(db.String())
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
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    senha = db.Column(db.String())
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
    id = db.Column(db.Integer, primary_key=True)
    emissor = db.Column(db.String(100))
    autor = db.Column(db.String(100))
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
    id = db.Column(db.Integer, primary_key=True)
    emissor = db.Column(db.String(100))
    autor = db.Column(db.String(100))
    cargo = db.Column(db.String(50))
    area = db.Column(db.String(50))
    assunto = db.Column(db.String(100))
    destinatario = db.Column(db.String(100))
    data = db.Column(db.DateTime, default=datetime.utcnow)
    mensagem = db.Column(db.String(1000))

    # Retorna a id do oficio que acaba de ser gerado
    def __repr__(self):
        return '<comunicacaoInterna %r>' % self

# Decorador para páginas que exigem um Token
def token_normal(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        token = request.args.get('token')
        tipo = request.args.get('tipo')
        id = request.args.get('id')
        if not token:
            return 'Sem token de acesso'

        try:
            token_dec = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return 'Token inválido'
        usuario_logado = usuario.query.filter_by(email = token_dec['email']).first()
        if not usuario_logado.cargo:
            return 'Adm não permitido aqui'
        if tipo and id:
            return f(token, usuario_logado, tipo, id, *args, **kwargs)
        return f(token, usuario_logado, *args, **kwargs)
    return decorador

# Decorador para páginas do adm
def token_adm(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return 'Sem token de acesso'

        try:
            token_dec = jwt.decode(token, app.config['SECRET_KEY'])
            usuario_logado = usuario.query.filter_by(email = token_dec['email']).first()
        except:
            return 'Token inválido'

        if usuario_atual.cargo:
            return 'Acesso inválido'
        else:
            return f(token, usuario_atual, *args, **kwargs)
    return decorated


# Nota: alterar os [return 'algum erro'] pra flash messages nas próprias páginas

# Página inicial
@app.route("/")
def incio():
    return render_template('inicio.html')

# Página de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuarioLogin = usuario.query.filter_by(email=email).first()

        # E-mail e senha corretos
        if email == usuarioLogin.email and check_password_hash(usuarioLogin.senha, senha):
            # Gera um token que expira após 2 minutos
            token = jwt.encode({'email' : email,
                                'exp' : datetime.utcnow() + timedelta(minutes = 2)
                               },
                               app.config['SECRET_KEY']
                              )
            return redirect(url_for('perfil', token = token))

        # E-mail ou senha incorretos
        else:
            return 'Dados incorretos, volte para a página anterior.'
    else:
        return render_template('login.html')

# Página com informações do usuário logado
@app.route('/perfil')
@token_normal
def perfil(token, usuario_logado):
    return render_template('perfil.html', usuario = usuario_logado)

# Página para a alteração dos dados do usuário logado
@app.route('/editarusuario', methods=['POST', 'GET'])
@token_normal
def editarUsuario(token, usuario_logado):
    if request.method == 'POST':
        usuario_logado.nome = request.form['nome']
        usuario_logado.nivelCargo = request.form['nivelCargo']
        usuario_logado.cargo = request.form['cargo']
        usuario_logado.area = request.form['area']
        usuario_logado.divisao = request.form['divisao']
        try:
            db.session.commit()
            return redirect(url_for('listaUsuarios', token = token))
        except:
            return 'Ocorreu um erro ao editar o usuário.'
    else:
        return render_template('editarUsuario.html', user = usuario_editado)

# Página de criação de um novo documento
@app.route("/criardocumento", methods=['POST', 'GET'])
@token_normal
def criarDocumento(token, usuario_logado):
    # Quando um novo documento é gerado
    if request.method == 'POST':
        # Recebe as informações passadas pelo usuário no formulário
        tipo = request.form['tipo']
        area = usuario_logado.area
        emissor = request.form['emissor']
        autor = usuario_logado.nome
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
        if(tipo == 'comInterna'):
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
                return redirect(url_for('listaOficios', token = token))
            if(tipo == 'comInterna'):
                return redirect(url_for('listaComInternas', token = token))
        except:
            return 'Occorreu um erro ao salvar o documento. Retorne para a página anterior'

    # Quando a página é acessada
    else:
        return render_template('criarDocumento.html', token = token)

# Página com o histórico de documentos gerados
@app.route("/listaoficios", methods=['POST', 'GET'])
@token_normal
def listaOficios(token, usuario_logado):
    # Ofícios ordenados do mais novo para o mais antigo
    oficios = oficio.query.order_by(oficio.id.desc()).all()
    exp = jwt.decode(token, app.config['SECRET_KEY'])['exp']
    return render_template('listaDocumentos.html', token = token, documentos = oficios, tipo = "oficio")

@app.route("/listacomunicacoesinternas", methods=['POST', 'GET'])
@token_normal
def listaComInternas(token, usuario_logado):
    # Comunicações internas ordenadas da mais nova para a mais antiga 
    comInternas = comInterna.query.order_by(comInterna.id.desc()).all()
    return render_template('listaDocumentos.html', documentos = comInternas, tipo = "comInterna")

# Página para a alteração dos dados de um ofício existentente
@app.route('/editardocumento', methods=['GET', 'POST'])
@token_normal
def editarDocumento(token, usuario_logado, tipo, id):
    if(tipo == 'oficio'):
        doc = oficio.query.get_or_404(id)
    else:
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
            if tipo == 'oficio':
                return redirect(url_for('listaOficios', token = token))
            else:
                return redirect(url_for('listaComInternas', token = token))
        # Caso ocorra um erro com o BD
        except:
            return 'Occorreu um erro ao editar o documento. Volte para a página anterior'
    else:
        return render_template('editarDocumento.html', documento = doc)

# Págna para baixar um ofício existente
@app.route('/baixardocumento')
@token_normal
def baixarDocumento(token, usuario_logado, tipo, id):
    if tipo == "oficio":
        doc = oficio.query.get_or_404(id)
    if tipo == "comInterna":
        doc = comInterna.query.get_or_404(id)

    # Arquivo html que será convertido para PDF
    res = render_template('modeloDocumento.html',tipo = tipo, documento = doc)
    responsestring = pdfkit.from_string(res, False)
    response = make_response(responsestring)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline;filename = output.pdf'
    return response

# Página para a criação de um usuário novo
@app.route('/criarusuario', methods=['GET', 'POST'])
def criarUsuario():
     # Quando um novo usuário é gerado
    if request.method == 'POST':

        # Recebe as informações passadas pelo usuário no formulário
        usuarioCadastrado = usuarioNovo(
            email = request.form['email'],
            senha = generate_password_hash(request.form['senha']),
            nome = request.form['nome'],
            nivelCargo = request.form['nivelCargo'],
            cargo = request.form['cargo'],
            area = request.form['area'],
            divisao = request.form['divisao']
        )

        # Salva as informações do novo documento no 
        # BD e redireciona para o histórico
        try:
            db.session.add(usuarioCadastrado)
            db.session.commit()
            return redirect('/listausuariosnovos')
        # Caso ocorra um erro com o BD
        except:
            return 'Occorreu um erro ao registrar o usuário'
    # Quando a página é acessada
    else:
        return render_template('criarUsuario.html')

# Página com a lista de usuários aprovados pelo administrador
@app.route('/listausuarios', methods=['POST', 'GET'])
def listausuarios():
    usuarios = usuario.query.order_by(usuario.id).all()
    return render_template('listaUsuarios.html', usuarios = usuarios, novo=False)

# Inativa um usuário aprovado pelo administrador
@app.route('/inativarusuario/<int:id>')
def inativarUsuario(id):
    usuarioAtivo = usuario.query.get_or_404(id)
    usuarioAtivo.status = False
    try:
        db.session.commit()
        msg = Message(subject='Desativação  no sistema', recipients= [usuarioAtivo.email])
        msg.body = ('Olá sr/sra. %s, seu cadastro com o email: %s  foi desativado do sistema!\n Atenciosamente, coordenação NCE' %( usuarioAtivo.nome, usuarioAtivo.email ))
        mail.send(msg)

        return redirect('/listausuarios')
    except:
        return "Ocorreu um erro ao inativar o usuário"

# Reativa um usuário aprovado pelo administrador
@app.route('/ativarusuario/<int:id>')
def ativarUsuario(id):
    usuarioInativo = usuario.query.get_or_404(id)
    usuarioInativo.status = True
    try:
        db.session.commit()
        msg = Message(subject='Ativação no sistema', recipients= [usuarioInativo.email])
        msg.body = ('Olá sr/sra. %s, seu cadastro com o email: %s  foi ativado e está pronto para uso no sistema!\n Atenciosamente, coordenação NCE' %(usuarioInativo.nome,usuarioInativo.email))
        mail.send(msg)

        return redirect('/listausuarios')
    except:
        return "Ocorreu um erro ao ativar o usuario"

# Página com a lista de usuários ainda não aprovados pelo administrador
@app.route('/listausuariosnovos', methods=['GET', 'POST'])
def listaUsuariosNovos():
    usuarios = usuarioNovo.query.order_by(usuarioNovo.id).all()
    return render_template('listaUsuarios.html', usuarios = usuarios, novo=True)

# Aprova um usuário novo, excluíndo-o da lista de usuários não aprovados e adicionando-o
# à lista de usuários aprovados pelo administrador
@app.route('/aprovarusuario/<int:id>')
def aprovarUsuario(id):
    usuarioAprovado = usuarioNovo.query.get_or_404(id)
    usuarioAprovadoNovo = usuario(
        email = usuarioAprovado.email,
        senha = usuarioAprovado.senha,
        nome = usuarioAprovado.nome,
        cargo = usuarioAprovado.cargo,
        nivelCargo = usuarioAprovado.nivelCargo,
        area = usuarioAprovado.area,
        divisao = usuarioAprovado.divisao
    )
    try:
        db.session.add(usuarioAprovadoNovo)
        #msg = Message(subject='Ativação no sistema', recipients= [usuarioAprovadoNovo.email])
        #msg.body = ('Olá sr/sra. %s, seu cadastro com o email: %s  foi aprovado e ativo  pronto para uso no sistema!\nAtenciosamente, coordenação NCE' %(usuarioAprovadoNovo.nome, usuarioAprovadoNovo.email))
        #mail.send(msg)
        db.session.delete(usuarioAprovado)
        db.session.commit()
    except:
        return "Ocorreu um erro ao aprovar o usuário."
    return redirect('/listausuariosnovos')

# Reprova o cadastro de um usuário novo, excluíndo-o da lista de usuários não aprovados
@app.route('/reprovarusuario/<int:id>')
def reprovarUsuario(id):
    usuarioReprovado = usuarioNovo.query.get_or_404(id)
    try:
        db.session.delete(usuarioReprovado)
        msg = Message(subject='Ativação no sistema', recipients= [usuarioReprovado.email])
        msg.body = ('Olá sr/sra. %s, seu cadastro com o email: %s  foi reprovado no sistema!\nAtenciosamente, coordenação NCE' %(usuarioReprovado.nome, usuarioReprovado.email))
        mail.send(msg)
        db.session.commit()

        # Adicionar página pra selecionar os campos preenchidos incorretamente

        # Envia um e-mail pro usuário informando que ele foi reprovado
        # e os campos que estão errados.
        return redirect('/listausuariosnovos')
    except:
        return "Ocorreu um erro ao reprovar o usuário"

# Inicia a aplicação
if __name__ == "__main__":

    # Com essas configurações o endereço para utilizar a aplicação no navegador
    # sempre será "localhost:5000" e o debug mode sempre estará ativado
    app.run(host="localhost", port=5000, debug=True)
