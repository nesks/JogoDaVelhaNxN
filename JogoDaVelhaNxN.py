#!/usr/bin/env python3
# -*- codificacao: utf-8 -*-
"""
Created on Sun Sep 23 15:33:59 2018
@author: talles medeiros, decsi-ufop
"""


"""
Trabalho efetuado pelos alunos do curso de Sistemas de Informação:

Felipe Sousa Nunes - 16.1.8152
Carlos Alberto - 16.2.8394
Milena Esther de Sá 16.8365

"""


"""
Este código servirá de exemplo para o aprendizado do algoritmo MINIMAX 
na disciplina de Inteligência Artificial - CSI457
Semestre: 2020/1
"""

#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
import random
from os import system
import copy
"""
Um versão simples do algoritmo MINIMAX para o Jogo da Velha.
"""

# Representando a variável que identifica cada jogador
# HUMANO = Oponente humano
# COMP = Agente Inteligente
# tabuleiro = dicionário com os valores em cada posição (x,y)
# indicando o jogador que movimentou nessa posição.
# Começa vazio, com zero em todas posições.
HUMANO = -1
COMP = +1
tabuleiro = []
"""
Funcao para avaliacao heuristica do estado.
:parametro (estado): o estado atual do tabuleiro
:returna: +1 se o computador vence; -1 se o HUMANOo vence; 0 empate
 """
def avaliacao(estado):
    
    if vitoria(estado, COMP):
        retornar = +infinity
    elif vitoria(estado, HUMANO):
        retornar = -infinity
    else:
        retornar = 0

    return retornar
""" fim avaliacao (estado)------------------------------------- """

"""Essa função serve para criar uma lista de conjuntos de itens, basicamente cria uma lista separadando as linhas, colunas e diagonais"""
def criaListaDeLinhaColunaDiagonal(estado):
    win_estado = []
    i=0
    j=0
    tam=len(estado)
    tamDec=tam
    win_linha=[]
    win_coluna=[]
    win_diagonal1=[]
    win_diagonal2=[]

    while(i<tam):   #para toda a linha
        j=0
        while(j<tam):    #para toda a coluna
            win_linha.append([estado[i][j],i,j])   #todas as linhas
            win_coluna.append([estado[j][i],j,i])   #todas as colunas
            j+=1
        
        win_estado.append(win_linha)    #adiciona a linha na matriz de estados
        win_estado.append(win_coluna)   #adiciona a coluna na matriz de estados
        win_linha = []
        win_coluna = []
        tamDec-=1  
        win_diagonal1.append([estado[i][i],i,i])       #diagonal linha = coluna
        win_diagonal2.append([estado[tamDec][i],tamDec,i])  #diagonal linha decrescente e coluna crescente
        
        
        i+=1
    
    win_estado.append(win_diagonal1)    #adiciona a primeira diagonal na lista de estados
    win_estado.append(win_diagonal2)    #adiciona a segunda diagonal na lista de estados
    
    return win_estado

def vitoria(estado, jogador):
    """
    Esta funcao testa se um jogador especifico vence. Possibilidades:
    * N linhas     [X ... N vezes] or [O ... N vezes]
    * N colunas    [X ... N vezes] or [O ... N vezes]
    * Duas diagonais  [X ... N vezes] or [O ... N vezes]
    :param. (estado): o estado atual do tabuleiro
    :param. (jogador): um HUMANO ou um Computador
    :return: True se jogador vence
    """

    win_estado = []
  
    win_estado = criaListaDeLinhaColunaDiagonal(estado) #recebe as linhas, colunas e diagonais em uma lista de listas.
    # Se um, dentre todos os alinhamentos pertence um mesmo jogador, 
    # então o jogador vence!'
    for  conjuntoParaVitoria in win_estado: #entre todas as possibilidades de vitoria
        if all(itemParaVitoria[0] == jogador for itemParaVitoria in conjuntoParaVitoria):   #verifica se todos os itens desse conjunto são iguais (todos os itens de UMA linha por ex.)
            return True

    return False
""" ---------------------------------------------------------- """

"""
Testa fim de jogo para ambos jogadores de acordo com estado atual
return: será fim de jogo caso ocorra vitória de um dos jogadores.
"""
def fim_jogo(estado):
    return vitoria(estado, HUMANO) or vitoria(estado, COMP)
""" ---------------------------------------------------------- """

"""
Verifica celular vazias e insere na lista para informar posições
ainda permitidas para próximas jogadas.
"""
def celulas_vazias(estado):
    celulas = []
    for x, row in enumerate(estado):
        for y, cell in enumerate(row):
            if cell == 0: celulas.append([x, y])
    return celulas
""" ---------------------------------------------------------- """

