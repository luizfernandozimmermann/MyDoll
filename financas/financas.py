from kivy.uix.boxlayout import BoxLayout
from save_and_load import *
from kivy.uix.label import Label
from kivy.app import App
from datetime import date
from kivy.uix.screenmanager import Screen


class Tela_financas(Screen):
    def on_touch_move(self, touch):
        if touch.x - 20 > touch.ox:
            App.get_running_app().root.resetar_screenmanagers()
            self.parent.transition.direction = "right"
            self.parent.current = "historico"



class Scroll_financas_atual(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.anos = [str(date.today().year), str(date.today().year + 1), str(date.today().year + 2)]
        self.atualizar()
        self.dia_atual = str(date.today().day)
        if len(self.dia_atual) == 1:
            self.dia_atual = "0" + self.dia_atual
        self.mes_atual = str(date.today().month)
        if len(self.mes_atual) == 1:
            self.mes_atual = "0" + self.mes_atual
        self.ano_atual = str(date.today().year)
        self.editando_financas = 0

    def atualizar(self):
        self.conteudo = App.get_running_app().conteudo

        self.clear_widgets(self.children[2:])
        conteudo = self.conteudo["financas_atual"]
        conteudo = sorted(conteudo, key=lambda d: d['data']) 
        conteudo.reverse()

        for compras in conteudo:
            if compras["ativo"] == 1:
                self.add_widget(Caixa_financas_atual(
                    id= compras["id"],
                    nome_produto= compras["nome"],
                    local= compras["local"],
                    preco= compras["preco"],
                    forma_pagamento= compras["forma_pagamento"],
                    data= compras["data"],
                    descricao= compras["descricao"]
                ), len(self.children))

    def adicionar(self, produto, local, preco, forma_pagamento, dia, mes, ano, descricao):
        self.conteudo = App.get_running_app().conteudo

        dic = {
            "id": len(self.conteudo["financas_atual"]) + 1,
            "nome": produto.strip(),
            "local": local.strip(),
            "preco": float(preco),
            "forma_pagamento": forma_pagamento,
            "data": ano + "-" + mes + "-" + dia,
            "descricao": descricao.strip(),
            "ativo": 1
        }
        self.conteudo["financas_atual"].append(dic)
        salvar(self.conteudo)
        self.atualizar()

    def editar(self, produto, local, preco, forma_pagamento, dia, mes, ano, descricao):
        self.conteudo = App.get_running_app().conteudo
        dic = {
            "id": self.editando_financas,
            "nome": produto.strip(),
            "local": local.strip(),
            "preco": float(preco),
            "forma_pagamento": forma_pagamento,
            "data": ano + "-" + mes + "-" + dia,
            "descricao": descricao.strip(),
            "ativo": 1
        }
        self.conteudo["financas_atual"][self.editando_financas - 1] = dic
        salvar(self.conteudo)
        self.atualizar()

    def excluir(self):
        self.conteudo["financas_atual"][self.editando_financas - 1]["ativo"] = 0
        salvar(self.conteudo)
        self.atualizar()

    def concluir_mes(self):
        self.conteudo = App.get_running_app().conteudo
        if len(self.conteudo["financas_atual"]) > 0:
            mes = self.conteudo["financas_atual"][0]["data"][5:7]
            ano = self.conteudo["financas_atual"][0]["data"][:4]

            id_historico = len(self.conteudo["historico_financas"]) + 1
            self.conteudo["historico_financas"].append({
                "id": id_historico,
                "mes": mes,
                "ano": ano
            })

            for compra in self.conteudo["financas_atual"]:
                if compra["ativo"] == 1:
                    dic = {
                        "id": len(self.conteudo["historico_financas_compras"]) + 1,
                        "id_historico_financas": id_historico,
                        "nome": compra["nome"],
                        "local": compra["local"],
                        "data": compra["data"],
                        "forma_pagamento": compra["forma_pagamento"],
                        "preco": compra["preco"],
                        "descricao": compra["descricao"]
                    }
                    self.conteudo["historico_financas_compras"].append(dic)

            self.conteudo["financas_atual"] = []
            salvar(self.conteudo)
            self.atualizar()


class Caixa_financas_atual(BoxLayout):
    def __init__(self, id, nome_produto, local, preco, forma_pagamento, data, descricao, **kwargs):
        super().__init__(**kwargs)
        self.id = id
        self.nome = nome_produto
        self.local = local
        self.preco = str(preco)
        self.forma_pagamento = forma_pagamento
        self.descricao = descricao
        self.ids.nome_produto.text = nome_produto
        self.ids.local.text = local
        self.ids.preco.text = f"R${'{:,.2f}'.format(preco)} pago em {forma_pagamento}"
        self.ids.data.text = converter_data(data)
        if descricao != "" and descricao != "Descrição":
            self.height += 70
            self.ids.caixa_financa_descricao_atual.add_widget(Label(text=descricao, bold=True, font_size=60))



class Scroll_financas_historico(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.atualizar()

#
    def atualizar(self):
        self.conteudo = App.get_running_app().conteudo

        self.historico = {}
        for container in self.conteudo["historico_financas"]:
            compras = []
            for compra in self.conteudo["historico_financas_compras"]:
                if compra["id_historico_financas"] == container["id"]:
                    compras.append(compra)
            
            self.historico[container["ano"] + "/" + container["mes"]] = compras

        myKeys = list(self.historico.keys())
        myKeys.sort()
        self.historico = {i: self.historico[i] for i in myKeys}

        for data, lista in self.historico.items():
            self.add_widget(Label(text=data[:4] + "/" + data[5:], color=(0, 0, 0, 1), bold=True, font_size=50))
            for compras in lista:
                self.add_widget(Caixa_financas_historico(
                    nome_produto= compras["nome"],
                    local= compras["local"],
                    preco= compras["preco"],
                    forma_pagamento= compras["forma_pagamento"],
                    data= compras["data"],
                    descricao= compras["descricao"]
                ))

    def filtro_atualizar(self, mes, ano):
        self.atualizar()
        self.clear_widgets()
        if mes == "Todos":
            if ano == "Todos":
                self.atualizar()
            else:
                for data, produtos in self.historico.items():
                    if data[:4] == ano:
                        self.add_widget(Label(text=data[:4] + "/" + data[5:], color=(0, 0, 0, 1), bold=True, font_size=50))
                        for produto in produtos:
                            self.add_widget(Caixa_financas_historico(
                                nome_produto= produto["nome"],
                                local= produto["local"],
                                preco= produto["preco"],
                                forma_pagamento= produto["forma_pagamento"],
                                data= produto["data"],
                                descricao= produto["descricao"]
                            ))
        else:
            if ano == "Todos":
                for data, produtos in self.historico.items():
                    if data[5:] == mes:
                        self.add_widget(Label(text=data[:4] + "/" + data[5:], color=(0, 0, 0, 1), bold=True, font_size=50))
                        for produto in produtos:
                            self.add_widget(Caixa_financas_historico(
                                nome_produto= produto["nome"],
                                local= produto["local"],
                                preco= produto["preco"],
                                forma_pagamento= produto["forma_pagamento"],
                                data= produto["data"],
                                descricao= produto["descricao"]
                            ))
            else:
                for data, produtos in self.historico.items():
                    if data[5:] == mes and data[:4] == ano:
                        self.add_widget(Label(text=data[:4] + "/" + data[5:], color=(0, 0, 0, 1), bold=True, font_size=50))
                        for produto in produtos:
                            self.add_widget(Caixa_financas_historico(
                                nome_produto= produto["nome"],
                                local= produto["local"],
                                preco= produto["preco"],
                                forma_pagamento= produto["forma_pagamento"],
                                data= produto["data"],
                                descricao= produto["descricao"]
                            ))
    
##
    def anos_filtro(self):
        self.conteudo = App.get_running_app().conteudo

        individuais = self.conteudo["historico_financas"]
        anos = []
        for container in individuais:
            if container["ano"] not in anos:
                anos.append(container["ano"])

        anos.sort()

        for num, ano in enumerate(anos):
            anos[num] = "Ano: " + ano
        
        anos.insert(0, "Ano: Todos")
        return anos

    def meses_filtro(self):
        self.conteudo = App.get_running_app().conteudo

        individuais = self.conteudo["historico_financas"]
        meses = []
        for container in individuais:
            if container["mes"] not in meses:
                meses.append(container["mes"])

        meses.sort()

        for num, mes in enumerate(meses):
            meses[num] = "Mês: " + mes
        
        meses.insert(0, "Mês: Todos")
        return meses


class Caixa_financas_historico(BoxLayout):
    def __init__(self, nome_produto, local, preco, forma_pagamento, data, descricao, **kwargs):
        super().__init__(**kwargs)
        self.ids.nome_produto.text = nome_produto
        self.ids.local.text = local
        self.ids.preco.text =  f"R${'{:,.2f}'.format(preco)} pago em {forma_pagamento}"
        self.ids.data.text = converter_data(data)
        if descricao != "" and descricao != "Descrição":
            self.height += 70
            self.ids.caixa_financas_historico_textos.add_widget(Label(text=descricao, bold=True, font_size=60))


def converter_data(data):
    dia = data[8:]
    mes = data[5:7]
    ano = data[:4]
    data_convertida = dia + "/" + mes + "/" + ano
    return data_convertida