import time
import serial
import threading

PORTA = 'COM4'
BAUDRATE = 9600
TIMEOUT = 1

ECU_SLEEP = 0.01
ID_SLEEP = 0.06

comandos_iniciais = ["AT Z", "AT E0", "AT D", "AT D0", "AT H0", "AT L0", "AT SP 0", "AT M0", "AT S0", "AT AT 1", "AT AL", "AT ST 64"]

sensores = {"7E2": ["000B", "000C"], "783": ["0003"]}
entradas = {"7E2000B": "", "7E2000C": "", "7830003": ""}
saidas = {"7E2000B": "0", "7E2000C": "0", "7830003": "0"}
update = {"7E2000B": False, "7E2000C": False, "7830003": False}

lock = threading.Lock()

def iniciar_conexao(porta, baudrate, timeout):
    try:
        ser = serial.Serial(port=porta, baudrate=baudrate, timeout=timeout)
        print(f"[+] Conectado à porta {porta}")
        return ser
    except serial.SerialException as e:
        print(f"[!] Erro: {e}")
        exit(1)

def enviar_comando(ser, comando, wait=0.05):
    if not comando.endswith('\r'):
        comando += '\r'
    ser.write(comando.encode())
    time.sleep(wait)
    resposta = ""
    t0 = time.time()
    while time.time() - t0 < 1:
        if ser.in_waiting:
            resposta += ser.read(ser.in_waiting).decode(errors='ignore')
        else:
            time.sleep(0.01)
    return resposta.strip()

def filtrar_resposta(resp):
    linhas = resp.replace('\r', '\n').split('\n')
    for linha in sorted(linhas, key=len, reverse=True):
        if linha.startswith('62'):
            return linha
    return None

def mapear(ecu, carga):
    try:
        valor = int(carga, 16)
    except ValueError:
        return carga
    if ecu == "7E2":
        return valor
    elif ecu == "783":
        return (valor - 65536)/10 if valor > 32768 else valor/10
    return carga

def requisitar_dados(ser):
    while True:
        for ecu, ids in sensores.items():
            enviar_comando(ser, "ATSH" + ecu, ECU_SLEEP)
            for id in ids:
                resp = enviar_comando(ser, "22" + id, ID_SLEEP)
                with lock:
                    entradas[ecu+id] = resp
                    update[ecu+id] = True

def entender_respostas():
    while True:
        with lock:
            for sensor, up in update.items():
                if up:
                    resp = filtrar_resposta(entradas[sensor])
                    if resp:
                        saidas[sensor] = resp
                    update[sensor] = False

        print(f"Acc: {mapear('7E2', saidas['7E2000B'][-2:])}% | "
              f"Freio: {mapear('7E2', saidas['7E2000C'][-2:])}% | "
              f"Volante: {mapear('783', saidas['7830003'][-4:])}°")
        time.sleep(0.1)

def main():
    ser = iniciar_conexao(PORTA, BAUDRATE, TIMEOUT)
    for cmd in comandos_iniciais:
        enviar_comando(ser, cmd, 0.1)

    threading.Thread(target=requisitar_dados, args=(ser,), daemon=True).start()
    threading.Thread(target=entender_respostas, daemon=True).start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nEncerrado")
        ser.close()

if __name__ == "__main__":
    main()
