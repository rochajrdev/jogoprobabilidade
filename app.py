from flask import Flask, render_template, request, jsonify, session
import random
import math

app = Flask(__name__)
app.secret_key = 'chave_secreta_do_jogo'

# Definição das cores e pontuações
PONTOS_COR = {
    'blue': 5,
    'red': 3,
    'green': 2
}

# Tabuleiro 6x6 com as cores
CORES = [
    ['red', 'blue', 'blue', 'blue', 'blue', 'red'],
    ['green', 'red', 'green', 'green', 'red', 'green'],
    ['green', 'green', 'red', 'red', 'green', 'green'],
    ['green', 'green', 'red', 'red', 'green', 'green'],
    ['green', 'red', 'green', 'green', 'red', 'green'],
    ['red', 'blue', 'blue', 'blue', 'blue', 'red']
]

# Base de perguntas
def gerar_pergunta(linha, coluna):
    cor = CORES[linha][coluna]
    total_casas = 36
    total_cor = sum(row.count(cor) for row in CORES)
    
    questoes = [
        {
            'pergunta': f'Qual é a probabilidade de cair em uma casa {cor}?',
            'resposta': f'{total_cor}/{total_casas}',
            'opcoes': [
                f'{total_cor}/{total_casas}',
                f'{total_cor-1}/{total_casas}',
                f'{total_cor+1}/{total_casas}',
                f'{total_casas}/{total_cor}'
            ]
        },
        {
            'pergunta': f'Quantas casas {cor} existem no tabuleiro?',
            'resposta': str(total_cor),
            'opcoes': [str(x) for x in [total_cor-1, total_cor, total_cor+1, total_cor+2]]
        },
        {
            'pergunta': f'Qual é a porcentagem aproximada de casas {cor} no tabuleiro?',
            'resposta': f'{round((total_cor/total_casas)*100)}%',
            'opcoes': [
                f'{round((total_cor/total_casas)*100)}%',
                f'{round(((total_cor-1)/total_casas)*100)}%',
                f'{round(((total_cor+1)/total_casas)*100)}%',
                f'{round(((total_cor+2)/total_casas)*100)}%'
            ]
        }
    ]
    return random.choice(questoes)

