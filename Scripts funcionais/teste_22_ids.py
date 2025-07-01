'''
Script para testar todos os IDs de uma ECU específica que deu resposta.
Verificar se esses valores variam se alterar os pedais ou volante.
'''

import serial
import time

ECU = '7E2'

input = r'Coletas/' + ECU + '/' + 'filtrado.txt'
output = r'Coletas/' + ECU + '/' + 'teste_todos.txt'

PORTA = 'COM4'
BAUDRATE = 9600
REPS = 200

PIDS_VALIDOS = []

def list_ids(input):
    pids = []

    with open(input, 'r') as file:
        while True:
            linha = file.readline()

            if linha:
                if linha[0] == '2':
                    pids.append(linha[3:7])
            else:
                break
    return pids

# Lista de PIDs válidos (apenas os valores hexadecimais após "22 ")
if not PIDS_VALIDOS:
    PIDS_VALIDOS = list_ids(input)
else:
    output = r'Coletas/' + ECU + '/' + 'teste_variam.txt'

print(PIDS_VALIDOS)
print()

def iniciar_conexao(porta, baudrate):
    try:
        ser = serial.Serial(porta, baudrate, timeout=1)
        print(f"[+] Conectado à porta {porta} @ {baudrate} baud")
        return ser
    except serial.SerialException as e:
        print(f"[!] Erro ao abrir a porta serial: {e}")
        exit(1)

def enviar_comando(ser, comando):
    if not comando.endswith('\r'):
        comando += '\r'
    ser.write(comando.encode())
    time.sleep(0.2)
    resposta = ser.read_all().decode(errors='ignore')
    return resposta

def main():
    ser = iniciar_conexao(PORTA, BAUDRATE)

    # Inicialização do ELM327
    enviar_comando(ser, "AT Z")
    enviar_comando(ser, "AT E0")
    enviar_comando(ser, "AT L1")
    enviar_comando(ser, "AT S1")
    enviar_comando(ser, "AT H1")
    enviar_comando(ser, "AT SH " + ECU)

    print("[*] Testando PIDs conhecidos por 70 vezes cada... Pressione Ctrl+C para interromper.\n")

    with open(output, 'a') as f:
        try:
            for pid in PIDS_VALIDOS:
                comando = f"22 {pid}"
                for i in range(REPS):
                    resp = enviar_comando(ser, comando)

                    print(comando)
                    print(resp)

                    f.write(comando)
                    f.write('\n')
                    f.write(resp)
                    f.write('\n')
                    f.flush()

        except KeyboardInterrupt:
            print("\n[*] Interrompido pelo usuário.")

    ser.close()
    print(f"[*] Conexão encerrada. Respostas salvas em '{output}'.")

if __name__ == "__main__":
    main()

