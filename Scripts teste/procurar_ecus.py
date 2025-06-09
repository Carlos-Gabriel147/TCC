import serial
import time

ARQUIVO_SAIDA = "procurar_ecus.txt"

# --- Testa todas as ECUs de 7E0 a 7EF ---
ecus_possiveis = [f"{i:03X}" for i in range(0x000, 0x800)]
ecus_possiveis = ecus_possiveis[::-1]

print("Qtd ECU's:", len(ecus_possiveis))
print("Testando:", ecus_possiveis)

def enviar_comando(ser, comando):
    if not comando.endswith('\r'):
        comando += '\r'
    ser.write(comando.encode())
    time.sleep(0.3)
    resposta = ser.read_all().decode(errors='ignore')
    return resposta

# --- Configura a conexão serial com o ELM327 ---
ser = serial.Serial('/dev/rfcomm0', 9800, timeout=1)  # Altere se necessário

# --- Inicialização do ELM327 ---
comandos_iniciais = [
    "AT Z",     # Reset
    "AT E0",    # Echo off
    "AT L0",    # Linefeed off
    "AT S1",    # Printing of spaces off
    "AT H1",    # Headers on (para ver o endereço de resposta)
    #"AT SP 6",  # Seleciona protocolo ISO 15765-4 (CAN 11bit 500kbps)
]

print("Inicializando ELM327...")
for cmd in comandos_iniciais:
    resposta = enviar_comando(ser, cmd)
    print(resposta)

print("\nProcurando ECUs que respondem ao VIN (22 F190)...\n")

with open(ARQUIVO_SAIDA, "w") as f:
    for ecu in ecus_possiveis:
        ecu = ecu.upper()
        enviar_comando(ser, f"AT SH {ecu}")  # Define o header de envio
        #for _ in range(3):
        resposta = enviar_comando(ser, "22 F190")
        print(ecu)
        print(resposta)
        print()

        f.write(ecu)
        f.write('\n')
        f.write(resposta)
        f.write('\n')

        f.flush()

ser.close()
