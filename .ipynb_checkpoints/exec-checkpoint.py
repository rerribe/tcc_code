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

#Lê o arquivo de extensao .kiss e separa as listas com as informações sobre a msf

temp = open('tav.kiss2')
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


#essa função calcula a quantidade de implicantes e variáveis de uma lista
    
def calculo_peso(lista_1):
    contador_dc = 0
    contador_termo = 0
    contador_literal = 0
    #tamanho_calculo = len(tamanho_espaco_busca)+len(saida)
    #para_calculo = lista_l[:tamanho_calculo]
    for i in range(len(lista_1)):
        contador_termo += 1
        for j in range(len(lista_1[i])):
            contador_literal +=1
            if (lista_1[i][j] == '-'):
                contador_dc += 1
    return (contador_termo+contador_literal)-contador_dc

# essa função separa da MSF as linhas relativas ao proximo estado e sáida para a contagem do peso

def prepara_lista(lista):
    para_calculo = []
    #print(len(entrada),len(atual_convertido[1]),len(proximo_convertido[1]),len(saida), len(lista[1]))
    for i in range(len(lista)):
        para_calculo.append(lista[i][len(entrada):-(len(saida))])
    return calculo_peso(para_calculo)
    

# neste ponto é criado o espaco de busca com todos as atribuicoes possíveis para representar a msf

for i in range (tamanho_espaco_busca**2):
        espaco_busca.append(bin(i)[2:].zfill(tamanho_espaco_busca))
        #espaco_aleatorio.append(bin(i)[2:].zfill(tamanho_espaco_busca))

# cria uma lista aleatória com os valores do espaço de busca

def cria_nova_msf():
    #print(tamanho_espaco_busca)
    espaco_aleatorio = espaco_busca.copy()
    shuffle(espaco_aleatorio)
    return set(espaco_aleatorio)

#nova_msf = []

# faz a comparação entre a lista entregue e o valor correspondente a ela na lista de valores aleatórios

def correspondente(palavra):
    espaco_aleatorio = list(cria_nova_msf())
    for i in range(len(espaco_busca)):
        if palavra == espaco_busca[i]:
            return str(espaco_aleatorio[i])

# recebe uma tabela, e a partir de comarações cria outra com os valores trocados pela atribuição aleatória

def nova_maquina():
    novo_atual = []
    novo_proximo = []
    nova_msf = []
    for i in range(len(l)):
        #print(atual_convertido[i],proximo_convertido[i])
        novo_atual.append(correspondente(atual_convertido[i]))
        novo_proximo.append(correspondente(proximo_convertido[i]))
        nova_atrib = str(lista_entradas[i])+str(novo_atual[i])+str(novo_proximo[i])+str(lista_saidas[i])
        nova_msf.append(nova_atrib)
        
    return nova_msf

def simplifica(lista):
    nova_lista = []
    for i in range(len(lista)):
        nova_lista.append(lista[i][:-len(saida)])
    nova_lista_simplificada = list(qm.simplify_los(nova_lista))
    for i in range(len(nova_lista_simplificada)):
        nova_lista_simplificada.append(lista[i][:len(saida)])
    return set(nova_lista_simplificada)

# algoritmo do SA, que realiza as comparaçoes e entrega a atribuição com o menor peso após a simplificação
# a primeira iteração do SA, utiliza o valor da msf entregue pelo arquivo.kiss

def simulated_annealing(temperatura):
    temperatura_inicial = temperatura
    temperatura_final = 10
    melhor = list(simplifica(msf_pronta))
    custo_inicial = prepara_lista(melhor)
    print(custo_inicial)
    historico = [prepara_lista(melhor)]
    while temperatura > temperatura_final:
        for i in range(5):
            nova_solucao = nova_maquina()
            np.warnings.filterwarnings('ignore')
            nova_solucao_simplificada = list(simplifica(nova_solucao))
            custo_local = prepara_lista(nova_solucao_simplificada)
            melhor_custo = prepara_lista(melhor)
            probabilidade = np.random.uniform(0, 3)
            if custo_local - melhor_custo < 0  or probabilidade < np.log((melhor_custo-custo_local)/temperatura):
            	melhor = nova_solucao_simplificada
            	historico.append(melhor_custo)
            	print(temperatura,"trocou!!")
        
        if temperatura > temperatura/2:
        	temperatura = temperatura-10
        else:
        	temperatura = temperatura-5
        #print(temperatura)
    
    custo_final = prepara_lista(melhor)
    melhora = 100-((custo_final *100)/custo_inicial)
    
    return melhor, historico, melhora


temperatura = 1000
resultado, historico, melhora_da_solucao = simulated_annealing(temperatura)
for i in range(len(resultado)):
	print(resultado[i])
print(historico)
print("melhorou:",melhora_da_solucao,"%")
#plt.plot(historico)
#plt.plot(historico, hv(historico))
