import obd
from pathlib import Path

# Conecta ao adaptador em uma porta específica
connection = obd.OBD("/dev/rfcomm0")  # ou "/dev/ttyUSB0"

if not connection.is_connected():
    print("❌ Não foi possível conectar ao adaptador OBD2.")
    quit()

# Lista comandos suportados com PID
supported = []

print("🔍 Coletando comandos suportados com PID...")
for attr in dir(obd.commands):
    cmd = getattr(obd.commands, attr)
    if isinstance(cmd, obd.OBDCommand):
        if connection.supports(cmd):
            raw_pid = cmd.command
            try:
                pid = raw_pid.decode() if isinstance(raw_pid, bytes) else str(raw_pid)
            except Exception:
                pid = str(raw_pid)
            desc = getattr(cmd, "description", "")
            supported.append((cmd.name, desc, pid))

# Salva em TXT
p = Path("comandos_com_pid.txt").resolve()
with p.open("w", encoding="utf-8") as f:
    for name, desc, pid in supported:
        f.write(f"{name:<25} PID: {pid:<5} - {desc}\n")

print(f"✅ {len(supported)} comandos com PID encontrados.")
print(f"📄 Salvo em: {p}")

connection.close()
