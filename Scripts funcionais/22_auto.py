'''
Script para perguntar todos os valores de 22 0000 até 22 FFFF para um única ECU específica
'''

import serial
import time

ECU = '7E0'

output = r'Coletas/' + ECU + '/' + 'bruto.txt'

PORTA = '/dev/rfcomm0'
BAUDRATE = 9600

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

    print("[*] Iniciando varredura de PIDs no formato '22 XXXX'... Pressione Ctrl+C para interromper.\n")

    with open(output, 'a') as f:
        try:
            for pid in range(0x0000, 0x10000):  # 0000 até FFFF
                pid_hex = f"{pid:04X}"
                comando = f"22 {pid_hex}"
                resp = enviar_comando(ser, comando)

                print(comando)
                print(resp)
                print()

                f.write(comando)
                f.write('\n')
                f.write(resp)
                f.write('\n')
                f.flush()

        except KeyboardInterrupt:
            print("\n[*] Varredura interrompida pelo usuário.")

    ser.close()
    print(f"[*] Conexão encerrada. Respostas salvas em '{output}'.")

if __name__ == "__main__":
    main()
