import serial
import time
import re

# IDs que queremos ouvir
TARGET_IDS = {"D5B3A7", "D5B3A8", "D5B370"}

def setup_elm327(ser):
    commands = [
        "AT Z",        # Reset
        "AT E0",       # Echo off
        "AT L0",       # Linefeeds off
        "AT S0",       # Spaces off
        "AT H1",       # Headers on
        "AT CAF0",     # Automatic formatting off
        "AT CSM0",     # Single message mode off
        "AT SP 6",     # CAN 11 bits, 500kbps
        "AT MA"        # Monitor All
    ]
    for cmd in commands:
        ser.write((cmd + "\r").encode())
        time.sleep(0.2)
        while ser.in_waiting:
            try:
                line = ser.readline().decode(errors='ignore').strip()
                if line:
                    print("[Setup] " + line)
            except Exception as e:
                print(f"[Erro lendo setup]: {e}")

def parse_and_print(line):
    # Expressão para capturar ID e dados: ex: "D5B3A7 00 00 00 ..."
    print(line)

def main():
    data = None
    try:
        ser = serial.Serial('/dev/rfcomm0', 9600, timeout=1)
        time.sleep(2)
        setup_elm327(ser)

        print("\n🟢 Escutando os IDs desejados no barramento CAN...\n")
        buffer = ""
        while True:
            try:
                if bytes := ser.in_waiting:
                    print(len(bytes))
                    data = ser.read(bytes)

                if data:
                    buffer += data.decode(errors='ignore')
                    lines = buffer.split("\r")
                    buffer = lines.pop()  # a última pode estar incompleta
                    for line in lines:
                        parse_and_print(line.strip())
            except Exception as e:
                print(f"[Erro durante leitura]: {e}")
    except Exception as e:
        print(f"[Erro ao abrir porta]: {e}")
    finally:
        if 'ser' in locals():
            ser.close()

if __name__ == "__main__":
    main()
