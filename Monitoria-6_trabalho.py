# -*- coding: utf-8 -*-
"""
Monitoria 6 de Macroeconomia I (Parte 1) de 2024: Escolha de Trabalho

"""

# Importação de módulo necessários
import numpy as np
from math import log as log
import matplotlib.pyplot as plt


##############################################################################
""" Modelo de Crescimento Neoclássico com Escolha de Trabalho (sem Incerteza)

Diferente do modelo da Monitoria 4:
 • Usando "it" para nº de iterações (ao invés de "n")
 • Usando "n" para quantidade de trabalho
 • Usando "v_it" para lista de funções valor calculadas (ao invés de "vn")
 • Usando "gk_it" para lista de funções política (de capital) calculadas (ao invés de "vn")
 • Usando "gk" p/ cálculo da função política (de capital) em cada iteração (ao invés de "Tg")
"""

# Definição dos parâmetros
k_grid = np.array([0.04, 0.08, 0.12, .16, .2])
# k_grid = np.linspace(0.0001, 0.3, 101)
n_k = len(k_grid)
alpha = 0.3
beta = 0.6
delta = 0.3

# Novos parâmetros
phi = 1
z = 0  # Não há incerteza/choque de produtividade
n_grid = np.array([1/4, 2/4, 3/4, 1])
# n_grid = np.linspace(0, 1, 21)
n_n = len(n_grid)


# Criando lista de listas para incluir funções valor e políticas
# Note que, diferente do modelo sem incerteza, teremos uma função para cada z
v_it = [np.zeros(n_k)]
gk_it = [np.zeros(n_k)]
gn_it = [np.zeros(n_k)]  # Temos uma função política de trabalho agora


# Estabelecendo variáveis para realizar os loops
tol_norma = 1e-5  # Distância entre funções máxima para considerar convergência
norma = np.inf  # Valor apenas para entrar no loop
it = 0  # Nº iterações (antes utilizamos n - agora usado para trabalho)


while norma > tol_norma:
    it += 1  # Atualizando o número da iteração
        
    # Criando objetos para preencher com funções objetivo, valor e política
    f_obj = np.zeros((n_k, n_k, n_n))  # Lista com n_k matrizes n_k x n_n
    Tv = np.zeros(n_k)
    gn = np.zeros(n_k)
    gk = np.zeros(n_k)
    
    for i_k, k in enumerate(k_grid):
        for i_kk, kk in enumerate(k_grid):
            for i_n, n in enumerate(n_grid):
                # Ao invés de verificar kk < np.exp(z)*(k**alpha) +(1-delta)*k,
                # calculamos c e verificamos se c > 0
                c = np.exp(z)*(k**alpha * n**(1 - alpha)) + (1 - delta)*k - kk
                if c > 0:
                    f_obj[i_k, i_kk, i_n] = log(c) - (n**(1 + phi) / 1 + phi) + beta*v_it[it - 1][i_kk]
                else:
                    f_obj[i_k, i_kk, i_n] = -np.inf
            
        # Preenchida uma matriz, encontrar elemento que maximiza na matriz inteira
        # (após preencher uma matriz inteira)
        
        # // e % nos permite converter um índice único de uma matriz 2d de volta para os índices
        # 'corretos' de linha e coluna de uma matriz. 
        indice_max = np.argmax(f_obj[i_k])
        indice_gk = indice_max // n_n  # Divisão Inteira - Índice de k' (linha)
        indice_gn = indice_max % n_n  # Resto da Divisão - Índice de n (coluna)
        
        Tv[i_k] = np.max(f_obj[i_k])
        gk[i_k] = indice_gk
        gn[i_k] = indice_gn
            
    # Trocando índices de gk e gn por valores de k em k_grid e n em n_grid
    for p in range(n_k):
        gk[p] = k_grid[int(gk[p])]
        gn[p] = n_grid[int(gn[p])]   
    
    v_it.append(Tv)
    gk_it.append(gk)
    gn_it.append(gn)

    norma = np.max(abs(v_it[it] - v_it[it - 1]))
    print('A iteração {} terminou com norma igual a {:.5f}'.format(it,norma))


""" Visualização Gráfica da Função Política do Capital """
fig, ax = plt.subplots()

# Inclusão de cada função valor no gráfico
ax.plot(k_grid, gk_it[it], label='$g_k$: função política do capital')
ax.plot(k_grid, k_grid, '--', label='45 graus')


# Legendas
ax.set_xlabel('Capital')
ax.set_ylabel('Função Política')
ax.set_title('Função Política de k ')
ax.legend()

plt.show()


""" Visualização Gráfica da Função Política do Trabalho """
fig, ax = plt.subplots()

# Inclusão de cada função valor no gráfico
ax.plot(k_grid, gn_it[it], label='$g_n$: função política do trabalho')

# Legendas
ax.set_xlabel('Capital')
ax.set_ylabel('Função Política')
ax.set_title('Função Política')
ax.legend()

plt.show()


""" Cálculo do capital estacionário """
i_k = int(np.round(np.random.uniform(0, n_k - 1, size = 1), 0))  # aleatório
t = 0  # nº períodos, pode haver uma quebra na função que torna o loop infinito

# Achar índice do capital estacionário
while k_grid[i_k] != gk_it[it][i_k] and t < 100:  # até termos k = k'
    i_k = np.where(k_grid == gk_it[it][i_k])[0][0]  # Aplica o índice de k' em k
    t += 1

# Note que precisamos em gn, precisamos indicar a coluna i_z
print('O capital estacionário para z = {} é {:.3f}'.format(z, k_grid[i_k]))