import requests
import telepot
import json
import re
import http.client
import urllib #Para trabalhar com as URLs
from urllib.request import urlopen #Para trabalhar com as URLs
from xml.dom import minidom # Para trabalhar com o XML retornado pelos correios

# Conecta ao Bot    
bot = telepot.Bot("790055465:AAFFwJdBCJacLFgKIfEvmKAnaF2hg3ljc7E")

# Andamento da conversa
roteiro = 0

# Variaveis Globais - ViaCEP
estado = "GO"
cidade = "Goiânia"
logradouro = "SR S3"
CEP = "74785240"

# Variáveis Globais - Correios
origemCEP = "12345678"
destinoCEP = "12345678"
codigoServico = "12345"
peso = "1"
comprimento = "0"
altura = "0"
largura = "0"
diametro = "0"
codigoRastreio = "SW123456789BR"

# Calcula Frete
def calculaFrete(origemCEP, destinoCEP, codigoServico, peso, comprimento, altura, largura, diametro):
    # URL do WebService
    urlCorreios =  "http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx"
    
    # Campos para consulta de preço e prazo
    campos = [
            ('nCdEmpresa', ''),
            ('sDsSenha', ''),
            ('nCdServico', codigoServico),
            ('sCepOrigem', origemCEP),
            ('sCepDestino', destinoCEP),
            ('nVlPeso', peso),
            ('nCdFormato', "1"), # 1 significa que é uma caixa
            ('nVlComprimento', comprimento),
            ('nVlAltura', altura),
            ('nVlLargura', largura),
            ('nVlDiametro', diametro),
            ('sCdMaoPropria', "N"), # Não sei o significa, então não vamos usar
            ('nVlValorDeclarado', "0"), # Não vamos declarar valores
            ('sCdAvisoRecebimento', "N"), # Não vamos adicionar opção de AR
            ('StrRetorno', "xml"), # Informar ao correios pra retornar os dados em XML
        ]

    #Uusando o HTTPGET
    url = urlCorreios + "?" + urllib.parse.urlencode(campos)
    informacoes = minidom.parse(urlopen(url))

    #Analisando o HTTP POST 
    tagsResposta = ('Codigo',
                    'Valor',
                    'PrazoEntrega',
                    'ValorMaoPropria',
                    'ValorValorDeclarado',
                    'EntregaDomiciliar',
                    'EntregaSabado',
                    'Erro',
                    'MsgErro',
                    'ValorSemAdicionais',
                    'obsFim',
                    'DataMaxEntrega',
                    'HoraMaxEntrega')
    
    dados = {}
    for tagsResposta in tagsResposta:
        try:
            dados[tagsResposta] = informacoes.getElementsByTagName(tagsResposta)[0]
            dados[tagsResposta] = dados[tagsResposta].childNodes[0].data
        except:
            dados[tagsResposta] = ''

    return dados

