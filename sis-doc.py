from flask import Flask, render_template

app = Flask("__name__")

@app.route('/')
def login():
    return render_template('login.html')

#@app.route('/documentos/')
#def documentos():
#    return render_template('documentos.html')

#Ofício
#@app.route('/documentos/oficio/')
#def oficio():
#    return render_template('oficio.html')

#Carta Externa
#@app.route('/documentos/carta_externa/')
#def index():
#    return render_template('carta_externa.html')

#Memorando
#@app.route('/documentos/memorando/')
#def index():
#    return render_template('memorando.html')

#Comunicação Interna
#@app.route('/documentos/comunicacao_interna/')
#def index():
#    return render_template('comunicacao_interna.html')

if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
