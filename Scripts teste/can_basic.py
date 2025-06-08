import serial
import time

# ========== CONFIGURAÇÕES ==========
SERIAL_PORT = "/dev/rfcomm0"  # <-- Ajuste para sua porta serial
BAUDRATE = 9600

# ========== FUNÇÕES ==========
def enviar_comando(ser, cmd, esperar=0.3):
    """Envia comando AT e imprime resposta."""
    ser.write((cmd + '\r').encode())
    time.sleep(esperar)
    resposta = ser.read_all().decode(errors='ignore').strip()
    print(f"> {cmd}\n{resposta}")
    return resposta

def configurar_elm(ser):
    """Configura ELM327 para leitura básica."""
    enviar_comando(ser, 'ATZ')    # Reset
    enviar_comando(ser, 'ATE0')   # Echo off
    enviar_comando(ser, 'ATL0')   # Linefeeds off
    enviar_comando(ser, 'ATS0')   # Spaces off
    enviar_comando(ser, 'ATH1')   # Headers on
    enviar_comando(ser, 'ATSP6')  # CAN 500kbps (ajuste se necessário)

# ========== PROGRAMA PRINCIPAL ==========
def main():
    print("Conectando ao ELM327...")
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=2)
    time.sleep(2)  # Aguarda estabilização da conexão

    configurar_elm(ser)
    enviar_comando(ser, 'ATMA')  # Modo monitorar todas as mensagens CAN

    print("Lendo mensagens CAN... Pressione Ctrl+C para parar.")

    try:
        while True:
            linha = ser.readline().decode(errors='ignore').strip()
            if linha:
                print(f"CAN: {linha}")

    except KeyboardInterrupt:
        print("\nEncerrando leitura...")

    finally:
        ser.close()

# ========== EXECUÇÃO ==========
if __name__ == '__main__':
    main()
