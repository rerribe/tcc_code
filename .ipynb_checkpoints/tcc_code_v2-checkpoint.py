import os
import sys
import string
import numpy as np
#import matplotlib.pyplot as plt
from sympy import *
from qm import*
from math import*
from random import shuffle
import random

#plt.rcParams['figure.figsize'] = (15,5)

qm = QuineMcCluskey()

#Lê o arquivo de extensao .kiss e separa as listas com as informações sobre a msf

temp = open('lion9.kiss2')
line_char = temp.readlines()
l = []
entrada = []
lista_entradas = []
saida = []
lista_saidas = []

estados = []
estados = line_char[4:5]

atual = []
atual_inteiro = []
atual_convertido = []

proximo = []
proximo_inteiro = []
proximo_convertido = []

espaco_busca = []
espaco_aleatorio = []
estados_convertido = int(estados[0].split()[1])

#define o tamanho do espaço de busca basedado no valor entregue pelo arquivo

tamanho_espaco_busca = math.ceil(np.log2(estados_convertido))


msf_pronta = []

l = line_char[5:]

# nesse trecho os dados são separados, tratados e é criada a lista no formato que o Quine_Mccluskey pode simplificar

for i in range(len(l)):
    entrada = l[i].split()[0]
    lista_entradas.append(entrada)
    
    atual = l[i].split()[1]
    proximo = l[i].split()[2]
    saida = l[i].split()[3]
    lista_saidas.append(saida)
    
    atual_inteiro = int(atual[2:])
    proximo_inteiro = int(proximo[2:])
    atual_convertido.append(bin(atual_inteiro)[2:].zfill(tamanho_espaco_busca))
    #atual_binario = atual_convertido[i]
    proximo_convertido.append(bin(proximo_inteiro)[2:].zfill(tamanho_espaco_busca))
    #proximo_binario = proximo_convertido[i]
    linha = str(lista_entradas[i])+str(atual_convertido[i])+str(proximo_convertido[i])+str(lista_saidas[i])
    msf_pronta.append(linha)
    #print(msf_pronta[i])


for i in range (2**tamanho_espaco_busca):
        espaco_busca.append(bin(i)[2:].zfill(tamanho_espaco_busca))
        #espaco_aleatorio.append(bin(i)[2:].zfill(tamanho_espaco_busca))


#def cria_nova_msf():
#    #print(tamanho_espaco_busca)
#    espaco_aleatorio = espaco_busca.copy()
#    shuffle(espaco_aleatorio)
#    return set(espaco_aleatorio)


def correspondente(palavra1,palavra2):
    #espaco_aleatorio = list(cria_nova_msf())
    espaco_aleatorio = palavra2
    for i in range(len(espaco_busca)):
        if palavra1 == espaco_busca[i]:
            return str(espaco_aleatorio[i])


def nova_maquina():
    novo_atual = []
    novo_proximo = []
    nova_msf = []
    
    espaco_aleatorio = espaco_busca.copy()

    # esse trecho a ideia é realizar varios embaralhamentos do espaco de busca na tentativa de aumentar a diferenca entre a 
    # msf inicial e a msf de saida

    for i in range(5):
    	shuffle(espaco_aleatorio)
    
    # percebi que esse trecho estava gerando uma nova lista de atribuicoes a cada chamada de teste de correspondencia
    # creio que isso estava causando um efeito indesejado, uma que vez isso provavelmente estava gerando inconsistencias 
    # que podem estar passando batidas
    # então agora é criada apenas uma lista que é utilizada para a comparacao entre atual e proximos estados da primeira 
    # lista e do novo conjunto de atribuicoes

    # aparentemente essa alteração, que pra mim faz sentido, fez cair muito a quantidade de geracao de msf's de tamanho menor que
    # a inicial
    
    for i in range(len(l)):
        #print(atual_convertido[i],proximo_convertido[i])
        novo_atual.append(correspondente(atual_convertido[i],espaco_aleatorio))
        #print("novo atual:",novo_atual[i])
        novo_proximo.append(correspondente(proximo_convertido[i],espaco_aleatorio))
        #print("novo proximo:",novo_proximo[i])
        nova_atrib = str(lista_entradas[i])+str(novo_atual[i])+str(novo_proximo[i])+str(lista_saidas[i])
        nova_msf.append(nova_atrib)
        
    return nova_msf


def simplifica(lista):
    lista_para_simplificar = []
    for i in range(len(lista)):
        lista_para_simplificar.append(lista[i][:-len(saida)])

    lista_simplificada = qm.simplify_los(lista_para_simplificar)
    return lista_simplificada

def calcula_custo(lista):
    #nova_lista = []
    nova_lista_prox = []
    nova_lista_transicoes = []
    lista_para_calculo = []
    comp_transit = len(entrada)+len(atual_convertido[0])
    comp_seg_lista = len(saida)+tamanho_espaco_busca
    for i in range(len(lista)):
        #nova_lista.append(lista[i][:-len(saida)])
        nova_lista_prox.append(lista[i][comp_transit:])
        nova_lista_transicoes.append(lista[i][:-tamanho_espaco_busca])
        
    for i in range(len(nova_lista_prox)):
        for j in range(len(nova_lista_prox[i])):
            if nova_lista_prox[i][j] == '1':
                #print(nova_lista_saidas[i])
                lista_para_calculo.append(nova_lista_transicoes[i])
    
    quantidade_dc = 0
    for i in range(len(lista_para_calculo)):
        for j in range(len(lista_para_calculo[i])):
            if lista_para_calculo[i][j] == '-':
                quantidade_dc += 1
                
    custo = (len(lista_para_calculo)*len(lista_para_calculo[0]))-quantidade_dc
    return custo



def simulated_annealing(temperatura):
    temperatura_inicial = temperatura
    temperatura_final = 10
    melhor = list(simplifica(msf_pronta))
    custo_inicial = calcula_custo(melhor)
    print(custo_inicial)
    historico = [custo_inicial]
    while temperatura > temperatura_final:
        for i in range(2):
            nova_solucao = nova_maquina()
            np.warnings.filterwarnings('ignore')
            nova_solucao_simplificada = list(simplifica(nova_solucao))
            custo_local = calcula_custo(nova_solucao_simplificada)
            melhor_custo = calcula_custo(melhor)
            probabilidade = np.random.random_sample() # define um sample aleatorio entre 0 e 1, com zero fazendo parte do intervalo
            if (custo_local - melhor_custo < 0):
            	melhor = nova_solucao_simplificada
            	historico.append(melhor_custo)
            	print(temperatura,"trocou!!")
            else:
                if (probabilidade < np.log(-(custo_local-melhor_custo)/temperatura)):
            	    melhor = nova_solucao_simplificada
            	    historico.append(melhor_custo)
            	    print(temperatura,"trocou!!")
            #sys.stdout.write('.')
        
        if temperatura > temperatura/2:
        	temperatura = temperatura-10
        else:
        	temperatura = temperatura-5
        #print(temperatura)
        

    custo_final = calcula_custo(melhor)
    melhora = 100-((custo_final *100)/custo_inicial)
    
    return melhor, historico, melhora



for i in range(10):
    temperatura = 3000
    resultado, historico, melhora_da_solucao = simulated_annealing(temperatura)
    for i in range(len(resultado)):
        print(resultado[i])
    print(historico)
    print("melhorou:",melhora_da_solucao,"%")

#plt.plot(historico)
#plt.plot(historico, hv(historico))