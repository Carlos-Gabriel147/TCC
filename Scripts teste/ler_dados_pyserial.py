import serial
import time
import signal
import sys

# Porta e baud rate do ELM327
PORTA = "/dev/rfcomm0"  # Altere conforme necessário (ex: COM3 no Windows)
BAUD = 9600  # Ou 38400, dependendo do adaptador

# Dicionário de comandos PID
comandos_obd = {
    "RPM": "010C",
    "Velocidade": "010D",
    "Temperatura Motor": "0105",
    "Carga do Motor": "0104",
    "Voltagem da Bateria": "0142",
    "Posição do Acelerador": "0111"
}

# Inicializa conexão serial
try:
    ser = serial.Serial(PORTA, BAUD, timeout=1)
except serial.SerialException:
    print("❌ Erro ao abrir a porta serial.")
    sys.exit(1)

def enviar_comando(cmd):
    """Envia um comando para o ELM327 e lê a resposta"""
    ser.write((cmd + "\r").encode())
    time.sleep(0.3)
    resposta = ser.read(ser.in_waiting or 128).decode(errors="ignore")
    return resposta.strip()

def inicializar_elm327():
    """Envia comandos de setup para o ELM327"""
    print("🔧 Inicializando ELM327...")
    for cmd in ["ATZ", "ATE0", "ATL0", "ATS0", "ATH0", "ATSP0"]:
        print(f"{cmd} → {enviar_comando(cmd)}")
    time.sleep(1)

def interpretar(pid, resposta):
    """Decodifica as respostas OBD2"""
    try:
        linhas = resposta.splitlines()
        dados = [l for l in linhas if l.startswith("41") or l.startswith("NO DATA")]

        if not dados:
            return None

        resposta_hex = dados[0].split()
        if len(resposta_hex) < 3:
            return None

        A = int(resposta_hex[2], 16)
        B = int(resposta_hex[3], 16) if len(resposta_hex) > 3 else 0

        if pid == "010C":  # RPM
            return ((A * 256) + B) / 4
        elif pid == "010D":  # Velocidade
            return A
        elif pid == "0105":  # Temperatura do motor
            return A - 40
        elif pid == "0104":  # Carga do motor
            return (A * 100) / 255
        elif pid == "0142":  # Voltagem do módulo
            return ((A * 256) + B) / 1000
        elif pid == "0111":  # Posição do acelerador
            return (A * 100) / 255
    except:
        return None

# Tratamento de Ctrl+C
def sair_graciosamente(sig, frame):
    print("\n⏹️ Encerrando leitura OBD2...")
    ser.close()
    sys.exit(0)

signal.signal(signal.SIGINT, sair_graciosamente)

# Inicializa ELM327
inicializar_elm327()

# Loop de leitura
print("\n📟 Lendo dados do veículo (pressione Ctrl+C para sair):\n")

while True:
    for nome, pid in comandos_obd.items():
        resposta = enviar_comando(pid)
        valor = interpretar(pid, resposta)
        if valor is None:
            print(f"{nome:<22} ❌")
        else:
            unidade = {
                "RPM": "RPM",
                "Velocidade": "km/h",
                "Temperatura Motor": "°C",
                "Carga do Motor": "%",
                "Voltagem da Bateria": "V",
                "Posição do Acelerador": "%"
            }[nome]
            print(f"{nome:<22} {valor:.2f} {unidade}")
    print("-" * 50)
    time.sleep(1)
