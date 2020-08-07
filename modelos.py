from sisdoc import db

# Usuários aprovados pelo administrador
class usuario(db.Model):
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

