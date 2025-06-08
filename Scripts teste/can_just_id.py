import serial
import time
import re

# ========== CONFIGURAÇÕES ==========
SERIAL_PORT = "/dev/rfcomm0"
BAUDRATE = 9600

ID_INTERESSANTE = '14005159'  # ID que queremos monitorar
DESCRICAO = 'Acelerador'

# ========== FUNÇÕES ==========
def enviar_comando(ser, cmd, esperar=0.5):
    ser.write((cmd + '\r').encode())
    time.sleep(esperar)
    resposta = ser.read_all().decode(errors='ignore')
    print(f"> {cmd}\n{resposta.strip()}")
    return resposta

def configurar_elm(ser):
    enviar_comando(ser, 'ATZ')    # Reset
    enviar_comando(ser, 'ATE0')   # Echo off
    enviar_comando(ser, 'ATL0')   # Linefeeds off
    enviar_comando(ser, 'ATS0')   # Spaces off
    enviar_comando(ser, 'ATH1')   # Headers on
    enviar_comando(ser, 'ATSP6')  # CAN 500 kbps

    # Tenta configurar filtro
    resp = enviar_comando(ser, f'AT CRA {ID_INTERESSANTE}')
    if '?' in resp or 'ERROR' in resp:
        print("Filtro AT CRA não suportado. Filtro será feito no código.")
    else:
        print(f"Filtro AT CRA {ID_INTERESSANTE} configurado com sucesso.")

    enviar_comando(ser, 'ATMA')   # Monitor All

def processar_linha(linha):
    match = re.match(r'([0-9A-Fa-f]+)\s+\d+\s+(.*)', linha)
    if match:
        msg_id = match.group(1)
        dados = match.group(2).split()
        return msg_id, dados
    return None, None

# ========== PROGRAMA PRINCIPAL ==========
def main():
    print("Conectando ao ELM327...")
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=2)
    time.sleep(2)

    configurar_elm(ser)

    print(f"Monitorando ID: {ID_INTERESSANTE} ({DESCRICAO})... Pressione Ctrl+C para parar.")

    try:
        while True:
            linha = ser.readline().decode(errors='ignore').strip()
            if not linha:
                continue

            msg_id, dados = processar_linha(linha)

            if msg_id == ID_INTERESSANTE:
                print(f"ID: {msg_id} ({DESCRICAO}) | Dados: {dados}")

                if dados and len(dados) > 0:
                    try:
                        valor = int(dados[0], 16)
                        print(f"{DESCRICAO}: {valor}")
                    except ValueError:
                        print(f"{DESCRICAO}: dado inválido: {dados[0]}")
                else:
                    print(f"{DESCRICAO}: sem dados disponíveis.")

    except KeyboardInterrupt:
        print("\nEncerrando monitoramento...")
    finally:
        ser.close()

if __name__ == '__main__':
    main()
