import serial
import time

PORTA = 'COM4'
BAUDRATE = 9600
SLEEP = 0.2

ini = ["AT Z", "AT E0", "AT D", "AT D0", "AT H1", "AT SP 0", "AT M0", "AT S0", "AT AT 1", "AT AL", "AT ST 64"]
sensores = {"7E2":["00B1", "00C1"], "783":["0031"]}

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
    time.sleep(SLEEP)
    resposta = ser.read_all().decode(errors='ignore')
    return resposta

def main():
    ser = iniciar_conexao(PORTA, BAUDRATE)

    print("Mandando comandos iniciais.")

    # Inicialização do ELM327
    for cmd in ini:
        enviar_comando(ser, cmd)

    print("Comandos iniciais finalizados.")

    for ecu, ids in sensores.items():
        enviar_comando(ser, "ATSH" + ecu)
        
        for id in ids:
            resp = enviar_comando(ser, "AT22" + id)
            print(resp)
    
if __name__ == "__main__":
    main()