# Perguntas de probabilidade
PERGUNTAS = {
    "1,1": {
        "questao": "Qual a probabilidade de sair um número par ao lançar um dado de 6 faces?",
        "opcoes": ["1/2", "1/3", "2/3"],
        "resposta": "1/2"
    },
    "1,2": {
        "questao": "Se um baralho tem 52 cartas, qual a chance de tirar um Ás?",
        "opcoes": ["1/13", "1/26", "1/52"],
        "resposta": "1/13"
    },
    "1,3": {
        "questao": "Qual a probabilidade de sair um número primo ao lançar um dado de 6 faces?",
        "opcoes": ["1/2", "1/3", "1/6"],
        "resposta": "1/2"
    },
    "1,4": {
        "questao": "Se você jogar uma moeda justa, qual a chance de sair cara?",
        "opcoes": ["1/2", "1/3", "1/4"],
        "resposta": "1/2"
    },
    "1,5": {
        "questao": "Em um baralho, qual a probabilidade de tirar uma carta vermelha?",
        "opcoes": ["1/2", "1/4", "3/4"],
        "resposta": "1/2"
    },
    "1,6": {
        "questao": "Qual a probabilidade de tirar uma bola azul de um saco com 3 azuis e 7 vermelhas?",
        "opcoes": ["3/10", "7/10", "1/2"],
        "resposta": "3/10"
    },
    "2,1": {
        "questao": "Se um dado justo é lançado, qual a chance de sair um número maior que 4?",
        "opcoes": ["1/3", "1/6", "1/2"],
        "resposta": "1/3"
    },
    "2,2": {
        "questao": "Se um número é escolhido ao acaso de 1 a 10, qual a probabilidade de ser um múltiplo de 3?",
        "opcoes": ["2/5", "1/3", "3/10"],
        "resposta": "3/10"
    },
    "2,3": {
        "questao": "Se um saco tem 5 bolas verdes e 5 bolas amarelas, qual a chance de tirar uma bola verde?",
        "opcoes": ["1/2", "1/3", "2/5"],
        "resposta": "1/2"
    },
    "2,4": {
        "questao": "Se um dado é lançado duas vezes, qual a chance de sair dois números ímpares?",
        "opcoes": ["1/4", "1/2", "1/3"],
        "resposta": "1/4"
    },
    "2,5": {
        "questao": "Em um grupo de 20 pessoas, qual a chance de escolher aleatoriamente alguém que faz aniversário em janeiro?",
        "opcoes": ["1/12", "1/10", "1/6"],
        "resposta": "1/12"
    },
    "2,6": {
        "questao": "Se um baralho tem 52 cartas, qual a chance de tirar uma carta de Copas?",
        "opcoes": ["1/4", "1/13", "1/26"],
        "resposta": "1/4"
    },
    "3,1": {
        "questao": "Se um número é escolhido de 1 a 20, qual a probabilidade de ser um número primo?",
        "opcoes": ["2/5", "1/4", "1/2"],
        "resposta": "2/5"
    },
    "3,2": {
        "questao": "Se um dado é lançado, qual a chance de sair um número menor que 3?",
        "opcoes": ["1/3", "1/6", "1/2"],
        "resposta": "1/3"
    },
    "3,3": {
        "questao": "Se uma moeda honesta é jogada 3 vezes, qual a chance de sair três caras?",
        "opcoes": ["1/8", "1/4", "1/2"],
        "resposta": "1/8"
    },
    "3,4": {
        "questao": "Se um dado de 8 faces é lançado, qual a chance de sair um número maior que 6?",
        "opcoes": ["1/4", "1/2", "1/8"],
        "resposta": "1/4"
    },
    "3,5": {
        "questao": "Se uma senha de 4 dígitos é criada com números de 0 a 9, qual a chance de ser 1234?",
        "opcoes": ["1/1000", "1/10000", "1/9999"],
        "resposta": "1/10000"
    },
    "3,6": {
        "questao": "Se um dado justo é lançado, qual a chance de sair um número ímpar?",
        "opcoes": ["1/2", "1/3", "2/3"],
        "resposta": "1/2"
    },
    "4,1": {
        "questao": "Se uma roleta tem 12 números, qual a probabilidade de cair em um número maior que 9?",
        "opcoes": ["1/4", "1/3", "1/2"],
        "resposta": "1/4"
    },
    "4,2": {
        "questao": "Se um baralho tem 52 cartas, qual a chance de tirar um Rei ou uma Dama?",
        "opcoes": ["2/13", "1/13", "1/26"],
        "resposta": "2/13"
    },
    "4,3": {
        "questao": "Se um número de 1 a 50 é escolhido ao acaso, qual a probabilidade de ser múltiplo de 5?",
        "opcoes": ["1/5", "1/10", "1/4"],
        "resposta": "1/5"
    },
    "4,4": {
        "questao": "Se uma moeda é lançada 2 vezes, qual a chance de sair pelo menos uma cara?",
        "opcoes": ["3/4", "1/2", "1/4"],
        "resposta": "3/4"
    },
    "4,5": {
        "questao": "Se um dado é lançado, qual a chance de sair um número maior que 2 e menor que 5?",
        "opcoes": ["1/3", "1/6", "1/2"],
        "resposta": "1/3"
    },
    "4,6": {
        "questao": "Se uma urna tem 3 bolas vermelhas, 4 azuis e 3 verdes, qual a chance de tirar uma azul?",
        "opcoes": ["2/5", "3/10", "2/3"],
        "resposta": "2/5"
    },
    "5,1": {
        "questao": "Se um número é escolhido de 1 a 100, qual a probabilidade de ser múltiplo de 10?",
        "opcoes": ["1/10", "1/5", "1/20"],
        "resposta": "1/10"
    },
    "5,2": {
        "questao": "Se um dado é lançado, qual a chance de sair um número diferente de 6?",
        "opcoes": ["5/6", "1/6", "1/3"],
        "resposta": "5/6"
    },
    "5,3": {
        "questao": "Se uma moeda honesta é jogada 4 vezes, qual a chance de sair exatamente duas caras?",
        "opcoes": ["3/8", "1/2", "1/4"],
        "resposta": "3/8"
    },
    "5,4": {
        "questao": "Se um baralho tem 52 cartas, qual a chance de tirar uma carta que não seja de Espadas?",
        "opcoes": ["3/4", "1/4", "2/3"],
        "resposta": "3/4"
    },
    "5,5": {  # Casa especial
        "questao": "Se um dado justo é lançado, qual a probabilidade de sair um 6?",
        "opcoes": ["1/6", "1/3", "1/12"],
        "resposta": "1/6"
    },
    "5,6": {
        "questao": "Se uma roleta tem 10 números, qual a chance de cair em um número ímpar?",
        "opcoes": ["1/2", "2/5", "3/10"],
        "resposta": "1/2"
    },
    "6,1": {
        "questao": "Se um número é escolhido ao acaso de 1 a 200, qual a probabilidade de ser múltiplo de 25?",
        "opcoes": ["1/25", "1/20", "1/10"],
        "resposta": "1/10"
    },
    "6,2": {
        "questao": "Se um dado de 8 faces é lançado, qual a chance de sair um número par?",
        "opcoes": ["1/2", "1/4", "3/4"],
        "resposta": "1/2"
    },
    "6,3": {
        "questao": "Se um baralho tem 52 cartas, qual a chance de tirar um número maior que 10?",
        "opcoes": ["3/13", "1/4", "1/3"],
        "resposta": "3/13"
    },
    "6,4": {
        "questao": "Se uma moeda é lançada 5 vezes, qual a chance de sair todas as caras?",
        "opcoes": ["1/32", "1/16", "1/64"],
        "resposta": "1/32"
    },
    "6,5": {
        "questao": "Se um dado é lançado duas vezes, qual a chance de sair um total de 7?",
        "opcoes": ["1/6", "1/12", "1/8"],
        "resposta": "1/6"
    },
    "6,6": {
        "questao": "Se uma urna tem 4 bolas verdes, 3 azuis e 3 vermelhas, qual a chance de tirar uma verde?",
        "opcoes": ["2/5", "4/10", "1/3"],
        "resposta": "2/5"
    }
}

