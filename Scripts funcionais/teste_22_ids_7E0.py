import serial
import time

PORTA = '/dev/rfcomm0'
BAUDRATE = 9600
ARQUIVO_SAIDA = 'testes_7E0_filtrado.txt'
ECU = '7E0'
REPS = 99999

# Lista de PIDs válidos (apenas os valores hexadecimais após "22 ")
PIDS_VALIDOS = [
    '0002', '0005', '0006', '0007', '0008', '0009', '000A', '000B', '000C', '000D', '000E', '000F',
    '0010', '0011', '0012', '0013', '0014', '0015', '0016', '0017', '0018', '0019', '001A', '001B',
    '001C', '001D', '001E', '001F', '0020', '0021', '0022', '0023', '0026', '0200', '0201', '0202',
    '0203', '0204', '0205', '0206', '0207', '0208', '0209', '020A', '020B', '020C', '020D', '020E',
    '020F', '0210', '0211', '0212', '0213', '0214', '0215', '0216', '0217', '0218', '0219', '021A',
    '021B', '021C', '021D', '021E', '021F', '0220', '0221', '0222', '0223', '0224', '0225', '0226',
    '0227', '0228', '0229', '022A', '022B', '022C', '022D', '022E', '022F', '0230', '0231', '0232',
    '0233', 'F190', 'F193', 'F194', 'F195', 'F197', 'F1F0'
]

#PIDS_VALIDOS = ['0012']

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

    with open(ARQUIVO_SAIDA, 'a') as f:
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
    print(f"[*] Conexão encerrada. Respostas salvas em '{ARQUIVO_SAIDA}'.")

if __name__ == "__main__":
    main()

