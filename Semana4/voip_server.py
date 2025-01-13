import socket
import random

# Configuración del servidor VoIP (lab1)
SERVER_IP = "192.168.0.49"
SERVER_PORT = 5070

# Configuración de simulación
PACKET_LOSS_PROBABILITY = 0.1  # Probabilidad de pérdida de paquetes (10%)

# Mensajes SIP
SIP_MESSAGES = {
    "INVITE": "INVITE sip:lab1 SIP/2.0",
    "200_OK": "SIP/2.0 200 OK",
    "ACK": "ACK sip:lab1 SIP/2.0",
    "BYE": "BYE sip:lab1 SIP/2.0",
}

def simulate_packet_loss():
    """Simula pérdida de paquetes basada en la probabilidad."""
    return random.random() < PACKET_LOSS_PROBABILITY

def start_server():
    """Inicia el servidor VoIP para recibir mensajes SIP."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((SERVER_IP, SERVER_PORT))
        print(f"[Servidor] Escuchando en {SERVER_IP}:{SERVER_PORT}")
        
        while True:
            data, addr = server.recvfrom(1024)
            message = data.decode()
            print(f"[Servidor] Mensaje recibido: {message} desde {addr}")
            
            if simulate_packet_loss():
                print("[Servidor] Simulando pérdida de paquete...")
                continue
            
            if message == SIP_MESSAGES["INVITE"]:
                print("[Servidor] Respondiendo con 200 OK...")
                server.sendto(SIP_MESSAGES["200_OK"].encode(), addr)
            elif message == SIP_MESSAGES["ACK"]:
                print("[Servidor] Recibido ACK, conexión establecida.")
            elif message == SIP_MESSAGES["BYE"]:
                print("[Servidor] Recibido BYE, cerrando la conexión...")
                server.sendto(SIP_MESSAGES["200_OK"].encode(), addr)
                print("[Servidor] Conexión cerrada.")
                break

if __name__ == "__main__":
    start_server()
