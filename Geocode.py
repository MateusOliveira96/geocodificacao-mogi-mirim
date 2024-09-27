import requests
import pandas as pd
import time
import unicodedata

# Sua chave de API do Geoapify
API_KEY = "SuaChave"

# Dicionário de abreviações
abreviacoes = {
    "AV.": "Avenida",
    "R.": "Rua",
    "PRAÇA": "Praça",
    "JD.": "Jardim",
    "PQ.": "Parque",
    "C.": "Centro",
    "VILA": "Vila",
    "AVDA.": "Avenida",
    "ROD.": "Rodovia",
    "TUC.": "Tucura",
    "R. DR.": "Rua Doutor",
    "R. PADRE": "Rua Padre",
    "N.": "Nova",
    "S.": "Santa",
    "B.": "Bairro",
    "ESTR.": "Estrada",
    "P.": "Parque",
}

# Função para remover acentuações dos endereços
def remover_acentuacao(texto):
    if isinstance(texto, str):  # Verifica se é uma string
        texto_normalizado = unicodedata.normalize('NFD', texto)
        texto_sem_acento = ''.join(char for char in texto_normalizado if unicodedata.category(char) != 'Mn')
        return texto_sem_acento
    return texto  # Se não for string, retorna o valor original

# Função para expandir abreviações
def expandir_abreviacoes(endereco):
    if pd.isna(endereco):  # Verifica se o endereço é NaN
        return endereco  # Retorna NaN sem fazer nada
    for abr, completo in abreviacoes.items():
        endereco = endereco.replace(abr, completo)
    return endereco

# Função para geocodificar endereços usando Geoapify
def geocode_endereco(endereco):
    try:
        # URL da API do Geoapify
        url = f"https://api.geoapify.com/v1/geocode/search?text={endereco}&apiKey={API_KEY}"

        # Faz a solicitação
        response = requests.get(url)

        # Verifica o status da resposta
        if response.status_code == 200:
            data = response.json()
            # Se houver resultados, retorna latitude e longitude
            if data['features']:
                latitude = data['features'][0]['geometry']['coordinates'][1]
                longitude = data['features'][0]['geometry']['coordinates'][0]
                return latitude, longitude
            else:
                print(f"Endereço não encontrado: {endereco}")
                return None, None
        else:
            print(f"Erro na solicitação: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"Erro ao geocodificar {endereco}: {e}")
        return None, None

# Carrega o arquivo CSV local
csv_file = 'SeuArquivo.csv'
df = pd.read_csv(csv_file)

# Checa o nome correto nas colunas do DF
print(df.columns)

# Cria os endereços completos sem o bairro e remove a acentuação, ajustar de acordo com seu arquivo csv
df['Endereço completo'] = df['LOGRADOURO'] + ',' + df['CEP']
df['Endereço completo'] = df['Endereço completo'].apply(remover_acentuacao)

# Define o tamanho do bloco e o tempo de espera
block_size = 50
wait_time = 10  # segundos

# Listas para armazenar resultados
resultados = []

# Faz o loop pelo DF em blocos de 50
for start_row in range(0, len(df), block_size):
    end_row = min(start_row + block_size - 1, len(df) - 1)  # Limita a última linha
    for index in range(start_row, end_row + 1):
        endereco = df.at[index, 'Endereço completo']
        endereco_expandidos = expandir_abreviacoes(endereco)
        latitude, longitude = geocode_endereco(endereco_expandidos)

        # Adiciona os resultados à lista
        resultados.append({
            'Endereço': endereco,
            'Latitude': latitude,
            'Longitude': longitude,
            'Encontrado': latitude is not None and longitude is not None  # Verifica se as coordenadas foram encontradas
        })

    # Espera o tempo definido
    time.sleep(wait_time)

# Cria um DataFrame com os resultados
df_resultados = pd.DataFrame(resultados)

# Salva o DataFrame como um arquivo CSV
df_resultados.to_csv('EndereçosGeocodificados.csv', index=False)

print("Geocodificação concluída. Resultados salvos em 'EndereçosGeocodificados.csv'.")
