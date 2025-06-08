import obd
import time
import signal
import sys

# Tenta conectar na porta do adaptador
connection = obd.OBD("/dev/rfcomm0")  # ou "/dev/ttyUSB0"

if not connection.is_connected():
    print("❌ Não foi possível conectar ao OBD2.")
    sys.exit(1)

# Comandos padrão da biblioteca
commands = [
    ("RPM",              obd.commands.RPM),
    ("Velocidade",       obd.commands.SPEED),
    ("Temperatura Motor",obd.commands.COOLANT_TEMP),
    ("Carga do Motor",   obd.commands.ENGINE_LOAD),
    ("Voltagem da ECU",  obd.commands.CONTROL_MODULE_VOLTAGE),
    ("Acelerador",       obd.commands.THROTTLE_POS),
]
print(commands)
exit()
# Ctrl+C para encerrar
def signal_handler(sig, frame):
    print("\n⏹️ Encerrando leitura OBD2...")
    connection.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print("📟 Lendo dados do veículo (pressione Ctrl+C para sair):\n")

# Loop principal
while True:
    for nome, cmd in commands:
        resposta = connection.query(cmd)
        if resposta.is_null():
            print(f"{nome}: ❌")
        else:
            print(f"{nome:<20} {resposta.value:<10} (⏱ {resposta.time:.3f}s)")
    print("-" * 50)
    time.sleep(1)
