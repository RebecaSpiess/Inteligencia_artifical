from math import sqrt
import os
import csv

def busca_a_estrela (matriz, linhas, colunas, estado_inicial, estados_finais):
	distancia_meta = {}
	distancia_percorrida = {}
	heuristica = {}
	predecessores = {}
	estados_expandidos = []
	solucao_encontrada = False
	
	distancia_percorrida[estado_inicial] = 0
	distancia_meta[estado_inicial] = calcula_distancia_meta (estado_inicial, estados_finais) 
	heuristica[estado_inicial] = distancia_percorrida[estado_inicial] + distancia_meta[estado_inicial]
	predecessores[estado_inicial] = None
	nao_explorado = []
	nao_explorado.append(estado_inicial)
	iteracao = 1
	while len(nao_explorado) != 0:
		indice_mais_promissor = encontra_estado_mais_promissor(nao_explorado, heuristica)
		estado = nao_explorado.pop(indice_mais_promissor)
		if estado in estados_finais:
			solucao_encontrada = True
			break
		estados_sucessores = encontra_estados_sucessores(matriz, colunas, linhas, estado)
		estados_expandidos.append(estado)
		for i in range (0, len(estados_sucessores)):	
			sucessor = estados_sucessores[i]
			if sucessor not in estados_expandidos and sucessor not in nao_explorado:
				nao_explorado.append(sucessor)
				if sucessor not in heuristica.keys():
					distancia_meta[sucessor] = calcula_distancia_meta(sucessor, estados_finais)
					distancia_percorrida[sucessor] = distancia_percorrida[estado] + 1
					heuristica[sucessor] = distancia_meta[sucessor] + distancia_percorrida[sucessor]
					predecessores[sucessor] = estado
		iteracao = iteracao + 1

	if solucao_encontrada == True:
		apresenta_solucao (estado, predecessores, iteracao)
	else:
		print("Nao foi possivel encontrar uma solucao para o problema.")

def encontraPosicoes (matriz, linhas, colunas, valor):	
	posicoes = []
	for i in range(0, linhas):		
		for j in range(0, colunas):
			if int(matriz[i][j]) == valor:
				posicoes.append((i, j))
	return posicoes

def calcula_distancia_meta (estado, estados_finais):
	x = estado[0]
	y = estado[1]
	distancia_minima = 1000000000

	for estado_final in estados_finais:
		x_estado_final = estado_final[0]
		y_estado_final = estado_final[1]
		diff1 = x_estado_final - x
		diff2 = y_estado_final - y
		somaDiffs = pow(diff1, 2) + pow(diff2, 2)
		distancia_atual = sqrt(somaDiffs)
		if distancia_atual < distancia_minima:
			distancia_minima = distancia_atual
	return distancia_minima

def encontra_estado_mais_promissor (nao_explorado, heuristica_estados):
	valor_mais_promissor = 1000000000
	estado_mais_promissor = None
	indice_mais_promissor = 0
	indice = 0
	for estado in nao_explorado:
		if heuristica_estados[estado] < valor_mais_promissor:
			estado_mais_promissor = estado
			valor_mais_promissor = heuristica_estados[estado]
			indice_mais_promissor = indice
		indice = indice + 1
	return indice_mais_promissor

def encontra_estados_sucessores (matriz, linhas, colunas, posicao_atual):
	i = posicao_atual[0]
	j = posicao_atual[1]
	estados_sucessores = []
	if i > 0 and matriz[i-1][j] != 2: # Move para cima na matriz.
		estados_sucessores.append ((i-1, j))
	if i+1 < colunas and matriz[i+1][j] != 2: # Move para baixo na matriz.
		estados_sucessores.append ((i+1, j))
	if j > 0 and matriz[i][j-1] != 2: # Move para esquerda na matriz.
		estados_sucessores.append ((i, j-1))
	if j+1 < linhas and matriz[i][j+1] != 2: # Move para direita na matriz.
		estados_sucessores.append ((i, j+1))
	return estados_sucessores

def apresenta_solucao (estado, predecessores, iteracao):
	caminho = []
	caminho.append(estado)
	print("Solucao encontrada na iteracao " + str(iteracao) + ":")
	while predecessores[estado] != None:
		caminho.append(predecessores[estado])
		estado = predecessores[estado]		
	caminho = caminho[::-1]
	print(caminho)

if __name__ == "__main__":
	problema = open(r"C:\Users\spies\Documents\IA\Inteligencia_artifical\Matriz.csv") 
	leitor_problema = csv.reader(problema)
	entrada = list(leitor_problema)
	valores = entrada[0][0].split(";")
	linhas = int(valores[1]) # numero de linhas.
	colunas = int(valores[3]) # numero de colunas.
	matrizComPontoVirgula = entrada[1:] # mapa representado como matriz.
	
	idxLinha = 0
	matriz = [[0 for x in range(colunas)] for y in range(linhas)] 
	for linhasMatriz in range(0, len(matrizComPontoVirgula)):
		valoresIndividuais = matrizComPontoVirgula[linhasMatriz][0].split(";")
		for colunasMatriz in range(0, len(valoresIndividuais)):
			matriz[linhasMatriz][colunasMatriz] = int(valoresIndividuais[colunasMatriz])
		
	estado_inicial = encontraPosicoes (matriz, linhas, colunas, 0)
	estados_finais = encontraPosicoes (matriz, linhas, colunas, 3)
	
	print("Matriz (mapa): ")
	print(str(matriz))
	print("Estado Inicial: " + str(estado_inicial))
	print("Estado Final: " + str(estados_finais))
	busca_a_estrela (matriz, linhas, colunas, estado_inicial[0], estados_finais)

