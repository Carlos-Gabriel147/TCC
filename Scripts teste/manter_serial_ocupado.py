import serial
import time

# Caminho da porta serial
serial_port = '/dev/rfcomm1'

try:
    # Abre a porta serial com configurações padrão
    ser = serial.Serial(serial_port, baudrate=9600, timeout=1)
    print(f"Porta {serial_port} aberta e ocupada.")

    # Mantém a porta aberta indefinidamente
    while True:
        time.sleep(1)  # Mantém o processo ativo

except serial.SerialException as e:
    print(f"Erro ao abrir a porta serial: {e}")

except KeyboardInterrupt:
    print("Encerrando script.")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print(f"Porta {serial_port} fechada.")
