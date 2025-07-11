import os
from collections import Counter

PASTA = r'logs_testes'
OUTPUT = r'Infos'

logs = os.listdir(PASTA)
print(f"Quantidade de logs: {len(logs)}")

ecu_sleeps = []
id_sleeps = []
sucessos = []
FPSs = []


output_path = os.path.join(OUTPUT, "calc_eficiencia.txt")

for log in logs:

    # print(f"Log: {log}")

    ecu_sleep = log[4:8]
    id_sleep = log[12:16]
    amostras = []

    # if id_sleep.endswith('.'):
    #     id_sleep = log[12:15] + '0'

    ecu_sleep = float(ecu_sleep)
    id_sleep = float(id_sleep)

    ecu_sleeps.append(ecu_sleep)
    id_sleeps.append(id_sleep)

    log_path = os.path.join(PASTA, log)

    cont = 0
    with open(log_path, 'r') as f:

        while cont < 20:
            f.readline()
            cont += 1

        while True:
            linha = f.readline()

            if not linha:
                break

            if linha[0] == 'F':
                FPS = linha[5:]
                FPSs.append(FPS)
                print(f"Log: {log}")

            else:
                amostras.append(int(linha.strip()))

    contagem = Counter(amostras)

    sucesso = 100*contagem[0]/len(amostras)
    falha = 100*contagem[1]/len(amostras)

    sucessos.append(sucesso)

    with open(output_path, 'a') as f:
        f.write(f"ecu_sleep = {ecu_sleep}, id_sleep = {id_sleep}\n")
        f.write(f"FPS: {FPS}\n")
        f.write(f"Perda: {falha:.2f}%\n")
        f.write(f"Sucesso: {sucesso:.2f}%\n\n")

with open(output_path, 'a') as f:
    f.write(f"ecu_sleeps: {ecu_sleeps}\n")
    f.write(f"id_sleeps: {id_sleeps}\n")
    f.write(f"FPSs: {FPSs}\n")
    f.write(f"Sucessos: {sucessos}")
