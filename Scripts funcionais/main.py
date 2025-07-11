import time
import serial
import threading

PORTA = 'COM4'
BAUDRATE = 9600
TIMEOUT = 1

ECU_SLEEP = 0.01 
ID_SLEEP = 0.06

comandos_iniciais = [
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

sensores = {"7E2": ["000B", "000C"], "783": ["0003"]}
entradas = {"7E2000B": "", "7E2000C": "", "7830003": ""}
saidas = {"7E2000B": "0", "7E2000C": "0", "7830003": "0"}
update = {"7E2000B": False, "7E2000C": False, "7830003": False}


# Conectar a porta com virtual do bluetooth
def iniciar_conexao(porta, baudrate, timeout):
    try:
        ser = serial.Serial(port=porta, baudrate=baudrate, timeout=timeout)
        print(f"[+] Conectado à porta {porta} @ {baudrate} baud")
        return ser
    
    except serial.SerialException as e:
        print(f"[!] Erro ao abrir a porta serial: {e}")
        exit(1)


# Enviar comando na porta serial virtual
def enviar_comando(ser, comando="ATI", sleep_time=0.1):
    if not comando.endswith('\r'):
        comando += '\r'
    ser.write(comando.encode())
    time.sleep(sleep_time)
    return ser.read_all().decode(errors='ignore').strip()


# Filtrar resposta cagada do ELM
def filtrar_resposta(resp):
    resp = repr(resp)[1:-1]
    resp = sorted(resp.strip().split('\\r'), key=len, reverse=True)
    return next((s for s in resp if s.startswith('62')), None)


# Mapear os valores lidos em unidades reais
def mapear(ecu, carga):

    if not carga:
        return carga

    try:
        valor = int(carga, 16)
    except ValueError:
        return carga

    if ecu == "7E2":
        return valor

    elif ecu == "783":
        return (valor - 65536)/10 if valor > 32768 else valor/10

    return carga


# Thread de envio de comandos e leitura dos dados
def requisitar_dados(ser):

    cont = 0
    while True:
        for ecu, ids in sensores.items():
            enviar_comando(ser, "ATSH" + ecu, ECU_SLEEP)
            
            for id in ids:
                entradas[ecu+id] = enviar_comando(ser, "22" + id, ID_SLEEP)
                #entradas[ecu+id] = f"\rSTOPS\r22000C\r6200147{cont}\r<\r"
                update[ecu+id] = True
                

# Thread de entendimento das respostas
def entender_respostas():

    while True:
        for sensor, up in update.items():

            if up:
                #print(saidas)

                # Tenta filtrar uma resposta válida, se teve resposta válida, atualizar leitura
                try:
                    resp = filtrar_resposta(entradas[sensor])
                    if resp:
                        saidas[sensor] = resp
                    else:
                        print(20*"=" + "> Erro <" + 20*"=")

                # Envia último valores para o simulador, se um valor não foi válido, apenas irá repeti-lo
                finally:
                    update[sensor] = False

                    print(f"Acc: {mapear('7E2', saidas['7E2000B'][-2:])}% \
                          \nFreio: {mapear( '7E2', saidas['7E2000C'][-2:])}% \
                          \nVolante: {mapear('783', saidas["7830003"][-4:])}°\n")
                    
                    # enviar_para_simulador(saidas[sensor])


def main():

    # # Porta COM virtual do bluetooth
    ser = iniciar_conexao(PORTA, BAUDRATE, TIMEOUT)

    # Comandos inicias de configurações
    for comando in comandos_iniciais:
        enviar_comando(ser, comando, 0.1)

    # Instanciar threads
    th_requisitar_dados = threading.Thread(target=requisitar_dados, args=(ser,), daemon=True)
    th_entender_respostas = threading.Thread(target=entender_respostas, args=(), daemon=True)

    # Iniciando as threads
    th_requisitar_dados.start()
    th_entender_respostas.start()

    try:
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Encerrado")


if __name__ == "__main__":
    main()