from flask import Flask, render_template #Bibliotecas e funções utilizadas

app = Flask("__name__")

# Configuração do sistema de login utilizando a API da Google
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

# Função para o login através do Google
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

# Tela inicial do sistema e tela de login
@app.route('/')
def login():
    return render_template('login.html')

# 'Execução' do Login
@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["46482407604-ontsmr4qnthcnbo6h1m13vde1bo50o49.apps.googleusercontent.com"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=base_url + "/callback",
        scope=["openid", "email"],
    )
    return redirect(request_uri)

# Callback do Login para dar get no código de autorização que o Google enviou
@app.route("/login/callback")
def callback():
    code = request.args.get("code")

# Tela com o histórico com todos os documentos gerados que o usuário pode visualizar e editar
@app.route('/historico')
def historico():
    return render_template('historico.html')

# Tela com a seleção do tipo de documento a ser gerado
@app.route('/menu')
def menu():
    if current_user.is_authenticated:
        return render_template('menu.html')
    else:
        return "Ocorreu um erro"

# Tela para a criação de um ofício
@app.route('/documentos/oficio')
def oficio():
    return render_template('oficio.html')

# Tela para a criação de uma Comunicação Interna
@app.route('/documentos/comunicacao_interna')
def index():
    return render_template('comunicacao_interna.html')

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)