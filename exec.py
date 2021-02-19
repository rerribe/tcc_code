#%matplotlib inline
import os
import sys
import string
import numpy as np
import matplotlib.pyplot as plt
from sympy import *
from qm import*
from math import*
from random import shuffle

plt.rcParams['figure.figsize'] = (15,5)

qm = QuineMcCluskey()

#Lê o arquivo de extensao .kiss e

temp = open('lion.kiss2')
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

tamanho_espaco_busca = math.ceil(np.log2(estados_convertido))


msf_pronta = []

l = line_char[5:]

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
    linha = entrada+atual_convertido[i]+proximo_convertido[i]+saida
    msf_pronta.append(linha)
    #print(msf_pronta[i])

    
def calculo_peso(lista_1):
    contador_implicante = 0
    contador_termo = 0
    #tamanho_calculo = len(tamanho_espaco_busca)+len(saida)
    #para_calculo = lista_l[:tamanho_calculo]
    for i in range(len(lista_1)):
        contador_termo += 1
        for j in range(len(lista_1[i])):
            if (lista_1[i][j] == '1'):
                contador_implicante += 1
    return contador_implicante+contador_termo

def prepara_lista(lista):
    tamanho_calculo = len(entrada)+len(atual_convertido[1])
    para_calculo = []
    #print(len(entrada),len(atual_convertido[1]),len(proximo_convertido[1]),len(saida), len(lista[1]))
    for i in range(len(lista)):
        para_calculo.append(lista[i][tamanho_calculo:])
    return calculo_peso(para_calculo)
    

for i in range (tamanho_espaco_busca**2):
        espaco_busca.append(bin(i)[2:].zfill(tamanho_espaco_busca))
        #espaco_aleatorio.append(bin(i)[2:].zfill(tamanho_espaco_busca))

def cria_nova_msf():
    #print(tamanho_espaco_busca)
    espaco_aleatorio = espaco_busca.copy()
    shuffle(espaco_aleatorio)
    return set(espaco_aleatorio)

#nova_msf = []

def correspondente(palavra):
    espaco_aleatorio = list(cria_nova_msf())
    for i in range(len(espaco_busca)):
        if palavra == espaco_busca[i]:
            return espaco_aleatorio[i]


def nova_maquina():
    novo_atual = []
    novo_proximo = []
    nova_msf = []
    for i in range(len(l)):
        #print(atual_convertido[i],proximo_convertido[i])
        novo_atual.append(correspondente(atual_convertido[i]))
        novo_proximo.append(correspondente(proximo_convertido[i]))
        nova_atrib = lista_entradas[i]+novo_atual[i]+novo_proximo[i]+lista_saidas[i]
        nova_msf.append(nova_atrib)
        
    return nova_msf



def simulated_annealing(temperatura):
    temperatura_final = 1
    melhor = list(qm.simplify_los(msf_pronta))
    historico = [prepara_lista(melhor)]
    while temperatura > temperatura_final:
        for i in range(10):
            nova_solucao = nova_maquina()
            np.warnings.filterwarnings('ignore')
            nova_solucao_simplificada = list(qm.simplify_los(nova_solucao))
            probabilidade = np.random.normal()
            if (prepara_lista(nova_solucao_simplificada) - prepara_lista(melhor)) < 0  or probabilidade < (np.log(-(prepara_lista(nova_solucao_simplificada)) - (prepara_lista(melhor)))/temperatura):
                melhor = nova_solucao_simplificada
                historico.append(prepara_lista(melhor))
        temperatura = temperatura-1
    return melhor, historico


temperatura = 50
resultado, historico = simulated_annealing(temperatura)
print(resultado)
print(historico)
plt.plot(historico)
#plt.plot(historico, hv(historico))