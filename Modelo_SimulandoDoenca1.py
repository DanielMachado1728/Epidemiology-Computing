import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# Parâmetros do modelo
TAMANHO_GRADE = 50
TAXA_INFECCAO = 0.1
TEMPO_RECUPERACAO = 4
PASSOS_TEMPO = 100

# Estados: 0 = S (Suscetível), 1 = I (Infectado), 2 = R (Recuperado)
grade = np.zeros((TAMANHO_GRADE, TAMANHO_GRADE), dtype=int)
tempo_infeccao = np.zeros((TAMANHO_GRADE, TAMANHO_GRADE), dtype=int)

# Condição inicial: Um infectado no centro
centro = TAMANHO_GRADE // 2
grade[centro, centro] = 1
tempo_infeccao[centro, centro] = 1

# Função para atualizar a grade
def atualizar_grade():
    global grade, tempo_infeccao
    nova_grade = grade.copy()

    for i in range(TAMANHO_GRADE):
        for j in range(TAMANHO_GRADE):
            if grade[i, j] == 1:  # Se infectado
                if tempo_infeccao[i, j] >= TEMPO_RECUPERACAO:
                    nova_grade[i, j] = 2  # Recuperado
                else:
                    tempo_infeccao[i, j] += 1
            elif grade[i, j] == 0:  # Se suscetível
                vizinhos = grade[max(i-1, 0):min(i+2, TAMANHO_GRADE), max(j-1, 0):min(j+2, TAMANHO_GRADE)]
                if 1 in vizinhos and np.random.rand() < TAXA_INFECCAO:
                    nova_grade[i, j] = 1  # Infectado
                    tempo_infeccao[i, j] = 1

    grade = nova_grade

# Função para animação
def animar(passo):
    atualizar_grade()
    plt.clf()
    plt.imshow(grade, cmap='viridis', vmin=0, vmax=2)
    plt.title(f"Passo {passo}")
    plt.colorbar(label="Estado: 0=S, 1=I, 2=R")

# Criar animação
fig = plt.figure()
anim = FuncAnimation(fig, animar, frames=PASSOS_TEMPO, interval=200)

# Exibir a animação no Colab
HTML(anim.to_jshtml())
