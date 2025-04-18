# Instruções para Implantação do Dashboard de Finanças Pessoais

Este documento contém instruções detalhadas para implantar o Dashboard de Finanças Pessoais como um site web permanente.

## Opção 1: Implantação no Streamlit Cloud (Recomendado)

O Streamlit Cloud é uma plataforma gratuita que permite hospedar aplicações Streamlit de forma simples e rápida.

1. Acesse [streamlit.io/cloud](https://streamlit.io/cloud) e crie uma conta gratuita
2. Conecte sua conta do GitHub (você precisará criar um repositório para o projeto)
3. Faça upload dos arquivos deste pacote para seu repositório GitHub
4. No Streamlit Cloud, clique em "New app"
5. Selecione seu repositório, o branch (geralmente "main") e defina o caminho do arquivo principal como "app.py"
6. Clique em "Deploy" e aguarde a implantação
7. Seu dashboard estará disponível em uma URL pública fornecida pelo Streamlit Cloud

## Opção 2: Implantação no Heroku

1. Crie uma conta no [Heroku](https://heroku.com)
2. Instale o [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. Extraia os arquivos deste pacote em uma pasta local
4. Abra um terminal na pasta e execute:
   ```
   heroku login
   git init
   git add .
   git commit -m "Initial commit"
   heroku create seu-app-nome
   git push heroku master
   ```
5. Seu dashboard estará disponível em `https://seu-app-nome.herokuapp.com`

## Opção 3: Implantação no Render

1. Crie uma conta no [Render](https://render.com)
2. Crie um novo repositório GitHub com os arquivos deste pacote
3. No Render, clique em "New Web Service"
4. Conecte seu repositório GitHub
5. Configure o serviço:
   - Nome: escolha um nome para seu dashboard
   - Ambiente: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `sh setup.sh && streamlit run app.py`
6. Clique em "Create Web Service"
7. Seu dashboard estará disponível na URL fornecida pelo Render

## Opção 4: Execução Local

Para executar o dashboard localmente:

1. Extraia os arquivos deste pacote em uma pasta local
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Execute o dashboard:
   ```
   streamlit run app.py
   ```
4. O dashboard estará disponível em `http://localhost:8501`

## Estrutura de Arquivos

- `app.py`: Arquivo principal do dashboard
- `extrator_ofx.py`: Script para extrair dados dos arquivos OFX
- `categorizador.py`: Script para categorizar transações
- `requirements.txt`: Lista de dependências
- `setup.sh`: Script de configuração para implantação
- `Procfile`: Arquivo de configuração para Heroku
- `.streamlit/config.toml`: Configurações do Streamlit
- `extratos/`: Pasta para armazenar arquivos OFX

## Personalização

Você pode personalizar o dashboard editando os seguintes arquivos:

- `app.py`: Interface do dashboard
- `categorizador.py`: Regras de categorização
- `.streamlit/config.toml`: Tema e aparência

## Suporte

Se precisar de ajuda com a implantação, consulte a documentação oficial das plataformas:

- [Documentação do Streamlit Cloud](https://docs.streamlit.io/streamlit-cloud)
- [Documentação do Heroku](https://devcenter.heroku.com/categories/python-support)
- [Documentação do Render](https://render.com/docs)
