import serial
import time
import re

# ========== CONFIGURAÇÕES ==========
SERIAL_PORT = "/dev/rfcomm0"
BAUDRATE = 9600

IDS_INTERESSANTES = {
    '14005159': 'Acelerador',
    '14005160': 'Freio',
    '14005104': 'Volante'
}

# ========== FUNÇÕES ==========
def enviar_comando(ser, cmd, esperar=0.2):
    """Envia comando AT e lê resposta."""
    ser.write((cmd + '\r').encode())
    time.sleep(esperar)
    resposta = ser.read_all().decode(errors='ignore')
    return resposta

def configurar_elm(ser):
    """Configura ELM327 para modo monitor CAN."""
    print("Resetando ELM327...")
    print(enviar_comando(ser, 'ATZ'))
    print(enviar_comando(ser, 'ATE0'))   # Echo off
    print(enviar_comando(ser, 'ATL0'))   # Linefeeds off
    print(enviar_comando(ser, 'ATS0'))   # Spaces off
    print(enviar_comando(ser, 'ATH1'))   # Headers on
    print(enviar_comando(ser, 'ATSP6'))  # CAN 500kbps
    print(enviar_comando(ser, 'ATMA'))   # Monitor All

def processar_linha(linha):
    """Processa uma linha recebida do ELM."""
    match = re.match(r'^([0-9A-Fa-f]+)\s+\d+\s+((?:[0-9A-Fa-f]{2}\s*)+)$', linha)
    if match:
        msg_id = match.group(1)
        dados = match.group(2).strip().split()
        return msg_id, dados
    return None, None

# ========== PROGRAMA PRINCIPAL ==========
def main():
    print("Conectando ao ELM327...")
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    time.sleep(2)

    configurar_elm(ser)
    print("Escutando mensagens CAN... Pressione Ctrl+C para parar.")

    try:
        while True:
            linha = ser.readline().decode(errors='ignore').strip()
            if not linha or '>' in linha or 'ELM' in linha or 'OK' in linha:
                continue  # Ignora prompts e mensagens irrelevantes

            msg_id, dados = processar_linha(linha)
            if msg_id and msg_id in IDS_INTERESSANTES:
                print(f"ID: {msg_id} ({IDS_INTERESSANTES[msg_id]}) | Dados: {dados}")

                # Processamento específico
                try:
                    valor = int(dados[0], 16)
                    print(f"{IDS_INTERESSANTES[msg_id]}: {valor}")
                except (IndexError, ValueError):
                    print(f"Erro ao processar dados para {msg_id}: {dados}")

    except KeyboardInterrupt:
        print("\nEncerrando...")
    finally:
        ser.close()

# ========== EXECUÇÃO ==========
if __name__ == '__main__':
    main()
