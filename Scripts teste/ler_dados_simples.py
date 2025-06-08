import obd
import time
import signal
import sys

# Tenta conectar à porta OBD2 automaticamente (ou especifique: "/dev/ttyUSB0", "/dev/rfcomm0", etc.)
connection = obd.OBD()

if not connection.is_connected():
    print("❌ Não foi possível conectar ao OBD2.")
    sys.exit(1)

# Comandos básicos que você quer monitorar
commands = {
    "RPM": obd.commands.RPM,
    "Velocidade": obd.commands.SPEED,
    "Temperatura Motor": obd.commands.COOLANT_TEMP,
    "Carga do Motor": obd.commands.ENGINE_LOAD,
    "Voltagem da Bateria": obd.commands.CONTROL_MODULE_VOLTAGE,
    "Posição do Acelerador": obd.commands.THROTTLE_POS
}

# Função para lidar com Ctrl+C
def signal_handler(sig, frame):
    print("\n⏹️ Encerrando leitura OBD2...")
    connection.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Loop contínuo
print("📟 Lendo dados do veículo (pressione Ctrl+C para sair):\n")

while True:
    for nome, cmd in commands.items():
        resposta = connection.query(cmd)
        if resposta.is_null():
            print(f"{nome}: ❌")
        else:
            print(f"{nome:<22} {resposta.value:<10} (⏱ {resposta.time:.3f}s)")
    print("-" * 50)
    time.sleep(1)
