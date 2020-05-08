# DAMAS - API

Desenvolvido em Python3, utilizando Flask.

Jogo de damas baseado em requisições API, e permanência de dados em memória (mais detalhes abaixo).

## Escopo

Jogo entre dois jogadores, 'p' e 'b' simbolizando as cores preto e branco;
Tabuleiro quadrado, de 64 casas alternadamente claras e escuras, dispondo de 12 peças brancas e 12 pretas(brancas não válidas);
O jogador que conseguir capturar todas as peças do inimigo ganha a partida;
No início da partida, as peças devem ser colocadas no tabuleiro sobre as casas escuras, da seguinte forma: nas três primeiras filas horizontais, as peças brancas; e, nas três últimas, as peças pretas;
A peça movimenta-se em diagonal, sobre as casas escuras (válidas), para a frente, e uma casa de cada vez;
A peça pode capturar a peça do adversário movendo-se para frente e para trás;
A peça que atingir a oitava casa adversária, parando ali, será promovida a "dama", Destacando-a;
A dama pode mover-se para trás e para frente em diagonal uma casa de cada vez, diferente das outras peças, que movimentam-se apenas para frente em diagonal;

A partida termina quando;
Um jogador perder todas as peças;
Os dois jogadores concordarem com o empate;
Ocorrer 20 lances sucessivos de Damas, sem tomada ou deslocamento de pedra.


## Chamadas API

Por padrão em Flask temos localhost como http://127.0.0.1:5000/

Requisição que inicia um novo jogo, deverá ser chamada para iniciar / reiniciar uma partida.
```bash
Requisição 1 - GET:
http://127.0.0.1:5000/game/newgame
Resposta 1 - status 200:
{
  "ID partida": "aee6f254-1665-4c94-b882-860478bb063c",
  "Primeiro a Jogar": "p"
}
Resposta 2 - status 404:
{
  "Erro": "Partida não localizada"
}
```
Requisição para acompanhar os status da partida
```bash
Requisição 2 - GET:
http://127.0.0.1:5000/game
Resposta 1 - status 200:
{
  "ID partida": "aee6f254-1665-4c94-b882-860478bb063c",
  "Turno do jogador": "p"
}
Resposta 2 - status 404:
{
  "Erro": "Partida não iniciada, acesse:game/newgame"
}
```
Requisição para exibir o tabuleiro do jogo corrente (não estruturado para ser um json utilizável).
```bash
Requisição 3 - GET:
http://127.0.0.1:5000/game/{'ID partida'} || ID partida ='aee6f254-1665-4c94-b882-860478bb063c'

Resposta 1 - status 200:
[
  "|H|>>|#|b|#|b|#|b|#|b|",
  "|G|>>|b|#|b|#|b|#|b|#|",
  "|F|>>|#|b|#|b|#|b|#|b|",
  "|E|>>| |#| |#| |#| |#|",
  "|D|>>|#| |#| |#| |#| |",
  "|C|>>|p|#|p|#|p|#|p|#|",
  "|B|>>|#|p|#|p|#|p|#|p|",
  "|A|>>|p|#|p|#|p|#|p|#|",
  "|-|>>|^|^|^|^|^|^|^|^|",
  "|X|>>|1|2|3|4|5|6|7|8|"
]
Resposta 2 - status 404:
{
  "Erro": "Partida não localizada"
}
```
Requisição para movimentar peças no tabuleiro; para visualizar jogo corrente use Requisição-3.
```bash
Requisição 4 - POST:
http://127.0.0.1:5000/game/move/{'ID partida'} || ID partida ='aee6f254-1665-4c94-b882-860478bb063c'
{
  "Turno do jogador": "p",
  "Movimento de": "e5",
  "Movimento para": "c7"
}
Resposta 1 - status 200:
{
  "Sucesso": "Peca movida"
}
Resposta 2 - status 200:
{
  "Sucesso": "Peca movida, e oponente perdeu uma peça"
}
Resposta 3 - status 404:
{
  "Erro": "Partida não localizada"
}
```

## Contribuição
Pull requests são bem vindos. Para maiores alterações dicas e outros assuntos envie-me um email =D

Preparing to launch my little rocket >===>
