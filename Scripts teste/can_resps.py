import serial
import time

SERIAL_PORT = "/dev/rfcomm0"  # ajuste
BAUDRATE = 9600 #38400
TIMEOUT = 1

comandos_leitura = [
    "ATRV",
    "ATDP",
    "ATDPN",
    "0000",
    "0012",
    "0013",
    "0111",
    "012F",
    "0131",
    "0146",
    "0142",
    "14005104",
]

def enviar_comando(ser, cmd, esperar=0.5):
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    ser.write((cmd + '\r').encode())
    time.sleep(esperar)
    resposta = b""
    while ser.in_waiting:
        resposta += ser.read(ser.in_waiting)
        time.sleep(0.1)
    return resposta.decode(errors='ignore').strip()

def configurar_elm(ser):
    comandos_config = [
        'ATZ',    # Reset
        'ATE0',   # Echo off
        'ATL0',   # Linefeeds off
        'ATS0',   # Spaces off
        'ATH1',   # Headers on
        'ATSP0',  # Automatic protocol
    ]
    for cmd in comandos_config:
        resp = enviar_comando(ser, cmd, esperar=1)
        print(f"{cmd} -> {resp}")

def main():
    print(f"Abrindo porta serial {SERIAL_PORT}...")
    with serial.Serial(SERIAL_PORT, BAUDRATE, timeout=TIMEOUT) as ser:
        time.sleep(2)

        print("\nConfigurando ELM327...")
        configurar_elm(ser)

        for cmd in comandos_leitura:
            print(f"\nEnviando comando: {cmd}")
            resposta = enviar_comando(ser, cmd)
            print(f"Resposta:\n{resposta if resposta else '(sem resposta)'}")

        print("\nLeitura finalizada.")

if __name__ == "__main__":
    main()
