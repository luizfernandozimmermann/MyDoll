from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
            

class Historico_scroll(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filtro_mes = "Mês: Todos"
        self.filtro_ano = "Ano: Todos"
        self.atualizar()

    def total_vendas(self, filtro_mes, filtro_ano):
        self.conteudo = App.get_running_app().conteudo
        filtro_mes = filtro_mes.split()[1]
        filtro_ano = filtro_ano.split()[1]

        vendas_feiras = self.conteudo["historico_feiras_vendas"]
        vendas_individuais = self.conteudo["historico_agenda"]

        total_vendas = 0
        for venda in vendas_feiras:
            feira = self.conteudo["historico_feiras"][venda["id_historico_feira"] - 1]
            if filtro_ano in [feira["data_feira"][:4], "Todos"] and filtro_mes in [feira["data_feira"][5:7], "Todos"]:
                total_vendas += venda["preco_total"]
        
        for venda in vendas_individuais:
            if filtro_ano in [venda["data_entrega"][:4], "Todos"] and filtro_mes in [venda["data_entrega"][5:7], "Todos"]:
                total_vendas += venda["preco_total"]

        return total_vendas

    def anos_filtro(self):
        self.conteudo = App.get_running_app().conteudo
        individuais = self.conteudo["historico_agenda"]
        feiras = self.conteudo["historico_feiras"]
        anos = []
        for venda in individuais:
            if venda["data_entrega"][:4] not in anos:
                anos.append(venda["data_entrega"][:4])

        for feira in feiras:
            if feira["data_feira"][:4] not in anos:
                for num, ano in enumerate(anos):
                    if int(feira["data_feira"][:4]) < int(ano):
                        anos.insert(num, feira["data_feira"][:4])
                        break

                    if num == len(anos) - 1:
                        anos.append(feira["data_feira"][5:7])

                if len(anos) == 0:
                    anos.append(feira["data_feira"][:4])

        anos.sort()

        for num, ano in enumerate(anos):
            anos[num] = "Ano: " + ano
        
        anos.insert(0, "Ano: Todos")
        return anos

    def meses_filtro(self):
        self.conteudo = App.get_running_app().conteudo
        individuais = self.conteudo["historico_agenda"]
        feiras = self.conteudo["historico_feiras"]
        meses = []
        for venda in individuais:
            if venda["data_entrega"][5:7] not in meses:
                meses.append(venda["data_entrega"][5:7])

        for feira in feiras:
            if feira["data_feira"][5:7] not in meses:
                for num, mes in enumerate(meses):
                    if int(feira["data_feira"][5:7]) < int(mes):
                        meses.insert(num, feira["data_feira"][5:7])
                        break

                    if num == len(meses) - 1:
                        meses.append(feira["data_feira"][5:7])
                
                if len(meses) == 0:
                    meses.append(feira["data_feira"][5:7])

        meses.sort()

        for num, mes in enumerate(meses):
            meses[num] = "Mês: " + mes
        
        meses.insert(0, "Mês: Todos")
        return meses

    def atualizar(self):
        self.conteudo = App.get_running_app().conteudo

        self.clear_widgets()
        self.add_widget(Button(height=1, size_hint_y=None, background_color=(0, 0, 0, 0)))

        self.historico = self.conteudo["historico_agenda"]
        self.ordem = sorted(self.conteudo["historico_agenda"], key=lambda d: d['data_entrega']) 
        for venda in self.ordem:
            subproduto = self.conteudo["subprodutos_estoque"][venda["id_subproduto"] - 1]
            produto = self.conteudo["produtos_estoque"][subproduto["id_produto"] - 1]
            colecao = self.conteudo["colecoes_estoque"][produto["id_colecao"] - 1]
            self.add_widget(Caixa_historico(
                data= venda["data_entrega"],
                nome= colecao["colecao"] + " " + produto["produto"] + " " + subproduto["subproduto"],
                quantidade= venda["quantidade"],
                preco= venda["preco_total"],
                imagem= subproduto["imagem"],
                metodo_pagamento= venda["forma_pagamento"],
                descricao= venda["descricao"]
            ))

    def filtro_atualizar(self, mes, ano):
        self.conteudo = App.get_running_app().conteudo

        self.clear_widgets()
        self.add_widget(Button(height=1, size_hint_y=None, background_color=(0, 0, 0, 0)))
        
        self.ordem = sorted(self.conteudo["historico_agenda"], key=lambda d: d['data_entrega']) 

        if mes == "Todos":
            if ano == "Todos":
                self.atualizar()
            else:
                for venda in self.ordem:
                    if venda["data_entrega"][:4] == ano:
                        subproduto = self.conteudo["subprodutos_estoque"][venda["id_subproduto"] - 1]
                        produto = self.conteudo["produtos_estoque"][subproduto["id_produto"] - 1]
                        colecao = self.conteudo["colecoes_estoque"][produto["id_colecao"] - 1]
                        self.add_widget(Caixa_historico(
                            data= venda["data_entrega"],
                            nome= colecao["colecao"] + " " + produto["produto"] + " " + subproduto["subproduto"],
                            quantidade= venda["quantidade"],
                            preco= venda["preco_total"],
                            imagem= subproduto["imagem"],
                            metodo_pagamento= venda["forma_pagamento"],
                            descricao= venda["descricao"]
                        ))
        else:
            if ano == "Todos":
                for venda in self.ordem:
                    if venda["data_entrega"][5:7] == mes:
                        subproduto = self.conteudo["subprodutos_estoque"][venda["id_subproduto"] - 1]
                        produto = self.conteudo["produtos_estoque"][subproduto["id_produto"] - 1]
                        colecao = self.conteudo["colecoes_estoque"][produto["id_colecao"] - 1]
                        self.add_widget(Caixa_historico(
                            data= venda["data_entrega"],
                            nome= colecao["colecao"] + " " + produto["produto"] + " " + subproduto["subproduto"],
                            quantidade= venda["quantidade"],
                            preco= venda["preco_total"],
                            imagem= subproduto["imagem"],
                            metodo_pagamento= venda["forma_pagamento"],
                            descricao= venda["descricao"]
                        ))
            else:
                for venda in self.ordem:
                    if venda["data_entrega"][5:7] == mes and venda["data_entrega"][:4] == ano:
                        subproduto = self.conteudo["subprodutos_estoque"][venda["id_subproduto"] - 1]
                        produto = self.conteudo["produtos_estoque"][subproduto["id_produto"] - 1]
                        colecao = self.conteudo["colecoes_estoque"][produto["id_colecao"] - 1]
                        self.add_widget(Caixa_historico(
                            data= venda["data_entrega"],
                            nome= colecao["colecao"] + " " + produto["produto"] + " " + subproduto["subproduto"],
                            quantidade= venda["quantidade"],
                            preco= venda["preco_total"],
                            imagem= subproduto["imagem"],
                            metodo_pagamento= venda["forma_pagamento"],
                            descricao= venda["descricao"]
                        ))
    

class Caixa_historico(BoxLayout):
    def __init__(self, data, nome, quantidade, preco, imagem, metodo_pagamento, descricao, **kwargs):
        super().__init__(**kwargs)
        self.ids.data_historico_caixa.text = converter_data(data)
        self.ids.nome_e_quantidade_subproduto_historico_caixa.text = f"{nome}: {quantidade} unidade(s)"
        self.ids.preco_total_historico_caixa.text = "R$" + "{:,.2f}".format(preco)
        self.ids.imagem_historico_caixa.source = imagem
        self.ids.metodo_de_pagamento.text = metodo_pagamento
        if descricao != "" and descricao != "Descrição":
            self.height += 80
            self.ids.caixinha_conteudo_historico.add_widget(Label(text=descricao, bold=True, font_size=60))
            


class Historico_scroll_feiras(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filtro_mes = "Mês: Todos"
        self.filtro_ano = "Ano: Todos"
        self.atualizar()
    
    def atualizar(self):
        self.conteudo = App.get_running_app().conteudo
        self.clear_widgets()
        self.add_widget(Button(height=1, size_hint_y=None, background_color=(0, 0, 0, 0)))

        self.feiras_historico = self.conteudo["historico_feiras"]
        self.ordem = sorted(self.conteudo["historico_feiras"], key=lambda d: d['data_feira']) 
        for feira in self.ordem:
            vendas_feira = []
            for venda in self.conteudo["historico_feiras_vendas"]:
                if venda["id_historico_feira"] == feira["id"]:
                    vendas_feira.append(venda)

            self.add_widget(Caixa_historico_feira(
                vendas= vendas_feira,
                nome_feira= feira["nome_feira"],
                local= feira["local_feira"],
                data_feira= feira["data_feira"],
                horario_inicial= feira["horario_inicio"],
                horario_final= feira["horario_final"],
                descricao= feira["descricao"]
            ))

            for venda in vendas_feira:
                subproduto = self.conteudo["subprodutos_estoque"][venda["id_subproduto"] - 1]
                produto = self.conteudo["produtos_estoque"][subproduto["id_produto"] - 1]
                colecao = self.conteudo["colecoes_estoque"][produto["id_colecao"] - 1]
                self.add_widget(Produto_feiras_historico(
                    imagem= subproduto["imagem"],
                    nome= colecao["colecao"] + " " + produto["produto"] + " " + subproduto["subproduto"],
                    quantidade= venda["quantidade"],
                    preco= venda["preco_total"],
                    forma_pagamento= venda["forma_pagamento"],
                    descricao= venda["descricao"]
                ))
            self.add_widget(BoxLayout(size_hint_y=None, height=30))

    def filtro_atualizar(self, mes, ano):
        self.conteudo = App.get_running_app().conteudo
        self.clear_widgets()
        self.add_widget(Button(height=1, size_hint_y=None, background_color=(0, 0, 0, 0)))

        feiras_historico = self.conteudo["historico_feiras"]
        self.ordem = sorted(self.conteudo["historico_feiras"], key=lambda d: d['data_feira']) 
        if mes == "Todos":
            if ano == "Todos":
                self.atualizar()
            else:
                for feira in feiras_historico:
                    if ano == feira["data_feira"][:4]:
                        vendas_feira = []
                        for venda in self.conteudo["historico_feiras_vendas"]:
                            if venda["id_historico_feira"] == feira["id"]:
                                vendas_feira.append(venda)

                        self.add_widget(Caixa_historico_feira(
                            vendas= vendas_feira,
                            nome_feira= feira["nome_feira"],
                            local= feira["local_feira"],
                            data_feira= feira["data_feira"],
                            horario_inicial= feira["horario_inicio"],
                            horario_final= feira["horario_final"],
                            descricao= feira["descricao"]
                        ))

                        for venda in vendas_feira:
                            subproduto = self.conteudo["subprodutos_estoque"][venda["id_subproduto"] - 1]
                            produto = self.conteudo["produtos_estoque"][subproduto["id_produto"] - 1]
                            colecao = self.conteudo["colecoes_estoque"][produto["id_colecao"] - 1]
                            self.add_widget(Produto_feiras_historico(
                                imagem= subproduto["imagem"],
                                nome= colecao["colecao"] + " " + produto["produto"] + " " + subproduto["subproduto"],
                                quantidade= venda["quantidade"],
                                preco= venda["preco_total"],
                                forma_pagamento= venda["forma_pagamento"],
                                descricao= venda["descricao"]
                            ))
                        self.add_widget(BoxLayout(size_hint_y=None, height=30))
        else:
            if ano == "Todos":
                for feira in feiras_historico:
                    if feira["data_feira"][5:7] == mes:
                        vendas_feira = []
                        for venda in self.conteudo["historico_feiras_vendas"]:
                            if venda["id_historico_feira"] == feira["id"]:
                                vendas_feira.append(venda)

                        self.add_widget(Caixa_historico_feira(
                            vendas= vendas_feira,
                            nome_feira= feira["nome_feira"],
                            local= feira["local_feira"],
                            data_feira= feira["data_feira"],
                            horario_inicial= feira["horario_inicio"],
                            horario_final= feira["horario_final"],
                            descricao= feira["descricao"]
                        ))

                        for venda in vendas_feira:
                            subproduto = self.conteudo["subprodutos_estoque"][venda["id_subproduto"] - 1]
                            produto = self.conteudo["produtos_estoque"][subproduto["id_produto"] - 1]
                            colecao = self.conteudo["colecoes_estoque"][produto["id_colecao"] - 1]
                            self.add_widget(Produto_feiras_historico(
                                imagem= subproduto["imagem"],
                                nome= colecao["colecao"] + " " + produto["produto"] + " " + subproduto["subproduto"],
                                quantidade= venda["quantidade"],
                                preco= venda["preco_total"],
                                forma_pagamento= venda["forma_pagamento"],
                                descricao= venda["descricao"]
                            ))
                        self.add_widget(BoxLayout(size_hint_y=None, height=30))
            else:
                for feira in feiras_historico:
                    if feira["data_feira"][5:7] == mes and feira["data_feira"][:4] == ano:
                        vendas_feira = []
                        for venda in self.conteudo["historico_feiras_vendas"]:
                            if venda["id_historico_feira"] == feira["id"]:
                                vendas_feira.append(venda)

                        self.add_widget(Caixa_historico_feira(
                            vendas= vendas_feira,
                            nome_feira= feira["nome_feira"],
                            local= feira["local_feira"],
                            data_feira= feira["data_feira"],
                            horario_inicial= feira["horario_inicio"],
                            horario_final= feira["horario_final"],
                            descricao= feira["descricao"]
                        ))

                        for venda in vendas_feira:
                            subproduto = self.conteudo["subprodutos_estoque"][venda["id_subproduto"] - 1]
                            produto = self.conteudo["produtos_estoque"][subproduto["id_produto"] - 1]
                            colecao = self.conteudo["colecoes_estoque"][produto["id_colecao"] - 1]
                            self.add_widget(Produto_feiras_historico(
                                imagem= subproduto["imagem"],
                                nome= colecao["colecao"] + " " + produto["produto"] + " " + subproduto["subproduto"],
                                quantidade= venda["quantidade"],
                                preco= venda["preco_total"],
                                forma_pagamento= venda["forma_pagamento"],
                                descricao= venda["descricao"]
                            ))
                        self.add_widget(BoxLayout(size_hint_y=None, height=30))
    

class Caixa_historico_feira(BoxLayout):
    def __init__(self, vendas, nome_feira, local, data_feira, horario_inicial, horario_final, descricao, **kwargs):
        super().__init__(**kwargs)
        preco = 0
        for produto in vendas:
            preco += produto["preco_total"]
        self.ids.preco_feiras_total_historico.text = str(preco)
        self.ids.nome_feira_historico.text = nome_feira
        self.ids.local_feira_historico.text = local
        self.ids.data_feira_historico.text = converter_data(data_feira)
        self.ids.horarios_feira_historico.text = horario_inicial + " - " + horario_final
        if descricao != "" and descricao != "Descrição":
            self.height += 80
            self.ids.caixa_historico_feira_textos.add_widget(Label(text=descricao, bold=True, font_size=60))


class Produto_feiras_historico(BoxLayout):
    def __init__(self, imagem, nome, quantidade, preco, forma_pagamento, descricao, **kwargs):
        super().__init__(**kwargs)
        self.ids.imagem_feiras_produto_historico.source = imagem
        self.ids.feiras_nome_subproduto_historico.text = nome
        self.ids.feiras_quantidade_produto_historico.text = str(quantidade) + " unidade(s)"
        self.ids.preco_total_feira_historico.text = "R$" + "{:,.2f}".format(preco)
        self.ids.metodo_de_pagamento_historico_feira_produto.text = "Pago em: " + forma_pagamento
        if descricao != "" and descricao != "Descrição":
            self.height += 80
            self.ids.caixa_historico_feira_textos.add_widget(Label(text=descricao, bold=True, font_size=60))


def converter_data(data):
    dia = data[8:]
    mes = data[5:7]
    ano = data[:4]
    data_convertida = dia + "/" + mes + "/" + ano
    return data_convertida