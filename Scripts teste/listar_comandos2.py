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
seen = set()  # Evita comandos duplicados

for attr in dir(obd.commands):
    try:
        cmd = getattr(obd.commands, attr)
        if isinstance(cmd, obd.OBDCommand) and cmd not in seen:
            seen.add(cmd)
            if connection.supports(cmd):
                try:
                    name = cmd.name or "Sem nome"
                except Exception:
                    name = "Erro no nome"

                try:
                    pid = cmd.command
                    pid = pid.decode() if isinstance(pid, bytes) else str(pid)
                except Exception:
                    pid = "???"

                try:
                    desc = cmd.desc or ""
                except Exception:
                    desc = ""

                supported.append((name, desc, pid))
    except Exception as e:
        # Ignora atributos quebrados
        continue

# Salva em TXT
p = Path("comandos_com_pid.txt").resolve()
with p.open("w", encoding="utf-8") as f:
    for name, desc, pid in supported:
        f.write(f"{name:<30} PID: {pid:<8} - {desc}\n")

print(f"✅ {len(supported)} comandos com PID encontrados.")
print(f"📄 Salvo em: {p}")

connection.close()