"""
Um movimento é valido se a célula escolhida está vazia.
:param (x): coordenada X
:param (y): coordenada Y
:return: True se o tabuleiro[x][y] está vazio
"""
def movimento_valido(x, y):
    if [x, y] in celulas_vazias(tabuleiro):
        return True
    else:
        return False
""" ---------------------------------------------------------- """

"""
Executa o movimento no tabuleiro se as coordenadas são válidas
:param (x): coordenadas X
:param (y): coordenadas Y
:param (jogador): o jogador da vez
"""
def exec_movimento(x, y, jogador):
    if movimento_valido(x, y):
        tabuleiro[x][y] = jogador
        return True
    else:
        return False
""" ---------------------------------------------------------- """
contador = 0
def incrementar():
    global contador
    contador+= 1
def zerar():
    global contador
    contador = 0
def imprimir():
    global contador
    print("valor do contador: ", contador)

"""
Função da IA que escolhe o melhor movimento
:param (estado): estado atual do tabuleiro
:param (profundidade): índice do nó na árvore (0 <= profundidade <= 9),
mas nunca será nove neste caso (veja a função iavez())
:param (jogador): um HUMANO ou um Computador
:return: uma lista com [melhor linha, melhor coluna, melhor placar]
"""
def minimax(estado, profundidade, jogador):

    # valor-minmax(estado)
    if jogador == COMP:
        melhor = [-1, -1, -infinity]
    else:
        melhor = [-1, -1, +infinity]

    # valor-minimax(estado) = avaliacao(estado)
    if profundidade == 0 or fim_jogo(estado):
        if fim_jogo(estado):
            placar = avaliacao(estado)
        else:
            placar = objetivo2(estado, jogador) #retorna a quantidade de chances de vitoria existente nesse estado pelo jogador
        return [-1, -1, placar]

    for cell in celulas_vazias(estado):
        
        incrementar()  #chama a função para incrementar o contador de estados

        x, y = cell[0], cell[1]
        estado[x][y] = jogador
        placar = minimax(estado, profundidade - 1, -jogador)
        estado[x][y] = 0
        placar[0], placar[1] = x, y

        if jogador == COMP:
            if placar[2] > melhor[2]:
                melhor = placar  # valor MAX
        else:
            if placar[2] < melhor[2]:
                melhor = placar  # valor MIN

    return melhor
""" ---------------------------------------------------------- """


"""Objetivo dessa avaliação é verificar em uma determinada quantas chances de vitoria ela tem dado um estado"""


def objetivo2(estado, jogador):

    win_estado = []
    win_estado = criaListaDeLinhaColunaDiagonal(estado)
    teste = True
    chances = 0 #variavel que será retornada com o placar de possibilidades de vitoria do jogador nesse estado. Quantas chances o jogador tem de ganhar no estado atual.
    for conjunto in win_estado: #as linhas, colunas e diagonais
        teste=True
        for coordenada in conjunto:  #para cada coordenada de uma linha/coluna ou diagonal
            if coordenada[0] == jogador: 
                teste = False
        if(teste):
            chances+=1
    return chances #retorna o placar final dessa coordenada.

""" ---------------------------------------------------------- """
"""
Limpa o console para SO Windows
"""
def limpa_console():
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')
""" ---------------------------------------------------------- """

"""
Imprime o tabuleiro no console
:param. (estado): estado atual do tabuleiro
"""
def exibe_tabuleiro(estado, comp_escolha, humano_escolha):
    ('----------------')
    nlinha=0
    ncoluna=0
    print('\n ','x  ', end='')
    for row in estado:
        if nlinha==0:
            while ncoluna != len(row):
                print('|', ncoluna, '|', end='')
                ncoluna=ncoluna+1    
        

        print('\n ',nlinha,' ', end='')
      
        nlinha=nlinha+1
        for cell in row:
            if cell == +1:
                print('|', comp_escolha, '|', end='')
            elif cell == -1:
                print('|', humano_escolha, '|', end='')
            else:
                print('|', ' ', '|', end='')
    print('\n----------------')
""" ---------------------------------------------------------- """

"""
Chama a função minimax se a profundidade < 9,
ou escolhe uma coordenada aleatória.
:param (comp_escolha): Computador escolhe X ou O
:param (humano_escolha): HUMANO escolhe X ou O
:return:
"""
"""
heuristica para chamar o minimax somente quando o humano tem chance de vencer, (espaços totais menos tamanho do tabuleiro mais 1)
Assim, quando o jogador for fazer a jogada numero tamanho do tabuleiro -1, a IA vai ativar o minimax. reduzindo o tamanho da profundidade.
"""

  

