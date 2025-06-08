import obd
from obd import OBDCommand, Unit
from obd.protocols import ECU
import time

# Força o protocolo: ISO 15765-4 CAN (11 bit ID, 500 kbaud)
protocol_id = '2'

# Conecta automaticamente na porta correta com protocolo forçado
connection = obd.OBD(portstr=None, baudrate=None, protocol=protocol_id, fast=False)

if connection.is_connected():
    print(f"Conectado com sucesso usando o protocolo {protocol_id}")

    # Criando comandos básicos manualmente com OBDCommand
    commands = [
        OBDCommand("RPM", "Engine RPM", "01 0C", 2, decoder=obd.decoders.rpm),
        OBDCommand("SPEED", "Vehicle Speed", "01 0D", 1, decoder=obd.decoders.speed),
        OBDCommand("COOLANT_TEMP", "Engine Coolant Temperature", "01 05", 1, decoder=obd.decoders.temperature),
        OBDCommand("ENGINE_LOAD", "Calculated Engine Load", "01 04", 1, decoder=obd.decoders.percent),
        OBDCommand("THROTTLE_POS", "Throttle Position", "01 11", 1, decoder=obd.decoders.percent),
    ]

    try:
        while True:
            print("\nLeitura OBD2:")
            for cmd in commands:
                response = connection.query(cmd)
                print(f"{cmd.name}: {response.value}")

            # Aguarda 1 segundo antes de nova leitura
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")

else:
    print(f"Não foi possível conectar usando o protocolo {protocol_id}")

# Fecha a conexão
connection.close()

'''
Protocolos disponíveis na python-OBD:

"1": SAE_J1850_PWM
"2": SAE_J1850_VPW
"3": ISO_9141_2
"4": ISO_14230_4_5baud
"5": ISO_14230_4_fast
"6": ISO_15765_4_11bit_500k
"7": ISO_15765_4_29bit_500k
"8": ISO_15765_4_11bit_250k
"9": ISO_15765_4_29bit_250k
"A": SAE_J1939
'''