# Trata as mensagens recebidas
def analizaMensagem(mensagem,data):
    global roteiro
    global estado
    global cidade
    global logradouro
    global CEP
    global origemCEP
    global destinoCEP
    global codigoServico
    global peso
    global comprimento
    global altura
    global largura
    global diametro

    if roteiro == 0:
        listaOI= ("OI","Oi","oi","ola","Ola","Olá","Hi","hi","Hey","hey","Ei","ei","Eai","eai","Eae","eae")
        for item in listaOI:
            if re.search(mensagem, item, re.IGNORECASE):
                bot.sendMessage(data['id'],"Olá, tudo bem?")          
                bot.sendMessage(data['id'],"Sou o Carteiro Virtual e estou a disposição para tirar algumas dúvidas " +
                "em relação a consulta de preço de frete e informar endereços referentes a CEPs...")
                bot.sendMessage(data['id'],"Se quiser saber como realizar a consulta de informações, basta digitar 'Ajuda'") 
                roteiro=0
                return True

        listaAjuda= ("AJUDA","ajuda","Ajuda")
        for item in listaAjuda:
            if re.search(mensagem, item, re.IGNORECASE):
                bot.sendMessage(data['id'],"No momento, esses são os serviços oferecidos:\n"+
                "- Consulta de endereço via CEP (Comando 'ENDEREÇO')\n"+
                
                "Obs: As informações consultadas são consumidas do webservice do ViaCEP\n"+
                "- Consulta de valor de envio (Comando 'CONSULTA')\n"+
                "[BREVE]- Consulta de encomenda (Comando 'RASTREIO')\n") 
                roteiro=0
                return True
        
        listaCEP= ("CEP","Cep","cep")
        for item in listaCEP:
            if re.search(mensagem, item, re.IGNORECASE):
                bot.sendMessage(data['id'],"Okay, para descobrir o CEP, vou precisar de algumas informações, digite as mensagens nesta ordem:\n"+
                "- UF (Siga do estado)\n"+
                "- Cidade\n"+
                "- Logradouro (Nome da rua, avenida, estrada, etc)\n"+
                "Exemplo: \nMensagem 1: GO\nMensagem 2: Goiania \nMensagem 3: SR 53") 
                bot.sendMessage(data['id'],"Muito bem, digite a sigla do Estado:")
                roteiro=20
                return True
        
        listaENDERECO= ("Endereço","endereço","ENDEREÇO","Endereco","endereco","ENDERECO")
        for item in listaENDERECO:
            if re.search(mensagem, item, re.IGNORECASE):
                bot.sendMessage(data['id'],"Okay, para descobrir o endereço, vou precisar do numero do CEP:\n"+
                "* Digite somente numeros, sem pontos ou traços"+
                "Exemplo: 74785240") 
                roteiro=10
                return True
        
        listaCONSULTA= ("Consulta","consulta","CONSULTA")
        for item in listaCONSULTA:
            if re.search(mensagem, item, re.IGNORECASE):
                bot.sendMessage(data['id'],"Okay, vou precisar de algumas informações para te passar um valor aproximado.\n"+
                "Por gentileza, digite o CEP de Origem:\n Obs: Digite somente numeros, sem pontos ou traços. \nExemplo: 74785240")

                #teste()
                #roteiro=0
                roteiro=30
                return True

        listaRASTREIO= ("Rastreio","rastreio","RASTREIO")
        for item in listaRASTREIO:
            if re.search(mensagem, item, re.IGNORECASE):
                bot.sendMessage(data['id'],"Okay, me informe o código de rastreio da encomenda:.\n"+
                "Exemplo: SW123456789BR, sempre numero de 13 digitos") 
                roteiro=40
                return True
    elif roteiro == 10:
        CEP = mensagem
        r = requests.get("https://viacep.com.br/ws/"+str(CEP)+"/json/")
        r.encoding
        data2 = r.json()
        print (data2)
        bot.sendMessage(data['id'],"O endereço encontrado foi "+str(data2['logradouro'])+" em  "+str(data2['bairro'])+
        " na cidade de "+data2['localidade']+" no estado de "+data2['uf'])
        roteiro = 0
    elif roteiro == 20:
        bot.sendMessage(data['id'],"Muito bem, digite o nome da cidade:")
        estado = mensagem
        roteiro = 21
    elif roteiro == 21:
        bot.sendMessage(data['id'],"Muito bem, digite o logradouro:")
        cidade = mensagem
        roteiro = 22
    elif roteiro == 22:
        logradouro = mensagem
        r = requests.get("https://viacep.com.br/ws/"+estado+"/"+cidade+"/"+logradouro+"/json/")
        data2 = r.json()
        bot.sendMessage(data['id'],"O CEP encontrado foi "+str(data2['cep'])+" em "+str(data2['bairro']))
        roteiro = 0
    elif roteiro == 30:
        origemCEP = mensagem
        bot.sendMessage(data['id'],"Muito bem, digite o CEP de destino:")
        roteiro = 31
    elif roteiro == 31:
        destinoCEP = mensagem
        bot.sendMessage(data['id'],"Digite o tipo de envio (SEDEX ou PAC):")
        roteiro = 32
    elif roteiro == 32:
        listaSEDEX= ("SEDEX","Sedex","sedex")
        for item in listaSEDEX:
            if re.search(mensagem, item, re.IGNORECASE):
                codigoServico = "40010"
                break
        listaPAC= ("PAC","Pac","pac")
        for item in listaPAC:
            if re.search(mensagem, item, re.IGNORECASE):
                codigoServico = "41106"
                break

        bot.sendMessage(data['id'],"Agora para o calculo do valor, precisa me informar o peso aproximado em quilogramas igorando o valor apos a virgula."+
        "\nExemplo: o pacote tem 2,1kg, então digite 2")
        roteiro = 33
    elif roteiro == 33:
        peso = mensagem
        bot.sendMessage(data['id'],"Agora digite em centrimetros o comprimento da caixa:\n"+
        "Exemplo: Uma caixa de 1,2metros tera 120 centimetros")
        roteiro = 34
    elif roteiro == 34:
        comprimento = mensagem
        bot.sendMessage(data['id'],"Agora digite em centrimetros a altura da caixa:")
        roteiro = 35
    elif roteiro == 35:
        altura = mensagem
        bot.sendMessage(data['id'],"Agora digite em centrimetros o largura da caixa:")
        roteiro = 36
    elif roteiro == 36:
        largura = mensagem
        bot.sendMessage(data['id'],"Só um momento...")
        dados = calculaFrete(origemCEP,destinoCEP,codigoServico,peso,comprimento,altura,largura,diametro)
        if codigoServico == "40010":
            bot.sendMessage(data['id'],"O valor do envio via SEDEX para "+destinoCEP+
            " custa "+dados['Valor']+" com um prazo de entrega de "+dados['PrazoEntrega']+" dias.")
        if codigoServico == "41106":
            bot.sendMessage(data['id'],"O valor do envio via PAC para "+destinoCEP+
            " custa "+dados['Valor']+" com um prazo de entrega de "+dados['PrazoEntrega']+" dias.")
        
        roteiro = 0
    elif roteiro == 40:
        codigoRastreio = mensagem
        #CODIGO QUE FAZ RASTREIO
        bot.sendMessage(data['id'],"RESULTADO:")
        roteiro = 0

# Verifica as mensagens recebidas
def recebendoMensagem(msg):
    data = msg['from']
    
    #Analiza as mensagens reecebidas, em vusca de informações
    analizaMensagem(msg['text'],data)
    
    print (data['username']+str(data['id'])+" enviou: "+msg['text'])

bot.message_loop(recebendoMensagem)

while True:
    pass


