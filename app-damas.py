from flask import Flask, request, jsonify
from uuid import uuid4
from random import choice

app = Flask(__name__)


class Match:
    game_id_run = None
    table_run = None
    player_turn_run = None

    def __init__(self, table, player_turn):
        self.id = None
        self.table = table
        self.player_turn = player_turn

    def save(self, game):
        self.__class__.game_id_run = game.id
        self.__class__.table_run = game.table
        self.__class__.player_turn_run = game.player_turn


def start_game():  # def que inicia/reinicia partida (dados de objetos instanciados)
    table = {'H': ['#', 'b', '#', 'b', '#', 'b', '#', 'b'],
             'G': ['b', '#', 'b', '#', 'b', '#', 'b', '#'],
             'F': ['#', 'b', '#', 'b', '#', 'b', '#', 'b'],
             'E': [' ', '#', ' ', '#', ' ', '#', ' ', '#'],
             'D': ['#', ' ', '#', ' ', '#', ' ', '#', ' '],
             'C': ['p', '#', 'p', '#', 'p', '#', 'p', '#'],
             'B': ['#', 'p', '#', 'p', '#', 'p', '#', 'p'],
             'A': ['p', '#', 'p', '#', 'p', '#', 'p', '#'],
             '-': ['^', '^', '^', '^', '^', '^', '^', '^'],
             'X': [1, 2, 3, 4, 5, 6, 7, 8]}
    game = Match(table, choice('pb'))
    game.id = uuid4()
    game.save(game)
    match_info = {"Primeiro a Jogar": game.player_turn, "ID partida": str(game.id)}
    return jsonify(match_info), 200


def game_info():  # def que exibe os status da partida em andamento
    if Match.game_id_run is None:
        match_info = {"Erro": "Partida não iniciada, acesse:game/newgame"}
        return jsonify(match_info), 404
    else:
        match_info = {"Turno do jogador": Match.player_turn_run, "ID partida": Match.game_id_run}
        return jsonify(match_info), 200


def print_gametable(MatchID):  # def que exibe em json(não utilizável) apenas para visualizar tabuleiro da atual partida
    if MatchID == str(Match.game_id_run):
        table_data = Match.table_run
        table_show = []
        for k, v in table_data.items():
            row = ''
            row += '|' + str(k) + '|>>'
            for z in v:
                row += '|' + str(z)
            row += '|'
            table_show.append(row)
        return jsonify(table_show), 200
    else:
        match_info = {"Erro": "Partida não localizada"}
        return jsonify(match_info), 404


def change_player_turn():  # def que altera o turno na instancia do objeto Match
    if Match.player_turn_run in 'p':
        Match.player_turn_run = 'b'
    else:
        Match.player_turn_run = 'p'


def move_piece(piece_from, piece_to):
    piece_from_board = Match.table_run[piece_from[0]][int(piece_from[1]) - 1]
    # charvar = valor diferenca char; baseado na diferenca das letras ex: A-C, 66-68 = -2
    charvar = ord(piece_from[0].upper()) - ord(piece_to[0].upper())
    # numvar = valor diferenca da posição
    numvar = int(piece_from[1]) - int(piece_to[1])
    # trigger = gatilho quando detecta peça do oponente
    trigger = False
    # c_mark/selector guarda estado do objeto detectado no gatilho para substituiçao posterior caso passe em teste 'if'
    c_mark = n_mark = None
    # c_selector/n_selector = variaveis para percorrer o tabuleiro nas 4 direções
    c_selector = n_selector = 0
    # controle de quantidades de loop while; (ver charvar)
    control = abs(charvar)
    # param = variável para verificação da próxima peça, sabendo se é do oponente.
    param = ''
    if Match.player_turn_run in 'p':
        param = 'b'
    else:
        param = 'p'
    if piece_from_board in 'pb':
        while control >= 0:
            if charvar < 0:
                c_selector += 1
            else:
                c_selector -= 1
            if numvar < 0:
                n_selector += 1
            else:
                n_selector -= 1
            control -= 1
            # formula para percorrer dicionário instanciado no objeto Match, com variaveis tipo 'selector' (ver acima)
            next_piece_or_place = Match.table_run[chr(ord(piece_from[0].upper()) + c_selector)][int(piece_from[1]) -
                                                                                                1 + n_selector]
            #verificação para movimento simples (1 salto a frente)
            if next_piece_or_place in ' ' and trigger is False:
                if Match.player_turn_run in 'p' and charvar > 0:
                    match_info = {'Erro': 'não é permitido movimento simples para trás'}
                    return jsonify(match_info), 200
                if Match.player_turn_run in 'b' and charvar < 0:
                    match_info = {'Erro': 'não é permitido movimento simples para trás'}
                    return jsonify(match_info), 200
                (Match.table_run[chr(ord(piece_from[0].upper()) + c_selector)][int(piece_from[1]) - 1 + n_selector]) = \
                    Match.table_run[piece_from[0]][int(piece_from[1]) - 1]
                Match.table_run[piece_from[0]][int(piece_from[1]) - 1] = ' '
                change_player_turn()
                match_info = {'Sucesso': 'Peca movida'}
                return jsonify(match_info)

            # verificação para movimento especial (2 saltos a frente e oponente perde 1 peca)
            if next_piece_or_place in ' ' and trigger is True:
                Match.table_run[chr(ord(piece_from[0].upper()) + c_selector)][int(piece_from[1]) - 1 + n_selector] = \
                    Match.table_run[piece_from[0]][int(piece_from[1]) - 1]
                Match.table_run[chr(ord(piece_from[0].upper()) + c_mark)][int(piece_from[1]) - 1 + n_mark] = ' '
                Match.table_run[chr(ord(piece_from[0].upper()))][int(piece_from[1]) - 1] = ' '
                change_player_turn()
                # JOGADA COMBO
                    # deve ser inserida aqui ou criar nova 'def' - implementações futuras neste repositório
                match_info = {'Sucesso': 'Peca movida, e oponente perdeu uma peça'}
                return jsonify(match_info), 200

            # ativa gatilho, verificando q a proxima peça pertence ao oponente
            if next_piece_or_place in param.lower():
                trigger = True
                c_mark = c_selector
                n_mark = n_selector
            else:
                match_info = {'Erro': 'Jogada não permitida'}
                return jsonify(match_info), 200




