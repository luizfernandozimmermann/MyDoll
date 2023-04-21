from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from save_and_load import *


class Scroll_colecoes(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conteudo = App.get_running_app().conteudo
        self.atualizar()
        self.editando_colecao_id = 0
        self.colecao_selecionada = 0

    def excluir_colecao(self):
        self.conteudo = App.get_running_app().conteudo
        self.colecoes[self.editando_colecao_id - 1]["ativo"] = 0

        self.conteudo["colecoes_estoque"] = self.colecoes
        salvar(self.conteudo)
        self.atualizar()

    def editar_colecao(self, texto):
        self.conteudo = App.get_running_app().conteudo
        self.colecoes[self.editando_colecao_id - 1]["colecao"] = texto
        self.conteudo["colecoes_estoque"] = self.colecoes
        salvar(self.conteudo)
        self.atualizar()

    def preco_total(self):
        self.conteudo = App.get_running_app().conteudo
        produtos = self.conteudo["produtos_estoque"]
        subprodutos = self.conteudo["subprodutos_estoque"]

        preco_total = 0
        for produto in produtos:
            if produto["ativo"] == 1:
                for subproduto in subprodutos:
                    if subproduto["ativo"] == 1:
                        preco_total += produto["preco"] * subproduto["quantidade"]

        return preco_total

    def pesquisar(self, texto):
        self.conteudo = App.get_running_app().conteudo
        self.colecoes = self.conteudo["colecoes_estoque"]
        self.ordem = sorted(self.conteudo["colecoes_estoque"], key=lambda d: d['colecao'].lower()) 
        self.ordem.reverse()

        self.clear_widgets(self.children[1:])

        for colecao in self.ordem:
            if colecao["ativo"] == 1 and texto in colecao["colecao"]:
                self.add_widget(Caixa_colecao(text=colecao["colecao"], id_colecao=colecao["id"], width=self.width - self.padding[0] * 2), len(self.children))

    def adicionar_colecao(self, texto_colecao):
        self.conteudo = App.get_running_app().conteudo
        if len(self.colecoes) != 0:
            self.colecoes.append({"id": self.colecoes[-1]["id"] + 1, "colecao": texto_colecao, "ativo": 1})
        else:
            self.colecoes.append({"id": 1, "colecao": texto_colecao, "ativo": 1})

        self.conteudo["colecoes_estoque"] = self.colecoes
        salvar(self.conteudo)
        self.atualizar()

    def atualizar(self):
        self.conteudo = App.get_running_app().conteudo
        self.colecoes = self.conteudo["colecoes_estoque"]
        self.ordem = sorted(self.conteudo["colecoes_estoque"], key=lambda d: d['colecao'].lower()) 
        self.ordem.reverse()
        
        self.clear_widgets(self.children[1:])
        
        for colecao in self.ordem:
            if colecao["ativo"] == 1:
                self.add_widget(Caixa_colecao(text=colecao["colecao"], id_colecao=colecao["id"], width=self.width - self.padding[0] * 2), len(self.children))

class Caixa_colecao(Button):
    def __init__(self, id_colecao, **kwargs):
        super().__init__(**kwargs)
        self.id_colecao = id_colecao
        self.size_hint_y = None
        self.width = self.width


class Scroll_produtos(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conteudo = App.get_running_app().conteudo
        self.colecao_selecionada = 0
        self.produto_selecionado = 0
        self.atualizar()
        self.editando_produto_id = 0

    def pesquisar(self, texto):
        self.conteudo = App.get_running_app().conteudo
        self.produtos = self.conteudo["produtos_estoque"]
        self.ordem = sorted(self.conteudo["produtos_estoque"], key=lambda d: d['preco']) 
        self.ordem.reverse()

        self.clear_widgets(self.children[1:])

        for produto in self.ordem:
            if produto["ativo"] == 1 and texto in produto["produto"] and produto["id_colecao"] == self.colecao_selecionada:
                preco_formatado = 'R$' + '{:,.2f}'.format(produto['preco'])
                texto = f"{produto['produto']}\n{preco_formatado}"
                self.add_widget(Caixa_produto(text=texto, id_produto=produto["id"], imagem=produto["imagem"]), len(self.children))

    def excluir_produto(self):
        self.conteudo = App.get_running_app().conteudo
        self.produtos[self.editando_produto_id - 1]["ativo"] = 0

        self.conteudo["produtos_estoque"] = self.produtos
        salvar(self.conteudo)
        self.atualizar()

    def editar_produto(self, imagem_produto, nome_produto, preco_produto):
        self.conteudo = App.get_running_app().conteudo
        dic = {
            "id": self.editando_produto_id,
            "id_colecao": self.colecao_selecionada,
            "imagem": imagem_produto,
            "produto": nome_produto,
            "preco": float(preco_produto),
            "ativo": 1
        }
        self.produtos[self.editando_produto_id - 1] = dic
        self.conteudo["produtos_estoque"] = self.produtos
        salvar(self.conteudo)
        self.atualizar()

    def adicionar_produto(self, imagem_produto, nome_produto, preco_produto):
        self.conteudo = App.get_running_app().conteudo
        id_produto = len(self.produtos) + 1

        dic = {
            "id": id_produto,
            "id_colecao": self.colecao_selecionada,
            "imagem": imagem_produto,
            "produto": nome_produto,
            "preco": float(preco_produto),
            "ativo": 1
        }
        self.produtos.append(dic)
        self.conteudo["produtos_estoque"] = self.produtos
        salvar(self.conteudo)
        self.atualizar()

    def preco_total(self):
        self.conteudo = App.get_running_app().conteudo
        produtos = self.conteudo["produtos_estoque"]
        subprodutos = self.conteudo["subprodutos_estoque"]

        preco = 0
        for produto in produtos:
            if produto["ativo"] == 1 and produto["id_colecao"] == self.colecao_selecionada:
                for subproduto in subprodutos:
                    if subproduto["ativo"] == 1:
                        preco += produto["preco"] * subproduto["quantidade"]
                
        return preco

    def atualizar(self, colecao=None):
        self.conteudo = App.get_running_app().conteudo
        if colecao == None:
            colecao = self.colecao_selecionada

        self.produtos = self.conteudo["produtos_estoque"]
        self.ordem = sorted(self.conteudo["produtos_estoque"], key=lambda d: d['preco']) 
        self.ordem.reverse()

        self.clear_widgets(self.children[1:])

        for produto in self.ordem:
            if produto["ativo"] == 1 and produto["id_colecao"] == colecao:
                print(produto)
                preco_formatado = 'R$' + '{:,.2f}'.format(produto['preco'])
                texto = f"{produto['produto']}\n{preco_formatado}"
                self.add_widget(Caixa_produto(text=texto, id_produto=produto["id"], imagem=produto["imagem"]), len(self.children))

class Caixa_produto(Button):
    def __init__(self, id_produto, imagem, **kwargs):
        super().__init__(**kwargs)
        self.id_produto = id_produto
        self.size_hint_y = None
        self.width = self.width
        self.ids.imagem_produto.source = imagem



class Scroll_subprodutos(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conteudo = App.get_running_app().conteudo
        self.colecao_selecionada = 0
        self.produto_selecionado = 0
        self.atualizar()
        self.editando_subproduto_id = 0

    def excluir_subproduto(self):
        self.conteudo = App.get_running_app().conteudo
        self.subprodutos[self.editando_subproduto_id - 1]["ativo"] = 0
        self.conteudo["subprodutos_estoque"] = self.subprodutos
        salvar(self.conteudo)
        self.atualizar()

    def editar_subproduto(self, imagem_subproduto, nome_subproduto, quantidade_subproduto):
        self.conteudo = App.get_running_app().conteudo
        dic = {
            "id": self.editando_subproduto_id,
            "id_produto": self.produto_selecionado,
            "subproduto": nome_subproduto,
            "quantidade": int(quantidade_subproduto),
            "imagem": imagem_subproduto,
            "ativo": 1
        }

        self.subprodutos[self.editando_subproduto_id - 1] = dic
        self.conteudo["subprodutos_estoque"] = self.subprodutos
        salvar(self.conteudo)
        self.atualizar()

    def adicionar_subproduto(self, imagem_subproduto, nome_subproduto, quantidade_subproduto):
        self.conteudo = App.get_running_app().conteudo
        dic = {
            "id": len(self.subprodutos) + 1,
            "id_produto": self.produto_selecionado,
            "subproduto": nome_subproduto,
            "quantidade": int(quantidade_subproduto),
            "imagem": imagem_subproduto,
            "ativo": 1
        }

        self.subprodutos.append(dic)
        self.conteudo["subprodutos_estoque"] = self.subprodutos
        salvar(self.conteudo)
        self.atualizar()

    def pesquisar(self, texto):
        self.conteudo = App.get_running_app().conteudo
        self.subprodutos = self.conteudo["subprodutos_estoque"]
        self.ordem = sorted(self.conteudo["subprodutos_estoque"], key=lambda d: d['subproduto'].lower()) 
        self.ordem.reverse()

        self.clear_widgets(self.children[1:])

        for subproduto in self.ordem:
            if subproduto["ativo"] == 1 and texto in subproduto["subproduto"] and subproduto["id_produto"] == self.produto_selecionado:
                texto = f"{subproduto['subproduto']}\n{subproduto['quantidade']} unidades"
                self.add_widget(Caixa_subproduto(id_subproduto=subproduto["id"], imagem=subproduto["imagem"], text=texto), len(self.children))

    def preco_total(self):
        self.conteudo = App.get_running_app().conteudo
        self.subprodutos = self.conteudo["subprodutos_estoque"]
        produtos = self.conteudo["produtos_estoque"]

        quantidade = 0
        for subproduto in self.subprodutos:
            if subproduto["ativo"] and subproduto["id_produto"] == self.produto_selecionado:
                quantidade += subproduto["quantidade"]

        preco = 0
        if len(produtos) > 1:
            preco = quantidade * produtos[self.produto_selecionado - 1]["preco"]
        elif len(produtos) == 1:
            preco = quantidade * produtos[0]["preco"]
        return preco

    def atualizar(self, produto = None):
        self.conteudo = App.get_running_app().conteudo
        if produto == None:
            produto = self.produto_selecionado

        self.clear_widgets(self.children[1:])

        self.subprodutos = self.conteudo["subprodutos_estoque"]
        self.ordem = sorted(self.conteudo["subprodutos_estoque"], key=lambda d: d['subproduto'].lower()) 
        self.ordem.reverse()
        for subproduto in self.ordem:
            if subproduto["ativo"] == 1 and subproduto["id_produto"] == produto:
                texto = f"{subproduto['subproduto']}\n{subproduto['quantidade']} unidades"
                self.add_widget(Caixa_subproduto(id_subproduto=subproduto["id"], imagem=subproduto["imagem"], text=texto), len(self.children))

class Caixa_subproduto(Button):
    def __init__(self, id_subproduto, imagem, **kwargs):
        super().__init__(**kwargs)
        self.id_subproduto = id_subproduto
        self.size_hint_y = None
        self.width = self.width
        self.ids.imagem_produto.source = imagem



class Scroll_imagens_subprodutos(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id_subproduto = 0
        self.atualizar()

    def copiar_todas_as_imagens(self):
        for widget in self.children[1:-1]:
            App.get_running_app().copiar_imagem(source=widget.source)
        
    def atualizar(self, numero=None):
        self.conteudo = App.get_running_app().conteudo

        if numero == None:
            numero = self.id_subproduto
        
        self.id_subproduto = numero
        self.clear_widgets(self.children[1:-1])

        for imagem in self.conteudo["imagens_subprodutos_estoque"]:
            if imagem["ativo"] == 1 and imagem["id_subproduto"] == self.id_subproduto:
                self.add_widget(Caixa_imagens_subprodutos(
                    id=imagem["id"],
                    imagem=imagem["imagem"],
                    id_subproduto=self.id_subproduto), len(self.children) - 1
                )

    def adicionar(self, imagem):
        self.conteudo = App.get_running_app().conteudo
        dic = {
            "id": len(self.conteudo["imagens_subprodutos_estoque"]) + 1,
            "imagem": imagem,
            "id_subproduto": self.id_subproduto,
            "ativo": 1
        }
        self.conteudo["imagens_subprodutos_estoque"].append(dic)
        salvar(self.conteudo)
        self.atualizar()

    def excluir(self, id):
        self.conteudo = App.get_running_app().conteudo

        self.conteudo["imagens_subprodutos_estoque"][id - 1]["ativo"] = 0
        salvar(self.conteudo)
        self.atualizar()


class Caixa_imagens_subprodutos(BoxLayout):
    def __init__(self, id, imagem, id_subproduto, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.id_subproduto = id_subproduto
        self.source = imagem
        self.ids.imagem.source = imagem