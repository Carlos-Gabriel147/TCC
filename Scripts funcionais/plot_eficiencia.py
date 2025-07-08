import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Vetores de exemplo (devem ter mesmo tamanho)
ecu_sleep = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03]
id_sleep = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08]
sucessos  = [52.9, 84.3, 93.2, 97.2, 98.0, 99.5, 98.9, 97.9, 97.5, 99.3, 61.74, 85.2, 93.9, 97.1, 98.7, 100.0, 100.0, 99.5, 99.8, 100.0, 56.34, 86.2, 95.4, 97.2, 99.3, 99.9, 99.9, 100.0]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plotando os pontos
ax.scatter(ecu_sleep, id_sleep, sucessos, c='red', marker='o')

# Rótulos dos eixos
ax.set_xlabel('ecu_sleep')
ax.set_ylabel('id_sleep')
ax.set_zlabel('Total')

plt.title("Gráfico 3D de Pontos")
plt.show()
