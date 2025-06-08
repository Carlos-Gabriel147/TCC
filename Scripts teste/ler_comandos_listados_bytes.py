import obd
import time
import signal
import sys
from obd.decoders import raw_string
from obd.OBDCommand import OBDCommand  # ou só use obd.commands padrão!

connection = obd.OBD()

if not connection.is_connected():
    print("❌ Não foi possível conectar ao OBD2.")
    sys.exit(1)

commands_raw = {
    "ELM_VERSION": "ATI",
    "ELM_VOLTAGE": "ATRV",
    "PIDS_A": "0100",
    "SPEED": "010D",
    "GET_DTC": "03",
    "GET_CURRENT_DTC": "07",
    "DTC_SPEED": "020D",
    "MIDS_A": "0600",
    "MONITOR_O2_B1S3": "0603",
    "MONITOR_O2_B2S3": "0607",
    "PIDS_9A": "0900",
    "VIN": "0902"
}

def signal_handler(sig, frame):
    print("\n⏹️ Encerrando leitura OBD2...")
    connection.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print("📟 Lendo dados do veículo (pressione Ctrl+C para sair):\n")

while True:
    for nome, pid in commands_raw.items():
        try:
            if pid.startswith("AT"):
                # Comandos AT
                resposta = connection.send(pid)
                if resposta.is_null():
                    print(f"{nome:<22} ❌ Resposta inválida")
                else:
                    print(f"{nome:<22} {resposta.value}")
            else:
                # Comandos PID
                cmd = OBDCommand(
                    name=nome,
                    desc=f"Consulta {nome}",
                    command=pid.encode('utf-8'),
                    _bytes=0,
                    decoder=raw_string
                )
                resposta = connection.query(cmd)

                if resposta.is_null():
                    print(f"{nome:<22} ❌ Resposta inválida")
                else:
                    print(f"{nome:<22} {resposta.value} (⏱ {resposta.time:.3f}s)")

        except Exception as e:
            print(f"{nome:<22} ❌ Erro: {e}")

    print("-" * 60)
    time.sleep(1)
