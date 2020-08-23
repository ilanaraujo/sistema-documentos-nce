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

from werkzeug.security import generate_password_hash, check_password_hash

# Variável que representa a aplicação
app = Flask("__name__")

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
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return 'Sem token de acesso'

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return 'Token inválido'
        return f(*args, **kwargs)
    return decorated

# Página inicial
@app.route("/")
def incio():
    return render_template('inicio.html')

# Teste de token
@app.route('/tokenteste')
@token_required
def tokenTeste():
    return 'Token válido'

# Página de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuarioLogin = usuario.query.filter_by(email=email).first()

        # E-mail e senha corretos
        if email == usuarioLogin.email and check_password_hash(usuarioLogin.senha, senha):
            # Gera um token que expira após 45 segundos
            token = jwt.encode({'user' : email,
                                'exp' : datetime.utcnow() + timedelta(seconds = 45)
                               },
                               app.config['SECRET_KEY']
                              )
            return redirect(url_for('tokenTeste', token = token))

        # E-mail ou senha incorretos
        else:
            return 'Dados incorretos'
    else:
        return render_template('login.html')

# Página de criação de um novo documento
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

# Página para a alteração dos dados de um ofício existentente
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

# Página para a alteração dos dados de uma comunicação interna existente
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

# Págna para baixar um ofício existente
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

# Página para baixar uma comunicação interna existente
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

# Página para a alteração dos dados de um usuário aprovado pelo administrador
@app.route('/editarusuario/<int:id>', methods=['POST', 'GET'])
def editarUsuario(id):
    usuarioEditado = usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuarioEditado.nome = request.form['nome']
        usuarioEditado.nivelCargo = request.form['nivelCargo']
        usuarioEditado.cargo = request.form['cargo']
        usuarioEditado.area = request.form['area']
        usuarioEditado.divisao = request.form['divisao']
        try:
            db.session.commit()
            return redirect('/listausuarios')
        except:
            return 'Ocorreu um erro ao editar o usuário.'
    else:
        return render_template('editarUsuario.html', user = usuarioEditado)

# Inativa um usuário aprovado pelo administrador
@app.route('/inativarusuario/<int:id>')
def inativarUsuario(id):
    usuarioAtivo = usuario.query.get_or_404(id)
    usuarioAtivo.status = False
    try:
        db.session.commit()
        # Envia um e-mail pro usuário informando
        # que ele foi inativado
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
        # Envia um email pro usuário informando
        # que ele foi ativado
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
        db.session.delete(usuarioAprovado)
        db.session.commit()
        # Envia um e-mail pro usuário informando que ele foi aprovado
        # e que já pode usar o sistema de documentos.
    except:
        return "Ocorreu um erro ao aprovar o usuário."
    return redirect('/listausuariosnovos')
    

# Reprova o cadastro de um usuário novo, excluíndo-o da lista de usuários não aprovados
@app.route('/reprovarusuario/<int:id>')
def reprovarUsuario(id):
    usuarioReprovado = usuarioNovo.query.get_or_404(id)
    try:
        db.session.delete(usuarioReprovado)
        db.session.commit()

        # Adicionar página pra selecionar os campos preenchidos incorretamente

        # Envia um e-mail pro usuário informando que ele foi reprovado
        # e os campos que estão errados.
        return redirect('/listausuariosnovos')
    except:
        return "Ocorreu um erro ao reprovar o usuário"



# Função que inicia a aplicação
if __name__ == "__main__":

    # Com essas configurações o endereço para utilizar a aplicação no navegador
    # sempre será "localhost:5000" e o debug sempre estará ativado
    app.run(host="localhost", port=5000, debug=True)
