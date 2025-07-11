import time
import serial
import threading

PORTA = 'COM4'
BAUDRATE = 9600
TIMEOUT = 1

CMD_INI_SLEEP = 0.1
ECU_SLEEP = 0.02
ID_SLEEP = 0.05

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


# Enviar comando na porta serial virtual com sleep definido
def enviar_comando_manual_sleep(ser, comando="ATI", sleep_time=0.1):
    ser.write(comando.encode())
    time.sleep(sleep_time)
    return ser.read_all().decode(errors='ignore').strip()


# Enviar comando na porta serial virtual com sleep "automatico" de espera de resposta
def enviar_comando_auto_sleep(ser, comando="ATI"):
    ser.write(comando.encode())
    while True:
        if ser.in_waiting >= 12:
            return ser.read_all().decode(errors='ignore').strip()
        else:
            time.sleep(0.0001)


# Filtrar resposta cagada do ELM
def filtrar_resposta(resp):
    resp = repr(resp)[1:-1]
    resp = sorted(resp.strip().split('\\r'), key=len, reverse=True)
    return next((s for s in resp if s.startswith('62')), None)


# Mapear os valores lidos em unidades reais
def mapear(ecu, carga):

    try:
        if ecu == "7E2":
            if not len(carga) == 8:
                return None
            
            return int(carga[-2:], 16)

        elif ecu == "783":
            if not len(carga) == 10:
                return None
        
            valor = int(carga[-4:], 16)
            return (valor - 65536)/10 if valor > 32768 else valor/10
        
    except:
        return None
    
    return None
                

# Thread de entendimento das respostas
def entender_respostas():

    while True:
        for sensor, up in update.items():

            if up:
                # Tenta filtrar uma resposta válida, se teve resposta válida, atualizar leitura
                resp = filtrar_resposta(entradas[sensor])

                if resp is not None:
                    resp = mapear(sensor[0:3], resp)

                    if resp is not None:
                        saidas[sensor] = resp

                else:
                    print("*Erro")
                    #pass

                # Envia último valores para o simulador, se um valor não foi válido, apenas irá repeti-lo
                update[sensor] = False
                print(saidas)
                #print(f"Acc: {saidas['7E2000B']}% \nFreio: {saidas['7E2000C']}% \nVolante: {saidas['7830003']}°\n")

                # enviar_para_simulador(saidas[sensor])


def main():

    # Porta COM virtual do bluetooth
    ser = iniciar_conexao(PORTA, BAUDRATE, TIMEOUT)

    # Comandos inicias de configurações
    for comando in comandos_iniciais:
        enviar_comando_manual_sleep(ser, comando, CMD_INI_SLEEP)

    # Instanciar thread
    th_entender_respostas = threading.Thread(target=entender_respostas, args=(), daemon=True)

    # Iniciar thread
    th_entender_respostas.start()

    try:
        while True:
            for ecu, ids in sensores.items():
                enviar_comando_auto_sleep(ser, "ATSH" + ecu + '\r')
                
                for id in ids:
                    entradas[ecu+id] = enviar_comando_auto_sleep(ser, "22" + id + '\r')
                    #entradas[ecu+id] = f"\rSTOPS\r22000C\r6200147{cont}\r<\r"
                    update[ecu+id] = True

    except KeyboardInterrupt:
        print("Encerrado")


if __name__ == "__main__":
    main()

    # contagem enviar comando auto: 1min 344
    # contagem enviar comando manual 1min: 402