def IA_vez(comp_escolha, humano_escolha, num_n):

    zerar()
    profundidade =  len(celulas_vazias(tabuleiro))
    prof = profundidade
    if profundidade == 0 or fim_jogo(tabuleiro):
        return
    limpa_console()
    print('Vez do Computador [{}]'.format(comp_escolha))
    exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
    if profundidade > 9:
        profundidade = 3
    if prof  > ((int(num_n)*int(num_n))-(int(num_n)*2 - 3)) and prof > 8:  #heuristica para jogar randomicamente as primeiras vezes
        item = random.choice(celulas_vazias(tabuleiro))
        x, y = item[0], item[1]   
        print("jogando randomicamente") 
    else:
        print("ENTROU NO MINIMAX COM PROFUNDIDADE ",profundidade)
        start_time = time.time()
        move = minimax(tabuleiro, profundidade, COMP)
        print("--- %s seconds ---" % (time.time() - start_time))
        imprimir()
        x, y = move[0], move[1]
    exec_movimento(x,y, COMP)
    time.sleep(1)
""" ---------------------------------------------------------- """


def HUMANO_vez(comp_escolha, humano_escolha, num_n):
    """
    O HUMANO joga escolhendo um movimento válido
    :param comp_escolha: Computador escolhe X ou O
    :param humano_escolha: HUMANO escolhe X ou O
    :return:
    """
    profundidade = len(celulas_vazias(tabuleiro))
    if profundidade == 0 or fim_jogo(tabuleiro):
        return

    # Dicionário de movimentos válidos
    linha = -1
    coluna= -1
    

    #limpa_console()
    print('Vez do HUMANO [{}]'.format(humano_escolha))
    exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
    while (linha== -1 and coluna==-1):
        while (linha < 0 or linha >= int(num_n)):
            try:
                linha = int(input('Qual a linha desejada? '))
            except:
                print('Escolha Inválida!')

        while (coluna < 0 or coluna >= int(num_n)):
            try:
                coluna = int(input('Qual a coluna desejada? '))
            except:
                print('Escolha Inválida!')
        
        tenta_movimento = exec_movimento(linha, coluna, HUMANO)
        if tenta_movimento == False:
            print('Movimento Inválido')
            linha = -1
            coluna = -1
        
""" ---------------------------------------------------------- """


"""Função para criar o tabuleiro n x n """
def cria_tabuleiro(num_n):
    linhas = []
    i=0
    while i < int(num_n):
        linhas.append(0)
        i+=1
    i=0
    while i <int(num_n):
        tabuleiro.append(copy.deepcopy(linhas))
        i+=1
    print(tabuleiro)
    


"""
Funcao Principal que chama todas funcoes
"""
def main():
    limpa_console()
    humano_escolha = '' # Pode ser X ou O
    comp_escolha = '' # Pode ser X ou O
    primeiro = ''  # se HUMANO e o primeiro
    num_n = ''

    while num_n == '':
        try:
            print('')
            num_n = input('Escolha o tamanho do tabuleiro: ').upper()
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Errada')
    cria_tabuleiro(num_n)
    limpa_console()
    # HUMANO escolhe X ou O para jogar
    while humano_escolha != 'O' and humano_escolha != 'X':
        try:
            print('')
            humano_escolha = input('Escolha X or O\n: ').upper()
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Errada')

    # Setting Computador's choice
    if humano_escolha == 'X':
        comp_escolha = 'O'
    else:
        comp_escolha = 'X'

    # HUMANO pode começar primeiro
    limpa_console()
    while primeiro != 'S' and primeiro != 'N':
        try:
            primeiro = input('Primeiro a Iniciar?[s/n]: ').upper()
        except KeyboardInterrupt:
            print('Tchau!')
            exit()
        except:
            print('Escolha Errada!')

    # Laço principal do jogo
    while len(celulas_vazias(tabuleiro)) > 0 and not fim_jogo(tabuleiro):
        if primeiro == 'N':
            IA_vez(comp_escolha, humano_escolha,num_n)
            primeiro = ''
        limpa_console()
        HUMANO_vez(comp_escolha, humano_escolha, num_n)
        limpa_console()
        IA_vez(comp_escolha, humano_escolha,num_n)


    # Mensagem de Final de jogo
    if vitoria(tabuleiro, HUMANO):
        #limpa_console()
        print('Vez do HUMANO [{}]'.format(humano_escolha))
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Você Venceu!')
    elif vitoria(tabuleiro, COMP):
        #limpa_console()
        print('Vez do Computador [{}]'.format(comp_escolha))
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Você Perdeu!')
    else:
        #limpa_console()
        exibe_tabuleiro(tabuleiro, comp_escolha, humano_escolha)
        print('Empate!')
        
    exit()


if __name__ == '__main__':
    main()