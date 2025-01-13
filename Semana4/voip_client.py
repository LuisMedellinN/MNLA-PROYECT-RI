import socket
import time
import matplotlib.pyplot as plt

# Configuración del cliente VoIP (lab2)
CLIENT_IP = "192.168.0.48"
CLIENT_PORT = 5060

# Configuración del servidor VoIP (lab1)
SERVER_IP = "192.168.0.49"
SERVER_PORT = 5070

# Mensajes SIP
SIP_MESSAGES = {
    "INVITE": "INVITE sip:lab1 SIP/2.0",
    "200_OK": "SIP/2.0 200 OK",
    "ACK": "ACK sip:lab1 SIP/2.0",
    "BYE": "BYE sip:lab1 SIP/2.0",
}

# Métricas
total_messages = 0
lost_messages = 0
latencies = []

def calculate_mos(latency, packet_loss):
    """Calcula un índice de calidad MOS simplificado."""
    if latency > 400:
        return 1  # Calidad inaceptable
    elif latency > 200:
        return 2  # Calidad pobre
    elif packet_loss > 0.05:
        return 3  # Calidad aceptable
    elif latency > 100:
        return 4  # Buena calidad
    else:
        return 5  # Excelente calidad

def send_message(client, message, expect_response=True):
    """Envía un mensaje SIP y mide la latencia si se espera una respuesta."""
    global total_messages, lost_messages
    total_messages += 1

    start_time = time.time()
    client.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
    
    if not expect_response:
        return
    
    try:
        client.settimeout(2)  # Tiempo de espera de 2 segundos
        data, _ = client.recvfrom(1024)
        end_time = time.time()
        latencies.append((end_time - start_time) * 1000)  # RTT en ms
        print(f"[Cliente] Respuesta recibida: {data.decode()}")
    except socket.timeout:
        print("[Cliente] Paquete perdido.")
        lost_messages += 1

def generate_graphs(latencies, packet_loss, mos):
    """Genera gráficos para analizar QoS."""
    if len(latencies) == 0:
        print("No hay datos de latencia registrados para graficar.")
        return
    
    avg_latency = sum(latencies) / len(latencies)
    
    # Gráfico 1: Latencia por mensaje
    plt.figure()
    plt.plot(range(1, len(latencies) + 1), latencies, marker='o', label="Latencia por mensaje (ms)")
    plt.axhline(y=avg_latency, color='r', linestyle='--', label=f"Promedio: {avg_latency:.2f} ms")
    plt.title("Latencia por mensaje")
    plt.xlabel("Número de mensaje")
    plt.ylabel("Latencia (ms)")
    plt.xticks(range(1, len(latencies) + 1))  # Aseguramos que cada mensaje tenga un marcador en el eje x
    plt.legend()
    plt.grid()
    plt.savefig("latency_graph.png")
    plt.show()

    # Gráfico 2: Pérdida de paquetes
    plt.figure()
    plt.bar(["Mensajes enviados", "Mensajes perdidos"], [total_messages, lost_messages], color=["blue", "red"])
    plt.title("Pérdida de paquetes")
    plt.ylabel("Cantidad")
    plt.savefig("packet_loss_graph.png")
    plt.show()

    # Gráfico 3: Índice MOS
    plt.figure()
    plt.bar(["MOS"], [mos], color="green")
    plt.title("Calidad de Voz (MOS)")
    plt.ylabel("Puntuación")
    plt.ylim(0, 5)
    plt.savefig("mos_graph.png")
    plt.show()

    # Gráfico combinado (Latencia y MOS)
    plt.figure()
    plt.plot(range(1, len(latencies) + 1), latencies, marker='o', label="Latencia por mensaje (ms)")
    plt.axhline(y=avg_latency, color='r', linestyle='--', label=f"Latencia promedio: {avg_latency:.2f} ms")
    plt.bar(["MOS"], [mos], color="green", alpha=0.5, label=f"MOS: {mos}")
    plt.title("Análisis combinado de QoS")
    plt.xlabel("Mensajes / Métrica")
    plt.ylabel("Valores")
    plt.legend()
    plt.grid()
    plt.savefig("combined_qos_graph.png")
    plt.show()

def start_client():
    """Inicia el cliente VoIP para enviar mensajes SIP."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.bind((CLIENT_IP, CLIENT_PORT))
        print(f"[Cliente] Conectando desde {CLIENT_IP}:{CLIENT_PORT} a {SERVER_IP}:{SERVER_PORT}")
        
        # Enviar varios mensajes para tener más datos
        for i in range(5):  # Enviamos 5 INVITE para recolectar más latencias
            print(f"[Cliente] Enviando INVITE {i+1}...")
            send_message(client, SIP_MESSAGES["INVITE"])
        
        # Enviar ACK
        print("[Cliente] Enviando ACK...")
        send_message(client, SIP_MESSAGES["ACK"], expect_response=False)
        
        # Esperar 2 segundos antes de cerrar la conexión
        time.sleep(2)
        
        # Enviar BYE
        print("[Cliente] Enviando BYE...")
        send_message(client, SIP_MESSAGES["BYE"])
        
        # Resultados
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        packet_loss = lost_messages / total_messages
        mos = calculate_mos(avg_latency, packet_loss)
        
        print("\n--- Resultados ---")
        print(f"Latencia promedio: {avg_latency:.2f} ms")
        print(f"Pérdida de paquetes: {packet_loss:.2%}")
        print(f"Calidad de voz (MOS): {mos}/5")

        # Generar gráficos
        generate_graphs(latencies, packet_loss, mos)

if __name__ == "__main__":
    start_client()
