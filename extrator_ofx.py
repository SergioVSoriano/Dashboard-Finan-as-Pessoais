import pandas as pd
from ofxparse import OfxParser

def extrair_dados_ofx(ofx_file_path):
    """
    Extrai dados de transações financeiras de um arquivo OFX e os converte para um DataFrame.
    """
    try:
        # Lê o arquivo OFX
        with open(ofx_file_path, 'r') as ofx_file:
            ofx = OfxParser.parse(ofx_file)
        
        # Extração das transações de cartão de crédito ou conta corrente
        transacoes = []
        for transaction in ofx.account.statement.transactions:
            transacoes.append({
                'Data': transaction.date,
                'Descricao': transaction.name,
                'Valor': transaction.amount
            })
        
        # Cria um DataFrame com as transações extraídas
        df = pd.DataFrame(transacoes)
        return df
    except Exception as e:
        print(f"Erro ao ler o arquivo OFX: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro
