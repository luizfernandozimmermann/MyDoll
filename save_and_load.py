import json
from platform import system

def salvar(conteudo, arquivo="saving"):
    sistema = system()
    if sistema == "Windows":
        with open("C:/Users/Luiz Fernando/Desktop/programacao/python/MyDoll2/" + arquivo + ".json", "w", encoding='UTF-8') as saving:
            json.dump(conteudo, saving)
    else:
        with open(arquivo + ".json", "w", encoding='UTF-8') as saving:
            json.dump(conteudo, saving)

def carregar(arquivo="saving"):
    sistema = system()
    if sistema == "Windows":
        with open("C:/Users/Luiz Fernando/Desktop/programacao/python/MyDoll2/" + arquivo + ".json", encoding='UTF-8') as loading:
            data = json.load(loading)
            return data
    else:
        with open(arquivo + ".json", encoding='UTF-8') as loading:
            data = json.load(loading)
            return data