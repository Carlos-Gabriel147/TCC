import obd
import time

# Força o protocolo: ISO 15765-4 CAN (11 bit ID, 500 kbaud)
protocol_id = '6'

# Conecta automaticamente na porta correta com protocolo forçado
connection = obd.OBD(portstr=None, baudrate=None, protocol=protocol_id, fast=False)

if connection.is_connected():
    print(f"Conectado com sucesso usando o protocolo {protocol_id}")

    # Lista de comandos de leitura OBD2
    commands = [
        obd.commands.SPEED,           # PID: 010D
        obd.commands.GET_DTC,         # PID: 03
        obd.commands.GET_CURRENT_DTC, # PID: 07
        obd.commands.VIN,             # PID: 0902
        obd.commands.ELM_VERSION,     # PID: ATI
        obd.commands.ELM_VOLTAGE,     # PID: ATRV
        obd.commands.PIDS_A,          # PID: 0100
        obd.commands.PIDS_9A,         # PID: 0900
        obd.commands.MIDS_A,          # PID: 0600
        obd.commands.MONITOR_O2_B1S3, # PID: 0603
        obd.commands.MONITOR_O2_B2S3  # PID: 0607
    ]

    try:
        while True:
            print("\nLeitura OBD2:")
            for cmd in commands:
                response = connection.query(cmd)
                print(f"{cmd.name} (PID: {cmd.command})")
                print(f"  Status: {response.status}")
                print(f"  Valor : {response.value}")
                print(f"  Raw   : {response.raw}\n")

            # Aguarda 1 segundo antes de nova leitura
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")

else:
    print(f"Não foi possível conectar usando o protocolo {protocol_id}")

# Fecha a conexão
connection.close()
