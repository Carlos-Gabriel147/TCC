import serial
import time
import re
from collections import Counter

# ========== CONFIGURAÇÕES ==========
SERIAL_PORT = "/dev/rfcomm0"  # Ajuste conforme necessário
BAUDRATE = 9600
TEMPO_COLETA = 10  # segundos
SALVAR_ARQUIVO = True
NOME_ARQUIVO = "coleta_ids.txt"

# ========== FUNÇÕES ==========
def enviar_comando(ser, cmd, esperar=0.2):
    ser.write((cmd + '\r').encode())
    time.sleep(esperar)
    return ser.read_all().decode(errors='ignore')

def configurar_elm(ser):
    print(enviar_comando(ser, 'ATZ'))
    print(enviar_comando(ser, 'ATE0'))
    print(enviar_comando(ser, 'ATL0'))
    print(enviar_comando(ser, 'ATS0'))
    print(enviar_comando(ser, 'ATH1'))
    print(enviar_comando(ser, 'ATSP6'))
    print(enviar_comando(ser, 'ATMA'))

def processar_linha(linha):
    match = re.match(r'([0-9A-Fa-f]+)\s+\d+\s+(.*)', linha)
    if match:
        return match.group(1)
    return None

# ========== PROGRAMA PRINCIPAL ==========
def main():
    print("Conectando ao ELM327...")
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=2)
    time.sleep(2)
    configurar_elm(ser)

    print(f"Coletando mensagens CAN por {TEMPO_COLETA} segundos...")
    fim = time.time() + TEMPO_COLETA
    ids_coletados = []

    try:
        while time.time() < fim:
            linha = ser.readline().decode(errors='ignore').strip()
            if not linha:
                continue
            msg_id = processar_linha(linha)
            if msg_id:
                ids_coletados.append(msg_id)
    except KeyboardInterrupt:
        print("Interrompido pelo usuário.")
    finally:
        ser.close()

    contagem = Counter(ids_coletados)
    print("\nIDs mais frequentes:")
    for msg_id, count in contagem.most_common():
        print(f"ID: {msg_id} - {count} vezes")

    if SALVAR_ARQUIVO:
        with open(NOME_ARQUIVO, 'w') as f:
            for msg_id, count in contagem.most_common():
                f.write(f"{msg_id}: {count}\n")
        print(f"Resultados salvos em {NOME_ARQUIVO}")

if __name__ == '__main__':
    main()
