import time
import serial
import threading

PORTA = 'COM4'
BAUDRATE = 9600
TIMEOUT = 1
DURACAO_ITS = 1020

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
rodada_finalizada = True

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
def requisitar_dados(ser, sleep_ecu, sleep_id):

    global rodada_finalizada

    cont = 0
    start_time = time.time()
    while True:
        for ecu, ids in sensores.items():
            enviar_comando(ser, "ATSH" + ecu, sleep_ecu)
            for id in ids:
                entradas[ecu+id] = enviar_comando(ser, "22" + id, sleep_id)
                #entradas[ecu+id] = f"\rSTOPS\r22000C\r6200147{cont}\r<\r"
                update[ecu+id] = True
                cont += 1
                if cont%100==0:
                    print(f"Amostra: {cont}")

        if cont >= DURACAO_ITS:
            rodada_finalizada = True

            with open("logs_testes/" + f"ecu_{sleep_ecu}_id_{sleep_id}.txt", "a") as f:
                f.write(f"FPS: {DURACAO_ITS/(time.time()-start_time):.2f}")

            break

                

# Thread de entendimento das respostas
def entender_respostas(sleep_ecu, sleep_id):

    with open("logs_testes/" + f"ecu_{sleep_ecu}_id_{sleep_id}.txt", "w") as f:
        while True:
            for sensor, up in update.items():

                if up:
                    #print(saidas)

                    # Tenta filtrar uma resposta válida, se teve resposta válida, atualizar leitura
                    try:
                        resp = filtrar_resposta(entradas[sensor])
                        if resp:
                            saidas[sensor] = resp
                            f.write("0\n")
                        else:
                            f.write("1\n")

                    # Envia último valores para o simulador, se um valor não foi válido, apenas irá repeti-lo
                    finally:
                        update[sensor] = False
                        f.flush()
                        #print(cont)

                        # print(f"Acc: {mapear('7E2', saidas['7E2000B'][-2:])}% \
                        #       \nFreio: {mapear( '7E2', saidas['7E2000C'][-2:])}% \
                        #       \nVolante: {mapear('783', saidas["7830003"][-4:])}°\n")
                    
                    # enviar_para_simulador(entradas[sensor])

            if rodada_finalizada:
                break


def main():

    global rodada_finalizada

    # # Porta COM virtual do bluetooth
    ser = iniciar_conexao(PORTA, BAUDRATE, TIMEOUT)

    print("Enviando comandos iniciais")
    # Comandos inicias de configurações
    for comando in comandos_iniciais:
        enviar_comando(ser, comando, 0.1)

    # Combinacoes de tempos
    combinacoes = []
    for sleep1 in [round(x * 0.01, 3) for x in range(2, 3)]:       # 0.01 to 0.05
        for sleep2 in [round(x * 0.01, 3) for x in range(7, 9)]:  # 0.01 to 0.1
            combinacoes.append((sleep1, sleep2))

    print(combinacoes)

    try:
        for sleep_ecu, sleep_id in combinacoes:

            while True:
                if rodada_finalizada:
                    print(f"-> Iniciando rodada ecu: {sleep_ecu}, id: {sleep_id}")
                    rodada_finalizada = False
                    th_requisitar_dados = threading.Thread(target=requisitar_dados, args=(ser, sleep_ecu, sleep_id,), daemon=True)
                    th_entender_respostas = threading.Thread(target=entender_respostas, args=(sleep_ecu, sleep_id), daemon=True)
                    th_requisitar_dados.start()
                    th_entender_respostas.start()
                    break
                else:
                    time.sleep(0.1)

    except KeyboardInterrupt:
        print("Encerrado")


if __name__ == "__main__":
    main()