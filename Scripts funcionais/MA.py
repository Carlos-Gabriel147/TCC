import serial
import time

ser = serial.Serial('/dev/rfcomm0', 9600, timeout=1)
time.sleep(1)

ser.write(b'AT Z\r'); time.sleep(1)
ser.write(b'AT E0\r'); time.sleep(0.1)
ser.write(b'AT L0\r'); time.sleep(0.1)
ser.write(b'AT S1\r'); time.sleep(0.1)
ser.write(b'AT H1\r'); time.sleep(0.1)
#ser.write(b'AT CAF0\r'); time.sleep(0.1)
#ser.write(b'AT CFC0\r'); time.sleep(0.1)
#ser.write(b'AT SP 6\r'); time.sleep(0.1)
#ser.write(b'AT CRA 7EX\r'); time.sleep(0.1)
ser.write(b'AT MA\r'); time.sleep(0.1)

print("Escutando...\n")

try:
    while True:
        #
        # ser.write(b'AT\r')
        time.sleep(1)
        #ser.write(b'AT MA\r')
        #linha = ser.read_until(b'\r').decode(errors='ignore').strip()
        #if linha:
        #print(linha)
        if bytes := ser.in_waiting:
            print(f"bytes: {bytes}")
            resp = ser.read(325)
            print(resp)

except KeyboardInterrupt:
    print("\nEncerrando...")
    ser.close()