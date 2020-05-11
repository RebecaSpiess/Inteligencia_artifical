from math import sqrt

def encontraPosicoes (matriz, M, N, valor):
	posicoes = []
	for i in range(0, M):
		for j in range(0, N):
			if matriz[i][j] == valor:
				posicoes.append((i, j))
	return posicoes

def busca_a_estrela (matriz, M, N, estado_inicial, estados_finais):
	distancia_meta = {}
	distancia_percorrida = {}
	heuristica = {}
	predecessores = {}
	estados_expandidos = []
	solucao_encontrada = False
	

	# Inicializacao de distancia percorrida (f), distancia ate a meta (g) e heuristica (h = f+g).
	distancia_percorrida[estado_inicial] = 0
	distancia_meta[estado_inicial] = calcula_distancia_meta (estado_inicial, estados_finais) 
	heuristica[estado_inicial] = distancia_percorrida[estado_inicial] + distancia_meta[estado_inicial]
	predecessores[estado_inicial] = None
	#print 'Heuristica da Distancia no Estado Inicial: ' + str(heuristica[estado_inicial])
	franja = []
	franja.append(estado_inicial)
	iteracao = 1
	while len(franja) != 0:
		# mostra_valores_franja (franja, heuristica)
		indice_mais_promissor = encontra_estado_mais_promissor(franja, heuristica)
		estado = franja.pop(indice_mais_promissor)
		if estado in estados_finais:
			solucao_encontrada = True
			break
		estados_sucessores = encontra_estados_sucessores(matriz, M, N, estado)
		estados_expandidos.append(estado)
		for i in range (0, len(estados_sucessores)):	
			sucessor = estados_sucessores[i]
			if sucessor not in estados_expandidos and sucessor not in franja:
				franja.append(sucessor)
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

def encontra_estado_mais_promissor (franja, heuristica_estados):
	valor_mais_promissor = 1000000000
	estado_mais_promissor = None
	indice_mais_promissor = 0
	indice = 0
	for estado in franja:
		if heuristica_estados[estado] < valor_mais_promissor:
			estado_mais_promissor = estado
			valor_mais_promissor = heuristica_estados[estado]
			indice_mais_promissor = indice
		indice = indice + 1
	return indice_mais_promissor

def encontra_estados_sucessores (matriz, M, N, posicao_atual):
	i = posicao_atual[0]
	j = posicao_atual[1]
	estados_sucessores = []
	if i > 0 and matriz[i-1][j] != '2': # Move para cima na matriz.
		estados_sucessores.append ((i-1, j))
	if i+1 < M and matriz[i+1][j] != '2': # Move para baixo na matriz.
		estados_sucessores.append ((i+1, j))
	if j > 0 and matriz[i][j-1] != '2': # Move para esquerda na matriz.
		estados_sucessores.append ((i, j-1))
	if j+1 < N and matriz[i][j+1] != '2': # Move para direita na matriz.
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
	linhas = 4
	colunas = 5
	matriz = [[0 for x in range(colunas)] for y in range(linhas)] 
	matriz[0][0] = '3'
	matriz[0][1] = '1'
	matriz[0][2] = '2'
	matriz[0][3] = '1'
	matriz[0][4] = '0'

	matriz[1][0] = '1'
	matriz[1][1] = '1'
	matriz[1][2] = '2'
	matriz[1][3] = '1'
	matriz[1][4] = '1'
	
	matriz[2][0] = '1'
	matriz[2][1] = '2'
	matriz[2][2] = '2'
	matriz[2][3] = '2'
	matriz[2][4] = '1'
	
	matriz[3][0] = '1'
	matriz[3][1] = '1'
	matriz[3][2] = '1'
	matriz[3][3] = '1'
	matriz[3][4] = '1'

	

	estado_inicial = encontraPosicoes (matriz, linhas, colunas, '3')
	estados_finais = encontraPosicoes (matriz, linhas, colunas, '0')
	
	print("Matriz (mapa): ")
	print(str(matriz))
	print("Estado Inicial: " + str(estado_inicial))
	print("Estado Final: " + str(estados_finais))
	busca_a_estrela (matriz, linhas, colunas, estado_inicial[0], estados_finais)

