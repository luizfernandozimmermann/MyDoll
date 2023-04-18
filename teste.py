from save_and_load import *

conteudo = carregar()

for chave, valor in conteudo.items():
    conteudo[chave] = []
salvar(conteudo)


