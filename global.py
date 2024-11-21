import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


opcoes_menu = [
    '||  [1] - Consultar Energia Solar                              ||',
    '||  [2] - Ver Notícias sobre Energia Solar e Sustentabilidade  ||',
    '||  [3] - Gráfico de Horas para Energia Solar                  ||',
    '||  [4] - Gráfico de Consumo Energético(Brasil)                ||',
    '||  [5] - Sair                                                 ||'
]


def registrar_usuario():
    try:
        nome = input("Digite o seu nome: ")
        senha = input("Digite a sua senha: ")
        print(f"\nSeu registro foi concluído, {nome}. Solarix agradece.")
        return nome,senha
    except Exception as e:
        print(f'Erro no registro: {e}')

def autenticar_usuario(nome,senha):
    try:
        print("\nAgora entre com sua conta: ")
        user = input("Digite seu nome: ")
        password = input("Digite a sua senha: ")
        if user == nome and password == senha:
            return True
        else:
            print('Os valores digitados estão incorretos. Cheque novamente.')
            autenticar_usuario(nome,senha)
    except Exception as e:
        print(f'Ocorreu um erro ao logar: {e}')

def grafico_horas():
    area_painel = 1.8 
    eficiencia_painel = 0.15  
    irradiancia_media = 800

    tempo_dia = np.arange(0, 24, 1)

    geracao_solar = area_painel * eficiencia_painel * irradiancia_media * np.cos(np.pi * (tempo_dia - 12) / 12)

    plt.plot(tempo_dia, geracao_solar, label="Energia Solar Gerada (kWh)")
    plt.title('Geração de Energia Solar ao Longo do Dia')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Energia Gerada (kWh)')
    plt.grid(True)
    plt.legend()
    plt.show()


dados = pd.read_csv('consumo-energia.csv')
dados['data_envio'] = pd.to_datetime(dados['data_envio'], errors='coerce')
dados = dados[['data_envio', 'consumo_mes_referencia']].dropna()


def graficoConsumo():

    plt.figure(figsize=(10, 6))
    plt.plot(dados['data_envio'], dados['consumo_mes_referencia'], marker='o', linestyle='-', color='b')

    plt.title('Consumo de Energia ao Longo do Tempo')
    plt.xlabel('Data de Envio')
    plt.ylabel('Consumo no Mês de Referência (kWh)')
    plt.xticks(rotation=45)

    plt.grid(True)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9)
    plt.show()


def exibir_menu():
    for opcao in opcoes_menu:
        print(opcao)


def obter_dados(cidade,api):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        return dados
    else:
        print("Erro ao buscar a cidade")
        return None


def calcular_dados(dados):

    valores = {
        'temperatura' : dados['main']['temp'],
        'humidade' : dados['main']['humidity'],
        'nuvens' : dados['clouds']['all'],
        'descricao' : dados['weather'][0]['description']
    }
    
    irradiacao = valores['temperatura'] * valores['humidade'] - valores['nuvens']
    area_media = 1.8
    energia = (irradiacao * area_media * valores['temperatura']) / 5
    
    print(f'Temperatura atual: {valores['temperatura']}')
    print(f'Humidade atual: {valores['humidade']}')
    print(f'Descricao da região: {valores['descricao']}')
    
    print(f'Produção estimada de energia solar por painel: {energia:.2f} Wh/dia')


def consultar_energia():
    cidade = input("Digite a cidade desejada: ")
    api = '5a7b99fcb1d59cfd1fdc012d3a16e09a'
    dados = obter_dados(cidade,api)
    print()
    calcular_dados(dados)

def verificar_opcao_menu():
    try:
        opcao = input('\nDigite o que gostaria de fazer: ')
        if opcao < '1' or opcao > '5':
            print('A opção não existe. Tente novamente.')
            return None
        return opcao
    except ValueError:
        print('O termo digitado é inválido. Tente novamente.')
        return None


def noticias_energia():
    api = '90af77575bcf4a47a7056bfa2f72b723'
    url = f'https://newsapi.org/v2/everything?q=energia%20solar&apiKey={api}'
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        noticias = dados['articles'][:5] 
        print("\nConfira as novas sobre Energia Solar e Sustentabilidade:\n")
        for noticia in noticias:
            print(f"Título: {noticia['title']}")
            print(f"Descrição: {noticia['description']}")
            print(f"Link: {noticia['url']}\n")
    else:
        print("Não foi possível buscar as notícias.")


def main():
    print("Bem vindo(a) a Solarix. O centro da futura solar.")
    nome, senha= registrar_usuario()
    autenticar_usuario(nome,senha)
    while True:
        print()
        print('=' * 65)
        exibir_menu()
        print('=' * 65)
        opcao = verificar_opcao_menu()
        if opcao == '1':
            consultar_energia()
        elif opcao == '2':
            noticias_energia()
        elif opcao == '3':
            grafico_horas()
        elif opcao == '4':
            graficoConsumo()
            print("O consumo da energia tende a aumentar a cada ano. Junte-se a Solarix para a transição de Energia Convencional para Solar.")
        elif opcao == '5':
            print(f"A Solarix agradece o seu uso, {nome}. Estamos aqui para priorizar a fonte solar e a sustentabilidade.")
            break


main()