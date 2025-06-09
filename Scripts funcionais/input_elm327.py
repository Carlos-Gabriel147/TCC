import serial
import time

# Modifique conforme a porta do seu ELM327 (ex: /dev/ttyUSB0 ou /dev/rfcomm0 para Bluetooth)
PORTA = '/dev/rfcomm0'
BAUDRATE = 9600  # 38400 ou 9600 são comuns, tente o que funcionar com seu adaptador

# AT CP 18
#14005159 (d5b3a7) - Posição do pedal Acelerador [PDC]
#14005160 (d5b3a8) - Posição do pedal do freio [PDC]
#14005104 (d5b370) - Posição do volante [EPS]

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
    return resposta.strip()

def main():
    ser = iniciar_conexao(PORTA, BAUDRATE)

    enviar_comando(ser, "AT Z")
    enviar_comando(ser, "AT E0")
    enviar_comando(ser, "AT L1")
    enviar_comando(ser, "AT S1")
    enviar_comando(ser, "AT H1")
    #enviar_comando(ser, "AT CP 01")
    enviar_comando(ser, "AT SP 7")
    #enviar_comando(ser, "AT MA")
    #enviar_comando(ser, "AT CAF0")
    #enviar_comando(ser, "AT CSM0")
    #enviar_comando(ser, "AT SH 7E0")

    print("\nDigite comandos para enviar ao ELM327 (ex: ATZ, ATI, 010C)")
    print("Digite 'exit' para sair.\n")

    while True:
        try:
            comando = input("Comando: ").strip()
            if comando.lower() == 'exit':
                break

            resposta = enviar_comando(ser, comando)
            print(resposta)

        except KeyboardInterrupt:
            break

    ser.close()
    print("[*] Conexão encerrada.")

if __name__ == "__main__":
    main()
