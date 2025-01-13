import pandas as pd
from tabulate import tabulate

# Datos de comparación
data = {
    "Métrica": ["Latencia (ms)", "Throughput (Mbps)"],
    "LTE": ["20-50 ms", "100 Mbps - 1 Gbps"],
    "5G": ["1-10 ms", "Hasta 10 Gbps"],
    "Simulación": ["0.2-0.6 ms", "15 Mbps"]
}

# Crear la tabla con pandas
df = pd.DataFrame(data)

# Mostrar la tabla en formato tabulado
print("Tabla comparativa:")
print(tabulate(df, headers="keys", tablefmt="grid"))

# Exportar la tabla a un archivo CSV
df.to_csv("tabla_comparativa.csv", index=False)
print("\nTabla exportada a 'tabla_comparativa.csv'")