def validate_play(match_id, player_turn, move_from, move_to):
    # 0 - ALL BASIC VERIFYING LOGIC
    valid_spots = ['A1', 'A3', 'A5', 'A7', 'B2', 'B4', 'B6', 'B8', 'C1', 'C3', 'C5', 'C7', 'D2', 'D4', 'D6', 'D8', 'E1',
                   'E3', 'E5', 'E7', 'F2', 'F4', 'F6', 'F8', 'G1', 'G3', 'G5', 'G7', 'H2', 'H4', 'H6', 'H8']
    # 1 - VERIFICA SE O ID DE PARTIDA RECEBIDO CONFERE COM ID DO OBJETO INSTANCIADO
    if match_id == str(Match.game_id_run):
        # 2- VALIDAÇÃO DO JOGADOR JOGANDO EM SEU TURNO CORRETAMENTE
        if player_turn not in Match.player_turn_run:
            match_info = {"Erro": "Não é o turno deste jogador"}
            return jsonify(match_info), 400
        # 3 - VALIDAÇÃO DE LOCAIS NO TABULEIRO QUE PODEM SER JOGADOS
        if move_to not in valid_spots or move_from not in valid_spots:
            match_info = {"Erro": "movimento inválido, verifique sua jogada"}
            return jsonify(match_info), 404
        # 4 - VALIDAÇÃO DO JOGADOR PODER MOVER SOMENTE A PEÇA QUE LHE PERTENCE
        piece_from = Match.table_run[move_from[0]][int(move_from[1]) - 1]
        piece_to = Match.table_run[move_to[0]][int(move_to[1]) - 1]
        if player_turn not in piece_from.lower():
            match_info = {"Erro": "A peça selecionada pertence ao outro jogador"}
            return jsonify(match_info), 400
        # 5 - VALIDAÇÃO DO LOCAL FINAL DA PEÇA DEVERÁ SER VAZIO
        if piece_to is not ' ':
            match_info = {"Erro": "Existe uma peça no destino, verifique '(Movimento para)'"}
            return jsonify(match_info), 400
        if True:
            return move_piece(move_from, move_to)
    else:
        match_info = {"Erro": "Partida não localizada"}
        return jsonify(match_info), 404
    # END OF BASIC VERIFYING LOGIC


# INICIO REQUISIÇõES API
@app.route("/game/newgame", methods=['GET'])
def new_game():

    return start_game()


@app.route("/game", methods=['GET'])
def game():

    return game_info()


@app.route("/game/<string:match_id>", methods=['GET'])
def gametable(match_id):

    return print_gametable(match_id)


@app.route("/game/move/<string:Match_ID>", methods=['POST', 'GET'])
def gamemove(Match_ID):

    data = request.get_json()
    player_turn = data['Turno do jogador'].lower()
    move_from = data['Movimento de'].upper()
    move_to = data['Movimento para'].upper()
    return validate_play(Match_ID, player_turn, move_from, move_to)


if __name__ == '__main__':
    app.run(debug=True)


