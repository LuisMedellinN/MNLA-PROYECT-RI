import matplotlib.pyplot as plt

# Datos de comparación
categorias = ["Latencia", "Throughput"]
lte = [35, 500]  # Promedio de latencia (ms) y throughput (Mbps) en LTE
g5 = [5, 10000]  # Promedio de latencia (ms) y throughput (Mbps) en 5G
simulacion = [0.4, 15]  # Promedios de latencia (ms) y throughput (Mbps) en tu simulación

# Crear gráfico de barras
x = range(len(categorias))
plt.bar(x, lte, width=0.2, label="LTE", align='center')
plt.bar([i + 0.2 for i in x], g5, width=0.2, label="5G", align='center')
plt.bar([i + 0.4 for i in x], simulacion, width=0.2, label="Simulación", align='center', color='green')

# Etiquetas y formato
plt.xlabel("Métrica")
plt.ylabel("Valor (ms / Mbps)")
plt.title("Comparación de métricas")
plt.xticks([i + 0.2 for i in x], categorias)
plt.legend()

# Ajustar el eje Y para resaltar los valores más pequeños
plt.yscale("log")  # Cambia el eje Y a escala logarítmica
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# Mostrar el gráfico
plt.show()
