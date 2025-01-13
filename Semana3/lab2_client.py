import socket
import time
import csv

# Configuración del cliente
SERVER_IP = "192.168.0.49"  # IP del servidor
SERVER_PORT = 5070          # Puerto del servidor
BUFFER_SIZE = 1024          # Tamaño del buffer

# Crear socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Variables para métricas
results = []  # Almacena latencias de cada mensaje
total_bytes = 0
num_messages = 50  # Número total de mensajes

# Tiempo inicial para throughput
start_time = time.time()

for i in range(num_messages):
    # Crear el mensaje (tamaño ~1 KB)
    message = f"Mensaje {i+1} " + "-" * 1000
    total_bytes += len(message.encode())
    message_start_time = time.time()

    # Enviar mensaje
    client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))

    # Recibir respuesta
    data, addr = client_socket.recvfrom(BUFFER_SIZE)
    message_end_time = time.time()

    # Calcular latencia
    latency = (message_end_time - message_start_time) * 1000  # ms
    results.append({"Mensaje": i+1, "Latencia (ms)": latency})

    # Imprimir latencia en la consola
    print(f"Respuesta del servidor: {data.decode()} | Latencia: {latency:.2f} ms")

# Tiempo final para throughput
end_time = time.time()

# Calcular throughput
elapsed_time = end_time - start_time
throughput = (total_bytes / elapsed_time) / 1024  # KB/s
print(f"\nThroughput total: {throughput:.2f} KB/s")

# Guardar resultados en un archivo CSV
with open("resultados.csv", "w", newline="") as csvfile:
    fieldnames = ["Mensaje", "Latencia (ms)"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(results)

print("\nResultados exportados a 'resultados.csv'.")
client_socket.close()
