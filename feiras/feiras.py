from kivy.uix.boxlayout import BoxLayout
from save_and_load import *
from kivy.uix.label import Label
from kivy.app import App
import datetime
from kivy.uix.screenmanager import Screen


class Tela_feira(Screen):
    def on_touch_move(self, touch):
        if touch.x + 20 < touch.ox:
            App.get_running_app().root.resetar_screenmanagers()
            self.parent.transition.direction = "left"
            self.parent.current = "agenda"
        
        elif touch.x - 20 > touch.ox:
            App.get_running_app().root.resetar_screenmanagers()
            self.parent.transition.direction = "right"
            self.parent.current = "estoque"


class Feiras_scroll(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.editar_feiras = 0
        self.finalizar_feiras = 0
        self.adicionando_produto = 0
        self.anos = [str(datetime.date.today().year), str(datetime.date.today().year + 1), str(datetime.date.today().year + 2)]
        self.conteudo = App.get_running_app().conteudo
        self.atualizar()

    def colecoes(self):
        self.conteudo = App.get_running_app().conteudo
        colecoes = []
        for colecao in self.conteudo["colecoes_estoque"]:
            if colecao["ativo"] == 1:
                colecoes.append(colecao["colecao"])
        colecoes.sort()
        return colecoes

    def procurar_subprodutos(self, produto_nome):
        self.conteudo = App.get_running_app().conteudo
        id = 0
        for produto in self.conteudo["produtos_estoque"]:
            if produto["produto"] == produto_nome and produto["ativo"] == 1:
                id = produto["id"]

        subprodutos = []
        for subproduto in self.conteudo["subprodutos_estoque"]:
            if subproduto["ativo"] == 1 and subproduto["id_produto"] == id:
                subprodutos.append(subproduto["subproduto"])
        subprodutos.sort()
        return subprodutos

    def procurar_produtos(self, colecao_nome):
        self.conteudo = App.get_running_app().conteudo
        id = 0
        for colecao in self.conteudo["colecoes_estoque"]:
            if colecao["colecao"] == colecao_nome and colecao["ativo"] == 1:
                id = colecao["id"]

        produtos = []
        for produto in self.conteudo["produtos_estoque"]:
            if produto["ativo"] == 1 and produto["id_colecao"] == id:
                produtos.append(produto["produto"])
        produtos.sort()
        return produtos

    def excluir(self):
        self.conteudo = App.get_running_app().conteudo

        self.conteudo["feiras"][self.editar_feiras - 1]["ativo"] = 0
        salvar(self.conteudo)
        self.atualizar()

    def editar(self, dia, mes, ano, local, horario_inicio, horario_final, descricao, nome_feira):
        self.conteudo = App.get_running_app().conteudo
        
        dic = {
            "id": self.editar_feiras,
            "data_feira": ano + "-" + mes + "-" + dia,
            "horario_inicio": horario_inicio.strip(),
            "horario_final": horario_final.strip(),
            "nome_feira": nome_feira.strip(),
            "local_feira": local.strip(),
            "descricao": descricao.strip(),
            "ativo": 1
        }

        self.conteudo["feiras"][self.editar_feiras - 1] = dic
        salvar(self.conteudo)
        self.atualizar()

    def excluir_subproduto_feira(self, id):
        self.conteudo = App.get_running_app().conteudo

        self.conteudo["subprodutos_feira"][id - 1]["ativo"] = 0
        salvar(self.conteudo)
        self.atualizar()

    def adicionar_produto(self, nome_colecao, nome_produto, nome_subproduto, quantidade):
        self.conteudo = App.get_running_app().conteudo

        for colecao in self.conteudo["colecoes_estoque"]:
            if colecao["colecao"] == nome_colecao:
                id_colecao = colecao["id"]
                break

        for produto in self.conteudo["produtos_estoque"]:
            if produto["produto"] == nome_produto and produto["id_colecao"] == id_colecao:
                id_produto = produto["id"]
                break

        for subproduto in self.conteudo["subprodutos_estoque"]:
            if subproduto["subproduto"] == nome_subproduto and subproduto["id_produto"] == id_produto:
                id_subproduto = subproduto["id"]
                break
        
        dic = {
            "id": len(self.conteudo["subprodutos_feira"]) + 1,
            "id_feira": self.adicionando_subproduto,
            "id_subproduto": id_subproduto,
            "quantidade": int(quantidade),
            "ativo": 1
        }

        self.conteudo["subprodutos_feira"].append(dic)
        salvar(self.conteudo)
        self.atualizar()

    def adicionar(self, dia, mes, ano, local, horario_inicial, horario_final, descricao, nome_feira):
        self.conteudo = App.get_running_app().conteudo

        dic = {
            "id": len(self.conteudo["feiras"]) + 1,
            "data_feira": ano + "-" + mes + "-" + dia,
            "horario_inicio": horario_inicial.strip(),
            "horario_final": horario_final.strip(),
            "nome_feira": nome_feira.strip(),
            "local_feira": local.strip(),
            "descricao": descricao.strip(),
            "ativo": 1
        }

        self.conteudo["feiras"].append(dic)
        salvar(self.conteudo)
        self.atualizar()

    def atualizar(self):
        self.conteudo = App.get_running_app().conteudo

        self.clear_widgets(self.children[1:])
        ordem = sorted(self.conteudo["feiras"], key=lambda d: d['data_feira']) 
        ordem.reverse()
        for feira in ordem:
            if feira["ativo"] == 1:
                self.add_widget(Caixa_feira(
                    id_feira= feira["id"],
                    nome_feira= feira["nome_feira"],
                    local_feira= feira["local_feira"],
                    data_feira= feira["data_feira"],
                    horario_inicial= feira["horario_inicio"],
                    horario_final= feira["horario_final"],
                    descricao= feira["descricao"]
                ), len(self.children))


class Caixa_feira(BoxLayout):
    def __init__(self, id_feira, nome_feira, local_feira, data_feira, horario_inicial, horario_final, descricao, **kwargs):
        super().__init__(**kwargs)
        self.conteudo = App.get_running_app().conteudo
        self.id_feira = id_feira
        self.nome_feira = nome_feira
        self.local_feira = local_feira
        self.data_feira = data_feira
        self.horario_inicial = horario_inicial
        self.horario_final = horario_final
        self.descricao = descricao
        previsoes_tempo = App.get_running_app().previsoes_tempo

        if data_feira in previsoes_tempo:
            self.chance_chuva = previsoes_tempo[data_feira]
            
            if self.chance_chuva == 0:
                imagem = "imagens/sem_chance_chuva.png"
            elif 30 >= self.chance_chuva:
                imagem = "imagens/pouca_chance_chuva.png"
            elif 70 >= self.chance_chuva:
                imagem = "imagens/media_chance_chuva.png"
            else:
                imagem = "imagens/alta_chance_chuva.png"

            self.ids.imagem_chance_chuva.source = imagem
            self.ids.porcentagem_chance_chuva.text = str(self.chance_chuva) + "%"

        self.subprodutos = []
        for subproduto in self.conteudo["subprodutos_feira"]:
            if subproduto["ativo"] == 1 and subproduto["id_feira"] == self.id_feira:
                self.subprodutos.append(subproduto)
                produto = self.conteudo["produtos_estoque"][self.conteudo["subprodutos_estoque"][subproduto["id_subproduto"] - 1]["id_produto"] - 1]
                colecao = self.conteudo["colecoes_estoque"][produto["id_colecao"] - 1]
                self.add_widget(Caixa_subproduto_feira(
                    id=subproduto["id"],
                    imagem= self.conteudo["subprodutos_estoque"][subproduto["id_subproduto"] - 1]["imagem"],
                    nome_subproduto= colecao["colecao"] + " " + produto["produto"] + " " + self.conteudo["subprodutos_estoque"][subproduto["id_subproduto"] - 1]["subproduto"],
                    quantidade = subproduto["quantidade"]
                    ), len(self.children) - 1)
        
        preco_total = 0
        for subproduto in self.subprodutos:
            subproduto_estoque = self.conteudo["subprodutos_estoque"][subproduto["id_subproduto"] - 1]
            produto_estoque = self.conteudo["produtos_estoque"][subproduto_estoque["id_produto"] - 1]
            preco_total += subproduto["quantidade"] * produto_estoque["preco"]
                
        self.ids.botao_feira_concluir.text = f"{self.nome_feira}\n{self.local_feira}\n{converter_data(self.data_feira)}\n{self.horario_inicial}-{self.horario_final}\nPreço total: {'R$' + '{:,.2f}'.format(preco_total)}"
        
        if self.descricao not in ["Descrição", ""]:
            self.height += 80
            self.ids.caixa_feira.height += 80
            self.ids.botao_feira_concluir.text += f"\n {descricao}"



class Caixa_subproduto_feira(BoxLayout):
    def __init__(self, id, imagem, nome_subproduto, quantidade, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = None
        self.id = id
        self.imagem = imagem
        self.ids.imagem_subproduto_feira.source = imagem
        self.nome_subproduto = nome_subproduto
        self.ids.texto_subproduto_feira.text = f"{nome_subproduto}:\n{quantidade} unidade(s)"


class Concluir_feira_scroll(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id_feira = 0
        self.conteudo = App.get_running_app().conteudo
        self.atualizar()

    def preco_subproduto_venda(self, metodo_pagamento, nome_subproduto, quantidade):
        self.conteudo = App.get_running_app().conteudo
        if quantidade == "":
            quantidade = 1
        quantidade = int(quantidade)

        print(nome_subproduto)
        if nome_subproduto != "•Escolha um subproduto":
            subproduto = self.conteudo["subprodutos_estoque"][self.ids_subprodutos_levados[nome_subproduto] - 1]
            print(subproduto)
            produto = self.conteudo["produtos_estoque"][subproduto["id_produto"] - 1]
            print(produto)
            preco = produto["preco"] * quantidade
            if metodo_pagamento in ["Pix", "Dinheiro físico"]:
                preco *= .95

            return str(preco)
        else:
            return ""

    def concluir_feira(self):
        self.conteudo = App.get_running_app().conteudo

        id_feira = len(self.conteudo["historico_feiras"]) + 1
        feira = self.conteudo["feiras"][id_feira - 1]
        
        self.conteudo["feiras"][id_feira - 1]["ativo"] = 0
        dic = {
            "id": id_feira,
            "horario_inicio": feira["horario_inicio"],
            "horario_final": feira["horario_final"],
            "nome_feira": feira["nome_feira"],
            "local_feira": feira["local_feira"],
            "data_feira": feira["data_feira"],
            "descricao": feira["descricao"]
        }

        self.conteudo["historico_feiras"].append(dic)

        for venda in self.conteudo["feiras_vendas"]:
            if venda["ativo"] == 1 and venda["id_feira"] == self.id_feira:
                dic = {
                    "id": len(self.conteudo["historico_feiras_vendas"]) + 1,
                    "id_historico_feira": id_feira,
                    "id_subproduto": venda["id_subproduto"],
                    "quantidade": venda["quantidade"],
                    "descricao": venda["descricao"],
                    "preco_total": venda["preco"],
                    "forma_pagamento": venda["forma_pagamento"]
                }

                self.conteudo["subprodutos_estoque"][venda["id_subproduto"] - 1]["quantidade"] -= venda["quantidade"]

                self.conteudo["historico_feiras_vendas"].append(dic)

        self.conteudo["feiras_vendas"] = []
        salvar(self.conteudo)
        self.atualizar()

    def excluir_venda_feira(self, id):
        self.conteudo = App.get_running_app().conteudo

        self.conteudo["subprodutos_feira"][id - 1]["ativo"] = 0
        salvar(self.conteudo)
        self.atualizar()

    def subprodutos_levados_na_feira(self):
        self.conteudo = App.get_running_app().conteudo
        
        self.ids_subprodutos_levados = {}
        subprodutos = []
        for subproduto_feira in self.conteudo["subprodutos_feira"]:
            if subproduto_feira["ativo"] == 1 and subproduto_feira["id_feira"] == self.id_feira:
                subproduto_estoque = self.conteudo["subprodutos_estoque"][subproduto_feira["id_subproduto"] - 1]
                produto_estoque = self.conteudo["produtos_estoque"][subproduto_estoque["id_produto"] - 1]
                colecao_estoque = self.conteudo["colecoes_estoque"][produto_estoque["id_colecao"] - 1]
                nome = colecao_estoque["colecao"] + " " + produto_estoque["produto"] + " " + subproduto_estoque["subproduto"]
                subprodutos.append(nome)
                self.ids_subprodutos_levados[nome] = subproduto_feira["id_subproduto"]

        return subprodutos

    def atualizar(self):
        self.conteudo = App.get_running_app().conteudo

        self.clear_widgets(self.children[1:])

        for venda in self.conteudo["feiras_vendas"]:
            if venda["ativo"] == 1 and venda["id_feira"] == self.id_feira:
                subproduto = self.conteudo["subprodutos_estoque"][venda["id_subproduto"] - 1]
                produto = self.conteudo["produtos_estoque"][subproduto["id_produto"] - 1]
                colecao = self.conteudo["colecoes_estoque"][produto["id_colecao"] - 1]
                self.add_widget(Caixa_concluir_feira(
                    id= venda["id"],
                    imagem= subproduto["imagem"],
                    nome_subproduto= colecao["colecao"] + " " + produto["produto"] + " " + subproduto["subproduto"],
                    quantidade= venda["quantidade"],
                    preco= venda["preco"],
                    descricao= venda["descricao"]
                ), len(self.children))

    def adicionar(self, nome_subproduto, quantidade, descricao, preco, forma_pagamento, id_feira):
        self.conteudo = App.get_running_app().conteudo

        id = self.conteudo["subprodutos_feira"][self.ids_subprodutos_levados[nome_subproduto] - 1]["id_subproduto"]

        dic = {
            "id": len(self.conteudo["feiras_vendas"]) + 1,
            "id_feira": id_feira,
            "id_subproduto": id,
            "quantidade": int(quantidade),
            "descricao": descricao.strip(),
            "preco": float(preco),
            "forma_pagamento": forma_pagamento,
            "ativo": 1
        }

        self.conteudo["feiras_vendas"].append(dic)
        salvar(self.conteudo)
        self.atualizar()


class Caixa_concluir_feira(BoxLayout):
    def __init__(self, id, imagem, nome_subproduto, quantidade, preco, descricao, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.ids.imagem_feiras_subproduto_concluir.source = imagem
        self.ids.feiras_nome_subproduto_concluir.text = nome_subproduto
        self.ids.feiras_quantidade_subproduto_concluir.text = str(quantidade)
        self.ids.preco_total_agenda_caixa_concluir.text = 'R$' + '{:,.2f}'.format(preco)
        if descricao != "" and descricao != "Descrição":
            self.height += 80
            self.ids.caixinha_descricao_concluir.add_widget(Label(text=descricao, bold=True, font_size=60, text_size=self.size))


def converter_data(data):
    dia = data[8:]
    mes = data[5:7]
    ano = data[:4]
    data_convertida = dia + "/" + mes + "/" + ano
    return data_convertida