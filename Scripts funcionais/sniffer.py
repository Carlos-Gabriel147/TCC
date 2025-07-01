import serial
import time

cell_port = serial.Serial('COM3', baudrate=9600, timeout=1)  # substitua pela porta real
elm_port = serial.Serial('COM4', baudrate=9600, timeout=1)

with open("log.txt", "w") as log:
    while True:
        if cell_port.in_waiting:
            data = cell_port.read(cell_port.in_waiting)
            print(data)
            log.write(f"[App]: {data}\n")
            elm_port.write(data)

        if elm_port.in_waiting:
            data = elm_port.read(elm_port.in_waiting)
            log.write(f"[ELM]: {data}\n")
            print(data)
            cell_port.write(data)

        time.sleep(0.01)