from woocommerce import API
from save_and_load import *
import os
from datetime import datetime

conteudo = carregar("woocommerce")
url = conteudo["url"]
consumer_key = conteudo["consumer_key"]
consumer_secret = conteudo["consumer_secret"]

wcapi = API(
    url = url,
    consumer_key = consumer_key,
    consumer_secret = consumer_secret,
    timeout=15
)

params = {
    'per_page': 100
}
contagem_chamadas = 0
produto = wcapi.get("products").json()

for produt in produto:

    print(produt)

while True:
    pass
conteudo = carregar()
colecoes = conteudo["colecoes_estoque"]
produtos = conteudo["produtos_estoque"]
subprodutos = conteudo["subprodutos_estoque"]
imagens_adicionais = conteudo["imagens_subprodutos_estoque"]

data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for colecao in colecoes:
    colecao["data_criacao"] = data
    colecao["data_edicao"] = data

for produto in produtos:
    produto["data_criacao"] = data
    produto["data_edicao"] = data

for subproduto in subprodutos:
    subproduto["data_criacao"] = data
    subproduto["data_edicao"] = data

for imagem in imagens_adicionais:
    imagem["data_criacao"] = data
    imagem["data_edicao"] = data

salvar(conteudo)
conteudo = carregar()
print(conteudo)


for colecao in colecoes:
    colecao["produtos"] = []

for produto in produtos:
    produto["subprodutos"] = []

for subproduto in subprodutos:
    subproduto["imagens_adicionais"] = []

for imagem in imagens_adicionais:
    subprodutos[imagem["id_subproduto"] - 1]["imagens_adicionais"].append(imagem)

for subproduto in subprodutos:
    produtos[subproduto["id_produto"] - 1]["subprodutos"].append(subproduto)

for produto in produtos:
    colecoes[produto["id_colecao"] - 1]["produtos"].append(produto)


import itertools


# Categorias
def pegar_categoria(nome_categoria):
    categorias = wc_categorias

    wc_categoria = None
    for categoria in categorias:
        if categoria["name"] == nome_categoria:
            wc_categoria = categoria
            break
    return wc_categoria
        

def criar_editar_categoria(conteudo_categoria):
    categoria = pegar_categoria(conteudo_categoria["name"])
    global contagem_chamadas 

    if categoria is None:
        resposta = wcapi.post("products/categories", conteudo_categoria).json()
        contagem_chamadas += 1
        return resposta["id"]
    
    else:
        if conteudo_categoria["name"] != categoria["name"] or \
        conteudo_categoria["description"] != categoria["description"] or \
        conteudo_categoria["image"] != categoria["image"]:
            resposta = wcapi.put(f"products/categories/{categoria['id']}", conteudo_categoria).json()
            contagem_chamadas += 1
            return resposta["id"]
    


def excluir_categoria(id=None, nome=None):
    if id is None:
        id = pegar_categoria(nome)["id"]

    wcapi.delete(f"products/categories/{id}", params={"force": True})
    global contagem_chamadas 
    contagem_chamadas += 1


# Produtos
def pegar_produto(nome_produto):
    produtos = wc_produtos

    for produto in produtos:
        if produto["name"] == nome_produto:
            return produto
    return None


def adicionar_editar_produto(conteudo_produto):
    produto = pegar_produto(conteudo_produto["name"])
    global contagem_chamadas

    if produto is None:
        wcapi.post("products", conteudo_produto)
        contagem_chamadas += 1

    else:
        variantes = wcapi.get(f"products/{produto['id']}/variations").json()
        """
        id
        name 
        option
        dentro de variantes[attributes]"""
        print()
        contagem_chamadas += 1
        if conteudo_produto["name"] != produto["name"] or \
        conteudo_produto["description"] != produto["description"] or \
        conteudo_produto["variations"] != variantes or \
        conteudo_produto["images"] != produto["images"] or \
        conteudo_produto["attributes"] != produto["attributes"]:
            wcapi.put(f"products/{produto}", conteudo_produto)
            contagem_chamadas += 1

            """
            
                variation_data["attributes"].append({
                    "id": attributes[i]["id"],
                    "name": atributos[0]["name"],
                    "option": attribute_combinations[indice][i]
                }"""


def excluir_produto(id=None, nome=None):
    if id is None:
        id = pegar_produto(nome)["id"]
    wcapi.delete(f"products/{id}")
    global contagem_chamadas 
    contagem_chamadas += 1


# imagens adicionais
def esvaziar_imagens_adicionais(id_produto=None, nome=None):
    if id_produto is None:
        id_produto = pegar_produto(nome)["id"]
    
    resposta = wcapi.get(f"products/{id_produto}/media", params=params)
    global contagem_chamadas 
    contagem_chamadas += 1
    resposta = resposta.json()

    for imagem in resposta:
        resposta = wcapi.delete(f"products/{id_produto}/media/{imagem['id']}")
        contagem_chamadas += 1


def adicionar_imagens_adicionais(imagens, nome_produto):
    id_produto = pegar_produto(nome_produto)["id"]

    for imagem in imagens:
        data = {
            "media_type": "image",
            "src": imagem
        }

        resposta = wcapi.post(f"products/{id_produto}/media", data)
        global contagem_chamadas 
        contagem_chamadas += 1


wc_categorias = wcapi.get("products/categories", params=params).json()
wc_produtos = wcapi.get("products", params=params).json()
contagem_chamadas += 2

for colecao in colecoes:
    if colecao["ativo"] == 0:
        for categoria in wc_categorias:
            if categoria["name"] == colecao["colecao"]:
                excluir_categoria(nome=categoria["name"])
                break
    else:
        imagem = colecao['imagem']
        imagem = os.path.basename(imagem)
        conteudo_categoria = {
                "name": colecao["colecao"],
                "description": colecao["descricao"],
                "image":
                {
                    "src": f"http://vidadeboneca.shop/wp-content/uploads/{imagem}"
                }
            }

        id_categoria = criar_editar_categoria(conteudo_categoria)

        for produto in colecao["produtos"]:
            nome_produto = colecao["colecao"] + " " + produto["produto"]
            if produto["ativo"] == 0:
                for wc_produto in wc_produtos:
                    if wc_produtos["name"] == nome_produto:
                        excluir_produto(nome=wc_produto["name"])
                        break

            else:
                imagem = produto['imagem']
                imagem = os.path.basename(imagem)

                variantes = []
                for subproduto in produto["subprodutos"]:
                    if subproduto["ativo"] == 1:
                        imagem = subproduto['imagem']
                        imagem = os.path.basename(imagem)
                        data = {
                            "regular_price": str(produto["preco"]), 
                            "attributes": [],
                            'manage_stock': True,
                            "stock_quantity": subproduto["quantidade"],
                            "image": {
                                "src": f"http://vidadeboneca.shop/wp-content/uploads/{imagem}"
                            }
                        }
                        variantes.append(data)
                
                conteudo_produto = {
                    "name": nome_produto,
                    "description": produto["descricao"],
                    "type": "variable",
                    "variations": variantes,
                    "reviews_allowed": False,
                    "images": [
                        {
                        "src": f"http://vidadeboneca.shop/wp-content/uploads/{imagem}"
                    }
                    ],
                    "categories": [
                        {
                            "id": id_categoria
                        }
                    ],
                    "attributes": [
                        {
                            "name": "Cor",
                            "options": list(map(lambda x: x["subproduto"], produto["subprodutos"])),
                            'visible': True, 
                            'variation': True
                        }
                    ]
                }

                adicionar_editar_produto(conteudo_produto)

                


print(contagem_chamadas)
