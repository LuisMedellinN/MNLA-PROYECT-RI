import socket
import time

# Configuración del cliente
SERVIDOR = "192.168.0.49"  # Cambia a la IP de tu servidor
PUERTO = 5070              # Debe coincidir con el puerto del servidor

# Crear el socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Crear el mensaje INVITE
mensaje_invite = (
    "INVITE sip:lab1@{0}:{1} SIP/2.0\r\n"
    "Via: SIP/2.0/UDP {0}:{1};branch=z9hG4bK776asdhds\r\n"
    "Content-Length: 0\r\n\r\n"
).format(SERVIDOR, PUERTO)

# Enviar INVITE
print(f"Enviando INVITE al servidor {SERVIDOR}:{PUERTO}...")
cliente.sendto(mensaje_invite.encode(), (SERVIDOR, PUERTO))

# Esperar respuesta 200 OK
respuesta, _ = cliente.recvfrom(1024)
print("Respuesta del servidor al INVITE:")
print(respuesta.decode())

# Enviar ACK
mensaje_ack = (
    "ACK sip:lab1@{0}:{1} SIP/2.0\r\n"
    "Via: SIP/2.0/UDP {0}:{1};branch=z9hG4bK776asdhds\r\n"
    "Content-Length: 0\r\n\r\n"
).format(SERVIDOR, PUERTO)
print("Enviando ACK...")
cliente.sendto(mensaje_ack.encode(), (SERVIDOR, PUERTO))

# Simular la duración de la sesión
time.sleep(5)

# Enviar BYE
mensaje_bye = (
    "BYE sip:lab1@{0}:{1} SIP/2.0\r\n"
    "Via: SIP/2.0/UDP {0}:{1};branch=z9hG4bK776asdhds\r\n"
    "Content-Length: 0\r\n\r\n"
).format(SERVIDOR, PUERTO)
print("Enviando BYE...")
cliente.sendto(mensaje_bye.encode(), (SERVIDOR, PUERTO))

# Esperar respuesta 200 OK al BYE
respuesta, _ = cliente.recvfrom(1024)
print("Respuesta del servidor al BYE:")
print(respuesta.decode())

cliente.close()