@app.route('/')
def index():
    if 'pontos' not in session:
        session['pontos'] = {'1': 0, '2': 0}
        session['jogador_atual'] = 1
        session['dados_girados'] = []
        
    # Mostrar regras do jogo
    regras = {
        'titulo': "Bem-vindo ao jogo de tabuleiro de probabilidade!🎲",
        'regras': [
            "Cada jogador lançará 2 vezes o dado.",
            f"Cada cor terá pontuações específicas: {', '.join([f'{cor}: {valor} pontos' for cor, valor in PONTOS_COR.items()])}",
            "Cada jogador terá 40 segundos para responder a questão.",
            "Caso o tempo acabe ou a resposta esteja incorreta, passa a vez.",
            "O campeão é quem acumular 10 pontos primeiro ou tirar a casa premiada.🏆"
        ]
    }
    
    return render_template('index.html', 
                         tabuleiro=CORES,
                         pontos=session['pontos'],
                         jogador_atual=session['jogador_atual'],
                         regras=regras,
                         dados_girados=session.get('dados_girados', []))

@app.route('/jogar_dado')
def jogar_dado():
    valor = random.randint(1, 6)
    return jsonify({'valor': valor})

@app.route('/get_pergunta', methods=['POST'])
def get_pergunta():
    dados = request.get_json()
    coord_key = f"{dados['x']},{dados['y']}"
    
    if coord_key in PERGUNTAS:
        return jsonify(PERGUNTAS[coord_key])
    return jsonify({'erro': 'Pergunta não encontrada'})

@app.route('/proximo_jogador')
def proximo_jogador():
    session['jogador_atual'] = 2 if session['jogador_atual'] == 1 else 1
    session.modified = True
    return jsonify({
        'jogador_atual': session['jogador_atual']
    })

@app.route('/verificar_resposta', methods=['POST'])
def verificar_resposta():
    dados = request.get_json()
    resposta_usuario = dados['resposta']
    coordenada = dados['coordenada']
    
    coord_key = f"{coordenada['x']},{coordenada['y']}"
    
    if coord_key in PERGUNTAS:
        pergunta = PERGUNTAS[coord_key]
        correto = resposta_usuario == pergunta['resposta']
        
        if correto:
            x, y = int(coordenada['x']) - 1, int(coordenada['y']) - 1
            cor = CORES[x][y]
            pontos = PONTOS_COR[cor]
            session['pontos'][str(session['jogador_atual'])] += pontos
            
        session['jogador_atual'] = 2 if session['jogador_atual'] == 1 else 1
        session.modified = True
        
        return jsonify({
            'correto': correto,
            'pontos': session['pontos'],
            'jogador_atual': session['jogador_atual']
        })
    
    return jsonify({'erro': 'Coordenada inválida'})

@app.route('/reiniciar_jogo')
def reiniciar_jogo():
    session['pontos'] = {'1': 0, '2': 0}
    session['jogador_atual'] = 1
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
