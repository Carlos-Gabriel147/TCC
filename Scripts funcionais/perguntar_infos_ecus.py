'''
Script que varia de 000 até 7FF para analisar a resposta de todas as ECU's possíveis do carro
analisando a resposta desses endereços para o comando 22 F190.
'''

import serial
import time

output = r'Coletas/ECUS/ECUS_perguntas_infos.txt'

PORTA = '/dev/rfcomm0'
BAUDRATE = 9600

PIDS = ['F193', 'F194', 'F195', 'F197', 'F1F0']

ECUS = [
    '7F2', '7F1', '7E7', '7E3', '7E2', '7E0', '7D6', '7D4', '7C2',
    '7B3', '7A7', '794', '783', '782', '762', '761', '760', '754',
    '741', '733', '726', '725', '723', '720', '711', '704', '68C',
    '68B', '68A', '689', '688', '687', '686', '685', '684', '683',
    '682', '681', '680', '67F', '67E', '67D', '67C', '67B', '67A',
    '679', '678', '677', '676', '675', '674', '673', '672', '671',
    '670', '66F', '66E', '66D', '66C', '66B', '66A', '669', '668',
    '667', '666', '665', '664', '663', '662', '661', '660', '65F',
    '65E', '65D', '65C', '65B', '65A', '659', '658', '657', '656',
    '655', '654', '653', '652', '651', '650', '64F', '64E', '64D',
    '64C', '64B', '64A', '649', '648', '647', '646', '645', '644',
    '643', '642', '641'
]

def iniciar_conexao(porta, baudrate):
    try:
        ser = serial.Serial(porta, baudrate, timeout=1)
        print(f"[+] Conectado à porta {porta} @ {baudrate} baud")
        return ser
    except serial.SerialException as e:
        print(f"[!] Erro ao abrir a porta serial: {e}")
        exit(1)

def enviar_comando(ser, comando):
    if not comando.endswith('\r'):
        comando += '\r'
    ser.write(comando.encode())
    time.sleep(0.2)
    resposta = ser.read_all().decode(errors='ignore')
    return resposta

def main():
    ser = iniciar_conexao(PORTA, BAUDRATE)

    # Inicialização do ELM327
    enviar_comando(ser, "AT Z")
    enviar_comando(ser, "AT E0")
    enviar_comando(ser, "AT L1")
    enviar_comando(ser, "AT S1")
    enviar_comando(ser, "AT H1")

    print("[*] Testando ECUs e PIDs conhecidos... Pressione Ctrl+C para interromper.\n")

    with open(output, 'a') as f:
        try:
            for ecu in ECUS:
                enviar_comando(ser, f"AT SH {ecu}")
                print(f"\n[=] Comunicando com ECU {ecu}\n")

                f.write('\n')
                f.write(ecu)
                f.write('\n')

                for pid in PIDS:
                    comando = f"22 {pid}"
                    resp = enviar_comando(ser, comando)

                    print(comando)
                    print(resp)

                    f.write(comando)
                    f.write('\n')
                    f.write(resp)
                    f.write('\n')
                    f.flush()

        except KeyboardInterrupt:
            print("\n[*] Interrompido pelo usuário.")

    ser.close()
    print(f"[*] Conexão encerrada. Respostas salvas em '{output}'.")

if __name__ == "__main__":
    main()
