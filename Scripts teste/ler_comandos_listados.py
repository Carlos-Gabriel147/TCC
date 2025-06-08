import obd
import time
import signal
import sys

# Conectar ao adaptador (mude se necessário para "/dev/ttyUSB0", etc.)
connection = obd.OBD("/dev/rfcomm0")

if not connection.is_connected():
    print("❌ Não foi possível conectar ao OBD2.")
    sys.exit(1)

# Função para lidar com Ctrl+C
def signal_handler(sig, frame):
    print("\n⏹️ Encerrando leitura OBD2...")
    connection.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Comandos ELM327 (respostas do adaptador, não do carro)
elm_commands = {
    "Versão do Adaptador": "ATI",
    "Voltagem da Bateria (ELM)": "ATRV"
}

# Comandos OBD-II seguros (somente leitura)
obd_commands = {
    "Velocidade (010D)": obd.commands.SPEED,
    "Códigos DTC Atuais (03)": obd.commands.GET_DTC,
    "Códigos DTC Pendentes (07)": obd.commands.GET_CURRENT_DTC,
    "PIDs suportados (0100)": obd.commands.PIDS_A,
    "PIDs suportados (0900)": obd.commands.PIDS_9A,
    "VIN do veículo (0902)": obd.commands.VIN,
    "Velocidade no DTC (020D)": obd.OBDCommand("DTC_SPEED", "DTC_SPEED", "020D", obd.OBDResponse, True),
    "Monitor O2 B1S3 (0603)": obd.OBDCommand("MONITOR_O2_B1S3", "MONITOR_O2_B1S3", "0603", obd.OBDResponse, True),
    "Monitor O2 B2S3 (0607)": obd.OBDCommand("MONITOR_O2_B2S3", "MONITOR_O2_B2S3", "0607", obd.OBDResponse, True),
    "Monitoramento disponível (0600)": obd.OBDCommand("MIDS_A", "MIDS_A", "0600", obd.OBDResponse, True),
}

# Mensagem inicial
print("📟 Lendo dados do adaptador e do veículo (pressione Ctrl+C para sair):\n")

while True:
    # ELM327
    for nome, comando in elm_commands.items():
        try:
            resposta = connection.interface.query(obd.OBDCommand(nome, nome, comando, obd.OBDResponse, True))
            if resposta.is_null():
                print(f"{nome:<35} ❌")
            else:
                print(f"{nome:<35} {resposta.value}")
        except Exception as e:
            print(f"{nome:<35} Erro: {e}")

    # OBD-II
    for nome, comando in obd_commands.items():
        try:
            resposta = connection.query(comando)
            if resposta.is_null():
                print(f"{nome:<35} ❌")
            else:
                print(f"{nome:<35} {resposta.value} (⏱ {resposta.time:.3f}s)")
        except Exception as e:
            print(f"{nome:<35} Erro: {e}")

    print("-" * 60)
    time.sleep(2)
