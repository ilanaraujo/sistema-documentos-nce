from flask import Flask, render_template

app = Flask("__name__")

#Tela de login do sistema
@app.route('/')
def login():
    return render_template('login.html')

#Página com todos os documentos (Disponível mesmo sem login)
@app.route('/documentos/')
def documentos():
    return render_template('documentos.html')

#Página para a criação do Ofício
@app.route('/oficio/')
def oficio():
    return render_template('oficio.html')

if __name__ == "__main__":
    app.run(debug=True)