import time
import serial
import threading

PORTA = 'COM4'
BAUDRATE = 9600
TIMEOUT = 1

comandos_iniciais = [
        "AT Z",
        "AT E0",
        "AT S0",
        "AT H0",
        "AT L0", 
        "AT D",
        "AT D0",
        "AT M0",
        "AT SP 0",
        "AT AT 1",
        "AT AL",
        "AT ST 64"
        ]

sensores = {"7E2": ["000B", "000C"], "783": ["0003"]}
leituras = {"7E2000B": "", "7E2000C": "", "7830003": ""}
atualizacao = {"7E2000B": False, "7E2000C": False, "7830003": False}


# Conectar a porta com virtual do bluetooth
def iniciar_conexao(porta, baudrate, timeout):
    try:
        ser = serial.Serial(porta=porta, baudrate=baudrate, timeout=timeout)
        print(f"[+] Conectado à porta {porta} @ {baudrate} baud")
        return ser
    
    except serial.SerialException as e:
        print(f"[!] Erro ao abrir a porta serial: {e}")
        exit(1)


# Enviar comando na porta serial virtual
def enviar_comando(ser, comando="AT I", sleep_time=0.1):
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


# Thread de envio de comandos e leitura dos dados
def requisitar_dados(ser):

    global atualizacao

    while True:

        for ecu, ids in sensores.items():
            enviar_comando(ser, "ATSH" + ecu, 0.03)
            
            for id in ids:
                leituras[ecu+id] = enviar_comando(ser, "22" + id, 0.08)
                atualizacao[ecu+id] = True


# Thread de entendimento das respostas
def entender_respostas():

    while True:
        for sensor, update in atualizacao.items():
            if update:

                # Tenta filtrar uma resposta válida
                try:
                    resp = filtrar_resposta(leituras[sensor])

                    # Se teve resposta válida, atualizar leitura
                    if resp:
                        leituras[sensor] = resp

                # Envia último valores para o simulador, se um valor não foi válido, apenas irá repeti-lo
                finally:
                    # enviar_para_simulador(leituras[sensor]) Aqui envia a leituras[sensor] para o simulador do 
                    pass

        print(leituras)

def main():

    # Porta COM virtual do bluetooth
    ser = iniciar_conexao(PORTA, BAUDRATE, TIMEOUT)

    # Comandos inicias de configurações
    for comando in comandos_iniciais:
        enviar_comando(ser, comando, 0.1)

    # Instanciar threads
    th_requisitar_dados = threading.Thread(target=requisitar_dados, args=(ser), daemon=True)
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