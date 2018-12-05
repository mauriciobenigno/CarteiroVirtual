import requests
import telepot
import json
import re


# Conecta ao Bot    
bot = telepot.Bot("790055465:AAFFwJdBCJacLFgKIfEvmKAnaF2hg3ljc7E")


# Variaveis Globais
roteiro = 0
estado = "GO"
cidade = "Goiânia"
logradouro = "SR S3"
CEP = "74785240"




# Trata as mensagens recebidas
def analizaMensagem(mensagem,data):
    global roteiro
    global estado
    global cidade
    global logradouro
    global CEP

    if roteiro == 10:
        print("TESTE - Resultado do endereço")
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
        data = r.json()
        text = json.loads(r)
        print (text)
        bot.sendMessage(data['id'],"O CEP encontrado foi "+str(data['cep'])+" em "+str(data['bairro']))
        roteiro = 0

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
            "- Consulta de endereço via CEP (Comando 'Endereço')\n"+
            "- Consulta de CEP via endereço (Comando 'CEP')\n"+
            "Obs: As informações consultadas são consumidas do webservice do ViaCEP") 
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
    for item in listaCEP:
        if re.search(mensagem, item, re.IGNORECASE):
            bot.sendMessage(data['id'],"Okay, para descobrir o endereço, vou precisar do numero do CEP:\n"+
            "* Digite somente numeros, sem pontos ou traços"+
            "Exemplo: 74785240") 
            roteiro=10
            return True

# Verifica as mensagens recebidas
def recebendoMensagem(msg):
    data = msg['from']
    
    #Analiza as mensagens reecebidas, em vusca de informações
    analizaMensagem(msg['text'],data)
    
    print (data['username']+str(data['id'])+" enviou: "+msg['text'])

    '''if pessoaExiste(data['id']) == True:
        analizaMensagem(msg['text'],pessoaPos(data['id']))
    else:
        pessoas.append(Pessoa(data['username'],data['id']))
        analizaMensagem(msg['text'],pessoaPos(data['id']))'''



bot.message_loop(recebendoMensagem)

while True:
    pass


