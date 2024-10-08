# Instruções para Uso do Código de Geocodificação

Este código foi desenvolvido para geocodificar endereços utilizando a API da Geoapify, processando grandes volumes de dados de maneira eficiente. Abaixo estão as instruções para rodar o código:

## Pré-requisitos
- Python 3.x instalado no seu sistema.

## Bibliotecas Python necessárias:
```bash
requests
pandas
time
unicodedata
```

Você pode instalá-las utilizando o seguinte comando:
```bash
pip install pandas requests
```

## Chave de API do Geoapify:
Crie uma conta gratuita no Geoapify e obtenha sua chave de API. Substitua **"SUA_CHAVE_API"** pelo valor da sua chave no código.

## Arquivo CSV com endereços:
Certifique-se de que o arquivo CSV tenha uma coluna chamada **LOGRADOURO** contendo os nomes das ruas e uma coluna **CEP** com os códigos postais. O nome do arquivo deve ser ajustado no trecho:
```python
csv_file = 'SeuArquivo.csv'
df = pd.read_csv(csv_file)
```

## Passo a Passo
1. **Baixe o código-fonte:** Acesse o repositório do código aqui https://github.com/MateusOliveira96/geocodificacao-mogi-mirim.git e faça o download ou clone o repositório.
2. **Prepare seu arquivo CSV de entrada:** Certifique-se de que o arquivo com os endereços esteja no mesmo diretório que o código Python ou ajuste o caminho do arquivo CSV no código.
3. **Adicione sua chave de API:** No código, substitua a string **API_KEY** pela sua chave de API:
   ```python
   API_KEY = "SUA_CHAVE_API"
   ```
4. **Executando o código:** Abra um terminal no diretório onde o código está salvo e execute:
   ```bash
   python geocodificacao_mogi_mirim.py
   ```

## Processamento em Blocos:
O código processa os endereços em blocos de 50 linhas por vez, aguardando 10 segundos entre cada bloco para evitar ultrapassar o limite de requisições da API.

## Resultados:
Após a execução, será gerado um arquivo CSV chamado **EndereçosGeocodificados.csv**, contendo:
- Endereço processado
- Latitude
- Longitude
- Indicador se o endereço foi encontrado ou não

## Customizações
### Expansão de Abreviações:
O código já expande abreviações comuns de logradouros. Você pode personalizar o dicionário de abreviações modificando a variável **abreviacoes** no início do código.

### Tempo de Espera entre Blocos:
Se necessário, ajuste o tempo de espera entre blocos para evitar sobrecarga na API:
```python
wait_time = 10 # em segundos
```

Seguindo esses passos, você poderá utilizar o código para geocodificar grandes volumes de endereços de forma eficiente.

