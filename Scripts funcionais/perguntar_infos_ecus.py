import serial
import time

PORTA = '/dev/rfcomm0'
BAUDRATE = 9600
ARQUIVO_SAIDA = 'perguntar_infos_ecus.txt'

ECUS = ['7C2', '7D4', '7D6', '7E0', '7E2', '7E3', '7E7', '7F1', '7F2']
PIDS = ['F193', 'F194', 'F195', 'F197', 'F1F0']

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

    print("[*] Testando ECUs e PIDs conhecidos... Pressione Ctrl+C para interromper.\n")

    with open(ARQUIVO_SAIDA, 'a') as f:
        try:
            for ecu in ECUS:
                enviar_comando(ser, f"AT SH {ecu}")
                print(f"\n[=] Comunicando com ECU {ecu}\n")

                f.write('\n')
                f.write(ecu)
                f.write('\n')

                for pid in PIDS:
                    comando = f"22 {pid}"
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
    print(f"[*] Conexão encerrada. Respostas salvas em '{ARQUIVO_SAIDA}'.")

if __name__ == "__main__":
    main()
