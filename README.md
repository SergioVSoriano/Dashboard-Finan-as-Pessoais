# Dashboard de Finanças Pessoais - Nubank

Este projeto consiste em um dashboard de finanças pessoais que extrai automaticamente dados de extratos do Nubank (arquivos OFX), categoriza as transações e apresenta visualizações interativas usando Streamlit.

## Funcionalidades

- **Extração automática de dados OFX**: Lê arquivos OFX do Nubank e extrai as transações
- **Categorização automática**: Classifica as transações em categorias como Alimentação, Transporte, Compras, etc.
- **Dashboard interativo**: Interface gráfica para visualizar e analisar suas finanças
- **Filtros por mês e categoria**: Permite filtrar as transações por período e tipo
- **Gráficos e resumos**: Visualizações de distribuição de gastos e evolução mensal
- **Categorização manual**: Possibilidade de ajustar manualmente as categorias das transações

## Estrutura do Projeto

- `extrator_ofx.py`: Script para extrair dados dos arquivos OFX
- `categorizador.py`: Script para categorizar automaticamente as transações
- `dashboard.py`: Aplicação Streamlit para visualização dos dados
- `extratos/`: Pasta onde devem ser colocados os arquivos OFX do Nubank
- `categorias.json`: Arquivo que armazena as regras de categorização aprendidas

## Requisitos

- Python 3.10 ou superior
- Bibliotecas: ofxparse, pandas, streamlit, plotly, matplotlib

## Instalação

1. Clone este repositório ou baixe os arquivos
2. Instale as dependências:

```bash
pip install ofxparse pandas streamlit plotly matplotlib
```

## Como Usar

1. Coloque seus arquivos OFX do Nubank na pasta `extratos/`
2. Execute o dashboard:

```bash
cd nubank_dashboard
streamlit run dashboard.py
```

3. Acesse o dashboard no navegador (geralmente em http://localhost:8501)

## Categorização de Transações

O sistema categoriza automaticamente as transações com base em palavras-chave presentes na descrição:

- **Receitas**: Valores positivos
- **Transferências para terceiros**: Transações com "pix" e "enviado"
- **Transporte**: Transações com "uber", "99app", "taxi", etc.
- **Alimentação**: Transações com "restaurante", "pizzaria", "supermercado", etc.
- **Compras**: Categoria padrão para despesas não identificadas

Você pode ajustar manualmente as categorias usando a seção "Categorização Manual" no dashboard.

## Personalização

Você pode personalizar as regras de categorização editando a função `categorizar_transacao()` no arquivo `categorizador.py`.

## Limitações

- O sistema funciona apenas com arquivos OFX do Nubank
- A categorização automática é baseada em regras simples de palavras-chave
- Não há sincronização automática com a conta do Nubank (é necessário baixar manualmente os extratos)

## Próximos Passos

- Implementar sincronização automática com a API do Nubank
- Melhorar o algoritmo de categorização usando aprendizado de máquina
- Adicionar mais visualizações e análises financeiras
- Implementar previsões de gastos futuros

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.
