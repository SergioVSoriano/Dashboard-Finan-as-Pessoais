import streamlit as st
import pandas as pd
from ofxparse import OfxParser
import os

# Função para extrair dados do arquivo OFX
def extrair_dados_ofx(ofx_file_path):
    try:
        # Abrir e processar o arquivo OFX
        with open(ofx_file_path, 'r', encoding='utf-8') as file:
            ofx = OfxParser.parse(file)
        
        # Verificar se há contas no arquivo OFX
        if not ofx.accounts:
            raise ValueError("Nenhuma conta encontrada no arquivo OFX.")
        
        # Extrair transações
        transacoes = []
        for conta in ofx.accounts:
            for transacao in conta.statement.transactions:
                # Adicionar as transações em uma lista de dicionários
                transacoes.append({
                    "Data": transacao.date.strftime('%Y-%m-%d'),  # Formatar a data
                    "Tipo": transacao.type.capitalize(),  # Capitalizar o tipo (ex.: Debit -> Debit)
                    "Valor": transacao.amount,
                    "Descrição": transacao.memo
                })
        
        # Verificar se há transações
        if not transacoes:
            raise ValueError("Nenhuma transação encontrada no arquivo OFX.")
        
        # Converter para DataFrame
        df = pd.DataFrame(transacoes)
        return df

    except Exception as e:
        raise ValueError(f"Erro ao processar o arquivo OFX: {e}")

# Função para categorizar automaticamente os gastos
def categorizar(transacoes):
    categorias = {
        "Alimentação": ["RESTAURANTE", "PADARIA", "PIZZA", "HAMBURGUER", "LANCHONETE", "FRUTAS"],
        "Receitas": ["RECEBIDO", "DEPÓSITO", "PIX RECEBIDO", "PAGAMENTO RECEBIDO"],
        "Saúde": ["FARMÁCIA", "HOSPITAL"],
        "Mercado": ["SUPERMERCADO", "MERCADO", "CARREFOUR", "BIG", "ZAFFARI"],
        "Educação": ["ESCOLA", "UNIVERSIDADE", "EDUCAÇÃO"],
        "Compras": ["COMPRA", "SHOPPING", "MAGAZINE", "AMAZON"],
        "Transporte": ["UBER", "99", "GASOLINA", "COMBUSTÍVEL", "POSTO"],
        "Investimento": ["TESOURO", "RENDA FIXA", "CDB", "AÇÃO"],
        "Transferências para terceiros": ["PIX ENVIADO", "TRANSFERÊNCIA", "DOC", "TED"],
        "Telefone": ["CLARO", "VIVO", "TIM", "OI"],
        "Moradia": ["ALUGUEL", "ENERGIA", "LUZ", "ÁGUA", "CONDOMÍNIO"]
    }

    def identificar_categoria(descricao):
        descricao_upper = descricao.upper()
        for categoria, palavras in categorias.items():
            if any(palavra in descricao_upper for palavra in palavras):
                return categoria
        return "Outros"

    transacoes["Categoria"] = transacoes["Descrição"].apply(identificar_categoria)
    return transacoes

# Função principal
def main():
    st.title("Dashboard de Finanças Pessoais")
    
    # Caminho do arquivo OFX
    ofx_file_path = r'c:\Users\Sérgio Soriano\Downloads\DFN\dashboard-financas-nubank-main\extratos\Nubank_2025-04-07.ofx'
    
    # Verificar se o arquivo OFX existe
    if not os.path.exists(ofx_file_path):
        st.error(f"Arquivo OFX não encontrado: {ofx_file_path}")
        return
    
    try:
        # Carregar os dados do arquivo OFX
        df = extrair_dados_ofx(ofx_file_path)
        
        # Categorização dos gastos
        df = categorizar(df)
        
        # Verifique se o DataFrame não está vazio
        if df.empty:
            st.error("Erro ao carregar os dados. O arquivo OFX está vazio ou inválido.")
            return
        
        # Exibir o DataFrame resultante no Streamlit
        st.write("Transações extraídas do arquivo OFX:")
        st.dataframe(df)
        
        # Exibir a distribuição dos gastos por categoria
        categoria_agrupada = df.groupby("Categoria")["Valor"].sum().reset_index()
        categoria_agrupada = categoria_agrupada[categoria_agrupada["Valor"] < 0]  # Somente gastos
        categoria_agrupada["Valor"] = categoria_agrupada["Valor"].abs()
        
        st.subheader("Distribuição dos Gastos por Categoria")
        st.bar_chart(categoria_agrupada.set_index('Categoria')['Valor'])
    
    except FileNotFoundError:
        st.error("O arquivo OFX não foi encontrado. Verifique o caminho e tente novamente.")
    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}")

# Iniciar o Streamlit
if __name__ == "__main__":
    main()







