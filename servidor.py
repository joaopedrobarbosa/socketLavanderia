# -------------------
# Servidor Socket UDP
# -------------------

import socket
import datetime


def iniciarDados(operacoes):
    inicDic = {
        'codOperacao': '1',
        'nome': 'Alberto',
        'idLoja': 'ALoja',
        'dataVenda': '10/11/2022',
        'valorVenda': '1000'
    }
    operacoes.append(inicDic)
    inicDic = {
        'codOperacao': '1',
        'nome': 'Alberto',
        'idLoja': 'BLoja',
        'dataVenda': '22/03/2022',
        'valorVenda': '1500'
    }
    operacoes.append(inicDic)
    inicDic = {
        'codOperacao': '1',
        'nome': 'Alberto',
        'idLoja': 'CLoja',
        'dataVenda': '30/12/2021',
        'valorVenda': '300'
    }
    operacoes.append(inicDic)
    inicDic = {
        'codOperacao': '1',
        'nome': 'Marcelo',
        'idLoja': 'ALoja',
        'dataVenda': '13/05/2021',
        'valorVenda': '700'
    }
    operacoes.append(inicDic)
    inicDic = {
        'codOperacao': '1',
        'nome': 'Marcelo',
        'idLoja': 'BLoja',
        'dataVenda': '07/12/2021',
        'valorVenda': '400'
    }
    operacoes.append(inicDic)
    inicDic = {
        'codOperacao': '1',
        'nome': 'Marcelo',
        'idLoja': 'CLoja',
        'dataVenda': '21/02/2022',
        'valorVenda': '1000'
    }
    operacoes.append(inicDic)
    inicDic = {
        'codOperacao': '1',
        'nome': 'Danilo',
        'idLoja': 'ALoja',
        'dataVenda': '09/08/2022',
        'valorVenda': '1900'
    }
    operacoes.append(inicDic)
    inicDic = {
        'codOperacao': '1',
        'nome': 'Danilo',
        'idLoja': 'BLoja',
        'dataVenda': '14/11/2022',
        'valorVenda': '500'
    }
    operacoes.append(inicDic)
    inicDic = {
        'codOperacao': '1',
        'nome': 'Danilo',
        'idLoja': 'CLoja',
        'dataVenda': '19/03/2022',
        'valorVenda': '300'
    }
    operacoes.append(inicDic)


def totalVendasVendedor(operacoes, vendedorSolicitado):
    valor = 0
    verificaExistenciaVendedor = False
    for operacao in operacoes:
        if operacao.get("nome") == vendedorSolicitado:
            valor += float(operacao.get("valorVenda"))
            verificaExistenciaVendedor = True
    if verificaExistenciaVendedor:
        return str(valor)
    return "ERRO"


def totalVendasLoja(operacoes, lojaSolicitada):
    valor = 0
    verificaExistenciaLoja = False
    for operacao in operacoes:
        if operacao.get("idLoja") == lojaSolicitada:
            valor += float(operacao.get("valorVenda"))
            verificaExistenciaLoja = True
    if verificaExistenciaLoja:
        return str(valor)
    return "ERRO"


def totalVendasPeriodo(operacoes, periodoEmString):
    valor = 0
    try:
        data1 = datetime.date(int(periodoEmString[6:10]), int(
            periodoEmString[3:5]), int(periodoEmString[0:2]))
        data2 = datetime.date(int(periodoEmString[21:25]), int(
            periodoEmString[18:20]), int(periodoEmString[15:17]))
    except ValueError:
        return "ERRO"
    if data1 > data2:
        data1, data2 = data2, data1
    for operacao in operacoes:
        dataNova = datetime.date(int(operacao.get("dataVenda")[6:10]), int(
            operacao.get("dataVenda")[3:5]), int(operacao.get("dataVenda")[0:2]))
        if dataNova >= data1 and dataNova <= data2:
            valor += float(operacao.get("valorVenda"))
    return str(valor)


def melhorVendedor(operacoes):
    try:
        vendas = {}
        for operacao in operacoes:
            vendas[operacao['nome']] = vendas.get(
                operacao['nome'], 0) + float(operacao['valorVenda'])

        return str(max(vendas, key=vendas.get))

    except ValueError:
        return "ERRO"


def melhorLoja(operacoes):
    try:
        vendas = {}
        for operacao in operacoes:
            vendas[operacao['idLoja']] = vendas.get(
                operacao['idLoja'], 0) + float(operacao['valorVenda'])

        return str(max(vendas, key=vendas.get))

    except ValueError:
        return "ERRO"


# definindo ip e porta
HOST = '127.0.0.1'    # Substituir pelo endereco IP do Servidor
PORT = 9000

# criando o socket e associando ao endereço e porta
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind((HOST, PORT))

# servidor escutando (aguardando cliente)
print("Servidor aguardando clientes...")

operacoes = []
# Inicializando dados para fim de teste
iniciarDados(operacoes)
# conversando com o cliente
while (True):
    # recebendo dados uma tupla com mensagem e endereço
    msg, enderecoCliente = servidor.recvfrom(9000)
    print("Mensagem do cliente " + str(enderecoCliente))
    # transformando mensagem em dict
    mensagem = eval(msg.decode("utf-8"))
    print(mensagem)

    # Se for mensagem de Vendedor
    if mensagem.get("codOperacao") == "1":
        operacoes.append(mensagem)
        resposta = "OK"
    # Se for mensagem de Gerente
    elif mensagem.get("codOperacao") == "2":
        # APAGAR ESSE COMENTARIO DEPOIS QUE TODO MUNDO JÁ TIVER FEITO
        # Aqui entrarão os métodos para processamento de pedidos do gerente
        if (mensagem.get("tipoConsulta") == "1"):
            resposta = totalVendasVendedor(operacoes, mensagem.get("consulta"))
        elif (mensagem.get("tipoConsulta") == "2"):
            resposta = totalVendasLoja(operacoes, mensagem.get("consulta"))
        elif (mensagem.get("tipoConsulta") == "3"):
            resposta = totalVendasPeriodo(operacoes, mensagem.get("consulta"))
        elif (mensagem.get("tipoConsulta") == "4"):
            resposta = melhorVendedor(operacoes)
        elif (mensagem.get("tipoConsulta") == "5"):
            resposta = melhorLoja(operacoes)
        else:
            resposta = "ERRO"
    else:
        resposta = "ERRO"
    servidor.sendto(resposta.encode("utf-8"), enderecoCliente)

# mensagem de encerramento
print("Servidor encerrado.")
