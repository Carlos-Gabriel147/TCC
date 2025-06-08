import obd
import time

# Força o protocolo: ISO 15765-4 CAN (11 bit ID, 500 kbaud)
protocol_id = '6'

# Conecta automaticamente na porta correta com protocolo forçado
connection = obd.OBD(portstr=None, baudrate=None, protocol=protocol_id, fast=False)

if connection.is_connected():
    print(f"Conectado com sucesso usando o protocolo {protocol_id}")

    # Lista de comandos básicos OBD2
    commands = [
        obd.commands.RPM,
        obd.commands.SPEED,
        obd.commands.COOLANT_TEMP,
        obd.commands.ENGINE_LOAD,
        obd.commands.THROTTLE_POS,
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

#ISO_15765_4_11bit_500k
#ISO_15765_4_29bit_500k
#ISO_15765_4_11bit_250k
#ISO_15765_4_29bit_250k
'''
"1": SAE_J1850_PWM,
"2": SAE_J1850_VPW,
"3": ISO_9141_2,
"4": ISO_14230_4_5baud,
"5": ISO_14230_4_fast,
"6": ISO_15765_4_11bit_500k,
"7": ISO_15765_4_29bit_500k,
"8": ISO_15765_4_11bit_250k,
"9": ISO_15765_4_29bit_250k,
"A": SAE_J1939,
'''