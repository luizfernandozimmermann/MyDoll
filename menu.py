from kivy.uix.boxlayout import BoxLayout
from save_and_load import *
from kivy.app import App
from kivy.uix.label import Label


class Menu_proximas_entregas(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conteudo = App.get_running_app().conteudo
        self.atualizar()

    def atualizar(self):
        self.conteudo = App.get_running_app().conteudo

        ordem = sorted(self.conteudo["agenda"], key=lambda d: d['data_entrega']) 

        self.clear_widgets()
        for item in ordem:
            if item["ativo"] == 1:
                subproduto = self.conteudo["subprodutos_estoque"][item["id_subproduto"] - 1]
                produto = self.conteudo["produtos_estoque"][subproduto["id_produto"] - 1]
                self.add_widget(Caixa_menu_entregas(
                    id_entrega= item["id"],
                    imagem= subproduto["imagem"],
                    subproduto= subproduto["subproduto"],
                    quantidade= item["quantidade"],
                    data= item["data_entrega"],
                    preco= produto["preco"],
                    descricao= item["descricao"]
                ))


class Caixa_menu_entregas(BoxLayout):
    def __init__(self, id_entrega, imagem, subproduto, quantidade, data, preco, descricao, **kwargs):
        super().__init__(**kwargs)
        self.id_entrega = id_entrega
        self.ids.imagem_compromisso_menu.source = imagem
        self.ids.nome_e_quantidade_subproduto_compromisso_menu.text = subproduto + ": " + str(quantidade) + " unidades"
        self.ids.data_compromisso_menu.text = converter_data(data)
        self.ids.preco_subproduto_compromisso_menu.text = "R$" + "{:,.2f}".format(preco * quantidade)
        if descricao != "" and descricao != "Descrição":
            self.add_widget(Label(text=descricao, size_hint_y=0.3, bold=True, text_size=(self.width, None), halign="center"))
    

class Menu_proximas_feiras(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conteudo = App.get_running_app().conteudo
        self.atualizar()

    def atualizar(self):
        self.conteudo = App.get_running_app().conteudo

        ordem = sorted(self.conteudo["feiras"], key=lambda d: d['data_feira']) 

        self.clear_widgets()
        for item in ordem:
            if item["ativo"] == 1:
                self.add_widget(Caixa_menu_feiras(
                    data= item["data_feira"],
                    nome_feira= item["nome_feira"],
                    local= item["local_feira"],
                    horario_final= item["horario_final"],
                    horario_inicio= item["horario_inicio"],
                    descricao= item["descricao"]
                ))

class Caixa_menu_feiras(BoxLayout):
    def __init__(self, data, nome_feira, local, horario_inicio, horario_final, descricao, **kwargs):
        super().__init__(**kwargs)
        self.ids.data_feira_menu.text = converter_data(data)
        self.ids.nome_feira_menu.text = nome_feira
        self.ids.local_feira_menu.text = local
        self.ids.horarios_feira_menu.text = horario_inicio + " - " + horario_final
        if descricao != "" and descricao != "Descrição":
            self.add_widget(Label(text=descricao, size_hint_y=0.3, bold=True))


def converter_data(data):
    dia = data[8:]
    mes = data[5:7]
    ano = data[:4]
    data_convertida = dia + "/" + mes + "/" + ano
    return data_convertida