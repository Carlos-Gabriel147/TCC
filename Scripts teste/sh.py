import serial
import time

# Configurações
porta = '/dev/rfcomm0'
baudrate = 9600

# Inicializa serial
ser = serial.Serial(porta, baudrate, timeout=1)
time.sleep(2)

# Função para enviar comando e ler resposta
def enviar_comando(cmd, espera=0.2):
    ser.write((cmd + '\r').encode())
    time.sleep(espera)
    resposta = ser.read_all().decode(errors='ignore').strip()
    print(f"> {cmd}")
    print(resposta)
    print('-' * 30)
    return resposta

# Inicialização do ELM327
comandos_iniciais = [
    'AT Z',     # Reset
    'AT E0',    # Eco off
    'AT L0',    # Linefeed off
    'AT S0',    # Printing spaces off
    'AT H1',    # Headers on
    'AT CAF0',  # Automatic formatting off
    'AT CFC0',  # Flow control off
    'AT SP 6',  # Set protocol to ISO 15765-4 (CAN 11-bit, 500 kbps)
]
for cmd in comandos_iniciais:
    enviar_comando(cmd, espera=0.3)

# Consulta dos dados
dados_para_ler = {
    'Acelerador': 'b3a7',
    'Freio':      'b3a8',
    'Volante':    'b370',
}

#14005159 (d5b3a7) - Posição do pedal Acelerador [PDC]
#14005160 (d5b3a8) - Posição do pedal do freio [PDC]
#14005104 (d5b370) - Posição do volante [EPS]

# Cabeçalho padrão do scanner (ajuste se necessário)
enviar_comando('AT SH 7E0')  # Header do scanner

for nome, pid in dados_para_ler.items():
    # Endereço de resposta (ajuste se souber o exato)
    # Assumindo que a resposta vem de 0x7E8, que é padrão. Se você sabe que é 0xD5Axxx, use:
    enviar_comando('AT CRA 5A' + pid)  # Espera resposta com esse endereço
    resposta = enviar_comando(f'22 {pid}')
    print(f'{nome} → {resposta}')
    time.sleep(0.5)

ser.close()
