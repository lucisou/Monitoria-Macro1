# -*- coding: utf-8 -*-
"""
Exercício 1 item (f) da Lista 1 de Macroeconomia I (Parte 1) de 2024
"""

# Módulos a serem utilizados
import numpy as np
import matplotlib.pyplot as plt

beta_2 = 0.95  # valor de beta_2 fixado

# Criando e preenchendo matriz com beta_1 e t*
tabela = np.zeros([18, 2])  # criando matriz de zeros 18 x 2 para preenchimento

# do exercício sabemos qe c1_t + c2_t  = 2
# também temos que beta_1 < beta_2

# Loop para preenchimento de possíveis \beta_1 < \beta_2 e t* para c1_t - c2_t
# mudar de sinal (quando c2_t > 1, pois c2_t = 2 - c1_t, no equilíbrio)

for i in range(len(tabela)):
    tabela[i, 0] = beta_2 - (i + 1) * 0.05 # gerando beta_1 genérico menor que beta_2
    
    # Calcular consumo inicial do indivíduo 2 (c2_0)
    t = 0
    c2_t = - np.inf # um valor pequeno arbitrário para entrar no loop
    
    # condição while c1_t + c2_t = 2, logo, como temos que c1_t > c2_t, c2_t necessariamente precisa ser
    # menor que 1, logo, precisamos verificar no while se c2_t > 1 ou c1_t < 1
    while c2_t < 1:
        c2_t = 2 / (1 + ((1 - tabela[i,0]) / (1 - beta_2)) * (tabela[i,0] / beta_2) ** t)
        t += 1
    tabela[i, 1] = t - 1 # tem que ser t-1 pois o Python não atualiza
    # automaticamente o valor de c2_t

print(tabela)

# Poderia ter usado linspace() do NumPy para preencher a 1ª coluna de uma vez
exemplo = np.zeros((18, 2))
exemplo[:, 0] = np.linspace(0.05, 0.90, 18)
exemplo

# Criação do gráfico
fig, ax = plt.subplots()  # Cria a base (em branco) do gráfico
ax.plot(tabela[:, 0], tabela[:, 1],  # Coluna 0 no eixo x e coluna 1 no y
        '-o',  # Formato da linha e ponto do gráfico
        label='$t^*(\\beta_1, \\beta_2)$')  # Descrição da legenda
ax.legend()  # Faz aparecer a legenda
ax.set_ylim([0, 15])  # tamanho mínimo e máximo vertical
ax.set_xlim([0.00, 0.95])  # tamanho mínimo e máximo horizontal
ax.set_xlabel('$\\beta_1$')  # Descrição do eixo x
ax.set_ylabel('$t^*(\\beta_1, \\beta_2)$')  # Descrição do eixo y
ax.set_title('Gráfico de $t^*(\\beta_1, \\beta_2)$ por $\\beta_1$')  # Título
plt.show()  # Plot do gráfico com os comandos dados
