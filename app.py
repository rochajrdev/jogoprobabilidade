from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Exemplo de lógica de jogo simples (adapte conforme seu jogo)
@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        palpite = request.form.get('palpite')
        if palpite == '42':
            resultado = 'Parabéns! Você acertou.'
        else:
            resultado = 'Tente novamente.'
    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
