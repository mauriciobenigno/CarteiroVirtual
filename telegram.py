import telepot
import json
import re

# Conecta ao Bot    
bot = telepot.Bot("790055465:AAFFwJdBCJacLFgKIfEvmKAnaF2hg3ljc7E")

# Trata as mensagens recebidas
def analizaMensagem(mensagem,data):
    listaOI= ("OI","Oi","oi","ola","Ola","Olá","Hi","hi","Hey","hey","Ei","ei","Eai","eai","Eae","eae")
    for item in listaOI:
        if re.search(mensagem, item, re.IGNORECASE):
            bot.sendMessage(data['id'],"Olá, tudo bem?")          
            bot.sendMessage(data['id'],"Sou o Carteiro Virtual e estou a disposição para tirar algumas dúvidas " +
            "em relação a consulta de preço de frete e informar endereços referentes a CEPs")
            roteiro=1
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


