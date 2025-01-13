import socket

# Configuración del servidor
SERVER_IP = "192.168.0.49"  # IP del servidor
SERVER_PORT = 5070          # Puerto del servidor
BUFFER_SIZE = 1024          # Tamaño del buffer

# Crear socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
print(f"Servidor UDP activo en {SERVER_IP}:{SERVER_PORT}")

# Escuchar mensajes del cliente
while True:
    data, addr = server_socket.recvfrom(BUFFER_SIZE)
    print(f"Mensaje recibido de {addr}: {data.decode()}")

    # Enviar respuesta
    response = "ACK: " + data.decode()
    server_socket.sendto(response.encode(), addr)
