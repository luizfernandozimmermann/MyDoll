from save_and_load import *
import pyowm

cidade = "Blumenau"

# Cria uma instância da API do OpenWeatherMap
owm = pyowm.OWM('8819aed96ad08d3d7e976baa6d0ba048')

# Obtém o gerenciador de clima da OWM
gerenciador_clima = owm.weather_manager()

# Pesquisa a previsão do tempo para a cidade especificada
observacao = gerenciador_clima.weather_at_place(cidade)

previsao_tempo = gerenciador_clima.forecast_at_place(cidade, '3h')

# Imprime as informações da previsão do tempo para cada dia
for clima in previsao_tempo.forecast:
    data = clima.reference_time('date').strftime('%Y-%m-%d')
    hora = clima.reference_time('date').hour
    temperatura = clima.temperature('celsius')['temp']
    condicao_clima = clima.status
    prob_chuva = clima.rain.get('3h')  # porcentagem de chance de chuva em 3 horas
    if prob_chuva != None:    
        print(data)