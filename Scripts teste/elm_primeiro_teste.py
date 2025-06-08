import serial
import time

ser = serial.Serial('/dev/rfcomm0', 9600, timeout=0.5)
time.sleep(2)

ser.write(b'AT Z\r'); time.sleep(1)
ser.write(b'AT E0\r'); time.sleep(0.2)  # Echo off
ser.write(b'AT L0\r'); time.sleep(0.2)  # Linefeed off
ser.write(b'AT S0\r'); time.sleep(0.2)  # Spaces off
ser.write(b'AT H1\r'); time.sleep(0.2)  # Headers on
ser.write(b'AT CAF0\r'); time.sleep(0.2)  # Auto formatting off
ser.write(b'AT CFC0\r'); time.sleep(0.2)  # Flow control off
#ser.write(b'AT SP 6\r'); time.sleep(0.2)  # ISO 15765-4 CAN (11/500)
#ser.write(b'AT TP B\r'); time.sleep(0.2)  # Força 29-bit CAN

print("Inicialização completa.\n")

ids_pids = [
    ('0D5A017', '22 0159'),  # Acelerador
    ('0D5A018', '22 0160'),  # Freio
    ('0D5A0D0', '22 0104'),  # Volante
]

for can_id, cmd in ids_pids:
    ser.write(f'AT SH {can_id}\r'.encode())
    time.sleep(0.2)

    ser.write((cmd + '\r').encode())
    time.sleep(0.3)

    print(f'\n→ Enviado para ID {can_id}: {cmd}')
    while True:
        linha = ser.readline().decode(errors='ignore').strip()
        print(f'Recebido: {linha}')
        #if '>' in linha:
        #    break

ser.close()
print("\nFinalizado.")
