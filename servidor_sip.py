from pjsip.simple import SIPServer

# Configuración del servidor SIP
def iniciar_servidor():
    # Crear una instancia del servidor SIP
    servidor = SIPServer(port=5070)  # Configura el puerto (ajusta si es necesario)

    # Iniciar el servidor
    servidor.start()
    print("Servidor SIP ejecutándose en el puerto 5070...")

    # Mantener el servidor corriendo
    try:
        while True:
            pass  # Reemplaza con lógica adicional si es necesario
    except KeyboardInterrupt:
        print("Apagando el servidor...")
        servidor.stop()

if __name__ == "__main__":
    iniciar_servidor()
