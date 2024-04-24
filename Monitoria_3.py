# -*- coding: utf-8 -*-
"""
Monitoria 3 de Macroeconomia I (Parte 1) de 2024
"""

# Importando os módulos necessários
import numpy as np  # NumPy com o "apelido" np
from math import log as log  # Apenas função log do módulo math

##############################################################################
""" Iterações até uma determinada distância entre funções valor """
# Incluiremos uma verificação para k' \in [0, f(k)] e criaremos uma função
# para retornar valor máximo e seu índice dentro do array


# Estabelecendo os parâmetros
k_grid = np.array([0.04, 0.08, 0.12, 0.16, 0.20])  # Possíveis valores de k e k'
# k_grid = np.linspace(0.001, 0.5, 201)
beta = 0.6
alpha = 0.3
delta = 1

n_k = len(k_grid)

# Criando lista de arrays de função valor e função política
v0 = np.zeros(n_k)
vn = [v0]
print(vn)

g0 = np.zeros(n_k)  # Não exite g0, é apenas para ocupar a posição 0
gn = [g0]
print(gn)


# Loop das iterações enquanto (while) é menor do que dada distância
tol_norma = 1e-5  # Tolerância de distância entre funções valor (0.00001)
norma = np.inf  # Valor inicial da norma = infinito
n = 0  # Contador de iterações

while norma > tol_norma: 
    # Aplicar a cada iteração Operador de Bellman em objetos genéricos Tv e Tg
    Tv = np.zeros(n_k)
    Tg = np.zeros(n_k)
    f_obj = np.zeros((n_k, n_k))
    n += 1
    
    for i in range(n_k):  # Loop de k (i é índice de k)
        for j in range(n_k):  # Loop de k (i é índice de k)
            if k_grid[j] >= 0 and k_grid[j] <= k_grid[i]**alpha + (1-delta)*k_grid[i]:
                f_obj[i,j] = log(k_grid[i]**alpha - k_grid[j]) + beta*vn[n-1][j]
            else:
                f_obj[i,j] = - np.inf
        Tv[i] = np.max(f_obj[i,:])
        Tg[i] = np.argmax(f_obj[i,:])
        
    # Quando acabar loop de linha, jogar função valor em vn e política em gn
    vn.append(Tv)
    gn.append(Tg)
    norma = max(abs(vn[n] - vn[n-1]))

np.round(vn, 2)  # Convergência da função valor
gn  # Convergência da funçao política (desconsiderar o primeira)
n  # Número de iterações realizadas
norma  # norma da última com a penúltima iteração


# Trocando índice em gn por valores de k'
for funcao in gn:
    for i in range(len(funcao)):
        funcao[i] = k_grid[int(funcao[i])]

gn[n]  # Função política da última iteração com valores de k'


# Visualização gráfica da convergência da função valor [Slide 8] 
import matplotlib.pyplot as plt  # Módulo para fazer gráficos
fig, ax = plt.subplots()

# Inclusão de cada função valor no gráfico
ax.plot(k_grid, vn[0], label='$v_0$')
ax.plot(k_grid, vn[1], label='$v_1$')
ax.plot(k_grid, vn[2], label='$v_2$')
ax.plot(k_grid, vn[4], label='$v_4$')
ax.plot(k_grid, vn[6], label='$v_6$')
ax.plot(k_grid, vn[8], label='$v_8$')
ax.plot(k_grid, vn[10], label='$v_{10}$')
ax.plot(k_grid, vn[15], label='$v_{15}$')
ax.plot(k_grid, vn[n], label='$v_{convergido}$')

# Legendas
ax.set_xlabel('Capital')
ax.set_ylabel('Função Valor')
ax.set_title('Convergência da Função Valor')
ax.legend()

plt.show()


# Visualização gráfica da convergência da função política [Slide 9] 
fig, ax = plt.subplots()

# Inclusão de cada função valor no gráfico
ax.plot(k_grid, gn[1], label='$g_1$')
ax.plot(k_grid, gn[2], label='$g_2$')
ax.plot(k_grid, gn[3], label='$g_5$')
ax.plot(k_grid, gn[10], label='$g_{10}$')
ax.plot(k_grid, gn[n], label='$g_{convergido}$')
ax.plot(k_grid, k_grid, '--', label='45 graus')

# Limites do gráfico
# ax.set_ylim([0, 0.15])  # tamanho mínimo e máximo vertical
# ax.set_xlim([0, 0.15])  # tamanho mínimo e máximo horizontal

# Legendas
ax.set_xlabel('Capital')
ax.set_ylabel('Função Política')
ax.set_title('Convergência da Função Política')
ax.legend()

plt.show()
