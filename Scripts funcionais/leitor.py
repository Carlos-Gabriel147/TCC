import serial
import time

PORTA = 'COM4'
BAUDRATE = 9600

ini_cmds = [
        "AT Z",
        "AT E0",
        "AT D",
        "AT D0",
        "AT H0",
        "AT L0", 
        "AT SP 0",
        "AT M0",
        "AT S0",
        "AT AT 1",
        "AT AL",
        "AT ST 64"
        ]

sensores = {"7E2":["000B", "000C"], "783":["0003"]}


def iniciar_conexao(porta, baudrate):
    try:
        ser = serial.Serial(porta, baudrate, timeout=1)
        print(f"[+] Conectado à porta {porta} @ {baudrate} baud")
        return ser
    except serial.SerialException as e:
        print(f"[!] Erro ao abrir a porta serial: {e}")
        exit(1)


def enviar_comando(ser, comando, sleep_time=0.1):
    if not comando.endswith('\r'):
        comando += '\r'
    ser.write(comando.encode())
    time.sleep(sleep_time)
    return ser.read_all().decode(errors='ignore').strip()


def mapear(val, in_min, in_max, out_min, out_max):
    val = max(min(val, in_max), in_min)
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def filtrar_resposta(resp):
    resp = repr(resp)[1:-1]
    resp = sorted(resp.strip().split('\\r'), key=len, reverse=True)
    #print(resp)
            
    return next((s for s in resp if s.startswith('62')), -1)        



def main():
    ser = iniciar_conexao(PORTA, BAUDRATE)

    print("Mandando comandos iniciais.")

    # Inicialização do ELM327
    for cmd in ini_cmds:
        print(cmd)
        resp = enviar_comando(ser, cmd, 0.1)

    print("Iníco de coleta de dados:")

    while True:

        for ecu, ids in sensores.items():
            enviar_comando(ser, "ATSH" + ecu, 0.05)
            
            for id in ids:
                resp = enviar_comando(ser, "22" + id, 0.05)
                print("- ID: ", id)

                if ecu == "7E2":
                    #val = resp[-2:0]
                    print(filtrar_resposta(resp))
                    #print(int(val))
                    #print(mapear(val, ))

                elif ecu == "783":
                    #val = resp[-4:0]
                    print(filtrar_resposta(resp))
                    #print(int(val))
                    #print(mapear(val, ))

                print()
    
if __name__ == "__main__":
    main()