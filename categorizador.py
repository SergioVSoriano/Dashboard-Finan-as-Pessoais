import pandas as pd

# Lista de categorias disponíveis
CATEGORIAS = [
    "Alimentação", "Receitas", "Saúde", "Mercado", "Educação", "Compras", "Transporte", 
    "Investimento", "Transferências para terceiros", "Telefone", "Moradia"
]

def categorizar_transacao(descricao, valor):
    """
    Categoriza uma transação usando regras predefinidas.
    """
    descricao_lower = descricao.lower() if isinstance(descricao, str) else ""
    
    # Valores positivos são receitas
    if valor > 0:
        return "Receitas"
    
    # Regras baseadas em palavras-chave
    if "pix" in descricao_lower and ("enviado" in descricao_lower or "transferido" in descricao_lower):
        return "Transferências para terceiros"
    if any(keyword in descricao_lower for keyword in ["uber", "99app", "taxi", "recargapay", "cartvem", "passagem"]):
        return "Transporte"
    if any(keyword in descricao_lower for keyword in ["restaurante", "pizzaria", "burguer", "food", "supermercado"]):
        return "Alimentação"
    if any(keyword in descricao_lower for keyword in ["farmacia", "drogaria", "hospital", "clinica"]):
        return "Saúde"
    if any(keyword in descricao_lower for keyword in ["escola", "curso", "livro", "educacao", "faculdade"]):
        return "Educação"
    if any(keyword in descricao_lower for keyword in ["telefone", "celular", "tim", "vivo"]):
        return "Telefone"
    if any(keyword in descricao_lower for keyword in ["aluguel", "condominio", "agua", "luz"]):
        return "Moradia"
    if any(keyword in descricao_lower for keyword in ["investimento", "aplicacao", "tesouro", "acao", "fundo"]):
        return "Investimento"
    
    # Se nenhuma regra se aplicar, retornar 'Outros'
    return "Outros"

def categorizar_transacoes(df):
    """
    Aplica a categorização em cada transação do DataFrame.
    """
    df['Categoria'] = df.apply(lambda row: categorizar_transacao(row['Descricao'], row['Valor']), axis=1)
    return df

