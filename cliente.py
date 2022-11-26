# ------------------
# Cliente Socket UDP
# ------------------

import socket


def validarData(data):
    try:
        ano = int(data[6:10])
        mes = int(data[3:5])
        dia = int(data[0:2])

        if mes < 1 or mes > 12:
            print("ERRO")
            return False
        if dia < 1 or dia > 31:
            print("ERRO")
            return False

        return True
    except ValueError:
        print("ERRO")
        return False


def validarValorVenda(valorVenda):
    try:
        numero = float(valorVenda)
        return True
    except ValueError:
        print("ERRO")
        return False


# Definindo ip e porta
HOST = '127.0.0.1'  # Endereco IP do Servidor
PORT = 9000              # Porta que o Servidor estará escutando

# Criando o socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define o endereco do servidor (Ip e porta)
enderecoServidor = (HOST, PORT)

print("Vou começar a mandar mensagens para o servidor.")

while (True):
    # Aqui começa a conversa
    codOperacao = input('''
		Escolha:
		1. Vendedor
		2. Gerente
		''')

    if codOperacao == '1':
        nome = input('Insira o nome do Vendedor: ')
        idLoja = input('Insira a identificação da loja: ')
        dataVenda = input('insira a data da venda (dd/mm/yyyy): ')
        if not validarData(dataVenda):
            continue
        valorVenda = input('Insira o valor da venda: ')
        if not validarValorVenda(valorVenda):
            continue

        mensagem = {
            'codOperacao': codOperacao,
            'nome': nome,
            'idLoja': idLoja,
            'dataVenda': dataVenda,
            'valorVenda': valorVenda
        }
    elif codOperacao == '2':
        consulta = ""
        tipoConsulta = input('''
		Escolha:
		1. Total de vendas de um vendedor 
		2. Total de vendas de uma loja
		3. Total de vendas da rede de lojas em um período 
		4. Melhor vendedor
		5. Melhor loja 
		''')

        if tipoConsulta == '1':
            consulta = input('Insira o nome do vendedor: ')
        elif tipoConsulta == '2':
            consulta = input('Insira o nome da loja: ')
        elif tipoConsulta == '3':
            consulta = input(
                'Insira o periodo da vendas no formato (dd/mm/yyyy até dd/mm/yyyy): ')
        elif tipoConsulta == '4':
            consulta = 4
        elif tipoConsulta == '5':
            consulta = 5

        mensagem = {
            'codOperacao': codOperacao,
            'tipoConsulta': tipoConsulta,
            'consulta': consulta
        }
    else:
        mensagem = {
            'codOperacao': codOperacao
        }
    # Enviando mensagem ao servidor
    print("... Mandando para o servidor")
    cliente.sendto(str(mensagem).encode("utf-8"), enderecoServidor)

    # Recebendo resposta do servidor
    msg, endereco = cliente.recvfrom(9000)
    resposta = msg.decode("utf-8")
    print("... O servidor respondeu:", resposta)

print("... Encerrando o cliente")
cliente.close()
