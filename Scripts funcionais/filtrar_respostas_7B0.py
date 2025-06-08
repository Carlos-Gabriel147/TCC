input = r"respostas_7EB.txt"
output = r"filtro_7eb.txt"

debug = False

with open(input, 'r') as dados, open(output, 'w') as filtro:

    cont_janelas = 0
    cont_pos = 0
    cont_neg = 0
    tamanhos = []

    while True:
        linha = dados.readline()
        janela = []

        # Verificar se chegou no fim do arquivo, se não, retirar \n
        if linha == '':
            break
        else:
            linha = linha.strip()

        # Verifica se é o começo de uma janela
        if linha == '>':
            
            cont_janelas += 1

            # Ler a janela inteira
            while True:
                linha = dados.readline().strip()
                if linha == '': break
                janela.append(linha)

            # Retirar valores repetidos
            janela = sorted(set(janela))

            # Mostrar janelas fora do padrão
            if len(janela) != 2 and debug:
                print(janela)

            # Mostrar se teve algum comando diferente de 22
            if janela[0][0:2] != "22":
                print(f"Comando diferente de 22: {janela[0][0:2]}, janela {cont_janelas}")

            # Mostrar se teve alguma resposta diferente de 7EB
            if janela[1][0:3] != "7E8":
                print(f"Resposta diferente de 7E8: {janela[1][0:3]}")

            # Verificar se a resposta foi válida ou nao
            if janela[1][7:9] != "7F":
                cont_pos += 1

                filtro.write(janela[0])
                filtro.write(": ")

                for valores in janela[1:]:
                    filtro.write(valores)
                    if valores != janela[-1]:
                        filtro.write(", ")

                filtro.write('\n')

            else:
                cont_neg += 1

            # Salva o tamanho da janela
            tamanhos.append(len(janela))

    print(f"Quantidade de comandos: {cont_janelas}")
    print(f"Negativo: {cont_neg}")
    print(f"Positivo: {cont_pos}")
    print(f"Janelas de tamanho: {set(tamanhos)}")