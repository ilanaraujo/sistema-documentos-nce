#Funções importadas da biblioteca Flask-Mail
from fask_mail import Mail, Message
#Variável que gerencia a biblioteca Flask-Mail
mail = mail(app)
#Configuração do Flask-Mail
app.config['DEBUG']= True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.google.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'emailelatorio@gmail.com' #email do adm
app.config['MAIL_PASSWORD'] = 'senha123' #senha do adm
app.config['MAIL_DEFAULT_SENDER'] = None
app.config['MAIL_MAX_EMAILS'] = None 
app.config['MAIL_ASCII_ATTACHEMENTS'] = False
#função de envio de email para usuário ativo
def mail_ativo(id)
        msg = Message('Ativação no sistema', recipients= [usuarioInativo.email])
        msg.body = 'Olá sr/sra. %s, seu cadastro com o email:%s  foi ativado e está pronto para uso no sistema!\n Atenciosamente, coordenação NCE'%(usuarioInativo.nome,usuarioInativo.email)
        mail.send(msg)
#função de envio de email para usuário inativo
def mail_inativo(id):
        msg = Message('Desativação  no sistema', recipients= [usuarioAtivo.email])
        msg.body = 'Olá sr/sra. %s, seu cadastro com o email: %s  foi desativado do sistema!\n Atenciosamente, coordenação NCE'%(usuarioAtivo.nome,usuarioAtivo.email)
        mail.send(msg)
#função de envio de email para usuário aprovado
def mail_aprovado(id):
        msg = Message('Aprovação do cadastro', recipients= [usuarioNovo.email])
        msg.body = 'Olá sr/sra. %s, seu cadastro com o email:%s  foi aprovado e está pronto para uso no sistema!\n Atenciosamente, coordenação NCE'%(usuarioNovo.nome,usuarioNovo.email)'
        mail.send(msg)
#função de envio de email para usuário reprovado
def mail_reprovado(id):)'
        msg = mail('Cadastro reprovado.', recipients=[usuarioNovo.email])
        msg.body = ('Seu cadastro foi reprovado pelos seguintes erros:\n %s' %{{form.cadastroReprovado}})
        mail.send(msg)
