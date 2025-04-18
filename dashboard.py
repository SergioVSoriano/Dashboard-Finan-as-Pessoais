import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import datetime
import json
from extrator_ofx import extrair_dados_ofx
from categorizador import categorizar_transacoes, aplicar_categorias_salvas, carregar_categorias, salvar_categorias, categorizar_manualmente

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Finanças Pessoais",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar estilo personalizado
st.markdown("""
<style>
    .main {
        background-color: #121214;
    }
    .st-emotion-cache-16txtl3 h1, .st-emotion-cache-16txtl3 h2, .st-emotion-cache-16txtl3 h3, .st-emotion-cache-16txtl3 h4 {
        color: #8257e5;
    }
    .st-emotion-cache-16txtl3 {
        color: #ffffff;
    }
    .stButton>button {
        background-color: #8257e5;
        color: white;
    }
    .stButton>button:hover {
        background-color: #6c45d9;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Função para carregar os dados de exemplo
def carregar_dados_exemplo():
    # Verifica se existem arquivos OFX na pasta extratos
    if not os.path.exists('extratos') or not any(f.endswith('.ofx') for f in os.listdir('extratos')):
        st.warning("Usando dados de exemplo para demonstração.")
        # Criar dados de exemplo
        data = {
            'Data': pd.date_range(start='2025-01-01', periods=30),
            'Valor': [-50.0, -120.0, -35.0, -80.0, -25.0, 1500.0, -45.0, -60.0, -90.0, -30.0,
                     -70.0, -40.0, -55.0, -65.0, -85.0, -95.0, -15.0, -75.0, -20.0, -110.0,
                     -130.0, -45.0, -55.0, -25.0, -35.0, -65.0, -75.0, -85.0, -95.0, 2000.0],
            'Descrição': ['Uber', 'Supermercado', 'Farmácia', 'Restaurante', 'Café', 'Salário', 
                         'Transporte', 'Internet', 'Aluguel', 'Telefone', 'Shopping', 'Livros',
                         'Cinema', 'Lanchonete', 'Roupas', 'Eletrônicos', 'Padaria', 'Móveis',
                         'Estacionamento', 'Viagem', 'Conserto', 'Uber', 'Lanchonete', 'Café',
                         'Farmácia', 'Internet', 'Móveis', 'Roupas', 'Eletrônicos', 'Bônus'],
            'Categoria': ['Transporte', 'Alimentação', 'Saúde', 'Alimentação', 'Alimentação', 'Receitas',
                         'Transporte', 'Moradia', 'Moradia', 'Telefone', 'Compras', 'Educação',
                         'Compras', 'Alimentação', 'Compras', 'Compras', 'Alimentação', 'Compras',
                         'Transporte', 'Compras', 'Compras', 'Transporte', 'Alimentação', 'Alimentação',
                         'Saúde', 'Moradia', 'Compras', 'Compras', 'Compras', 'Receitas']
        }
        return pd.DataFrame(data)
    else:
        # Extrai os dados dos arquivos OFX
        df = extrair_dados_ofx()
        
        if df.empty:
            st.error("Nenhum dado encontrado nos arquivos OFX.")
            return pd.DataFrame()
        
        # Carrega categorias salvas
        categorias_salvas = carregar_categorias()
        
        # Aplica categorias salvas
        df = aplicar_categorias_salvas(df, categorias_salvas)
        
        # Categoriza as transações restantes
        df = categorizar_transacoes(df)
        
        # Salva as categorias atualizadas
        salvar_categorias(df)
        
        return df

# Função para filtrar os dados por mês
def filtrar_por_mes(df, mes_selecionado):
    if mes_selecionado == "Todos":
        return df
    
    # Extrai o ano e mês da string selecionada (formato: YYYY-MM)
    ano, mes = map(int, mes_selecionado.split('-'))
    
    # Filtra o DataFrame
    df_filtrado = df[
        (df['Data'].dt.year == ano) & 
        (df['Data'].dt.month == mes)
    ]
    
    return df_filtrado

# Função para filtrar por categoria
def filtrar_por_categoria(df, categoria_selecionada):
    if categoria_selecionada == "Todas":
        return df
    
    return df[df['Categoria'] == categoria_selecionada]

# Função para criar gráfico de distribuição por categoria
def criar_grafico_categorias(df):
    # Agrupa por categoria e soma os valores (considerando apenas valores negativos)
    df_neg = df[df['Valor'] < 0].copy()
    
    if df_neg.empty:
        st.warning("Não há despesas no período selecionado.")
        return None
    
    # Agrupa por categoria e calcula a soma dos valores absolutos
    df_cat = df_neg.groupby('Categoria')['Valor'].sum().abs().reset_index()
    df_cat.columns = ['Categoria', 'Total']
    
    # Calcula o total geral para percentuais
    total_geral = df_cat['Total'].sum()
    
    # Adiciona coluna de percentual
    df_cat['Percentual'] = (df_cat['Total'] / total_geral * 100).round(1)
    
    # Ordena por valor total
    df_cat = df_cat.sort_values('Total', ascending=False)
    
    # Cria o gráfico de pizza
    fig = px.pie(
        df_cat, 
        values='Total', 
        names='Categoria',
        title='Distribuição por Categoria',
        color_discrete_sequence=px.colors.qualitative.Set3,
        hover_data=['Percentual']
    )
    
    # Atualiza o layout
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Valor: R$ %{value:.2f}<br>Percentual: %{customdata[0]:.1f}%'
    )
    
    # Adiciona anotação com o valor total
    fig.add_annotation(
        text=f"Total: R$ {total_geral:.2f}",
        x=0.5,
        y=-0.1,
        showarrow=False,
        font=dict(size=14)
    )
    
    return fig

# Função para criar gráfico de evolução mensal
def criar_grafico_evolucao(df):
    # Converte a coluna de data para datetime se não for
    if not pd.api.types.is_datetime64_dtype(df['Data']):
        df['Data'] = pd.to_datetime(df['Data'])
    
    # Cria uma coluna de ano-mês
    df['Ano-Mês'] = df['Data'].dt.strftime('%Y-%m')
    
    # Agrupa por ano-mês e categoria, somando os valores
    df_mensal = df.groupby(['Ano-Mês', 'Categoria'])['Valor'].sum().reset_index()
    
    # Separa receitas e despesas
    df_receitas = df_mensal[df_mensal['Valor'] > 0].copy()
    df_despesas = df_mensal[df_mensal['Valor'] < 0].copy()
    df_despesas['Valor'] = df_despesas['Valor'].abs()  # Converte para positivo para visualização
    
    # Cria o gráfico de barras agrupadas
    fig = go.Figure()
    
    # Adiciona as receitas
    fig.add_trace(go.Bar(
        x=df_receitas['Ano-Mês'],
        y=df_receitas['Valor'],
        name='Receitas',
        marker_color='green'
    ))
    
    # Adiciona as despesas
    fig.add_trace(go.Bar(
        x=df_despesas['Ano-Mês'],
        y=df_despesas['Valor'],
        name='Despesas',
        marker_color='red'
    ))
    
    # Atualiza o layout
    fig.update_layout(
        title='Evolução Mensal de Receitas e Despesas',
        xaxis_title='Mês',
        yaxis_title='Valor (R$)',
        barmode='group',
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

# Função principal
def main():
    # Título do dashboard
    st.title("Dashboard de Finanças Pessoais")
    
    # Informação sobre a aplicação
    st.markdown("""
    Este dashboard permite visualizar e analisar suas finanças pessoais a partir de extratos do Nubank.
    """)
    
    # Carrega os dados
    df = carregar_dados_exemplo()
    
    if df.empty:
        return
    
    # Converte a coluna de data para datetime se não for
    if not pd.api.types.is_datetime64_dtype(df['Data']):
        df['Data'] = pd.to_datetime(df['Data'])
    
    # Sidebar para filtros
    st.sidebar.title("Filtros")
    
    # Lista de meses disponíveis
    meses_disponiveis = df['Data'].dt.strftime('%Y-%m').unique().tolist()
    meses_disponiveis.sort(reverse=True)  # Ordena do mais recente para o mais antigo
    meses_disponiveis = ["Todos"] + meses_disponiveis
    
    # Filtro de mês
    mes_selecionado = st.sidebar.selectbox("Mês", meses_disponiveis)
    
    # Filtra os dados por mês
    df_filtrado = filtrar_por_mes(df, mes_selecionado) if mes_selecionado != "Todos" else df
    
    # Lista de categorias disponíveis
    categorias_disponiveis = ["Todas"] + sorted(df['Categoria'].unique().tolist())
    
    # Filtro de categoria
    categoria_selecionada = st.sidebar.selectbox("Categoria", categorias_disponiveis)
    
    # Filtra os dados por categoria
    df_filtrado = filtrar_por_categoria(df_filtrado, categoria_selecionada) if categoria_selecionada != "Todas" else df_filtrado
    
    # Divide a tela em duas colunas
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Exibe a tabela de transações
        st.subheader("Transações")
        st.dataframe(
            df_filtrado[['Data', 'Valor', 'Descrição', 'Categoria']].sort_values('Data', ascending=False),
            use_container_width=True,
            hide_index=True
        )
        
        # Resumo financeiro
        st.subheader("Resumo Financeiro")
        
        # Calcula receitas e despesas
        receitas = df_filtrado[df_filtrado['Valor'] > 0]['Valor'].sum()
        despesas = df_filtrado[df_filtrado['Valor'] < 0]['Valor'].sum()
        saldo = receitas + despesas  # despesas já são negativas
        
        # Cria três colunas para exibir os valores
        col_receitas, col_despesas, col_saldo = st.columns(3)
        
        with col_receitas:
            st.metric("Receitas", f"R$ {receitas:.2f}")
        
        with col_despesas:
            st.metric("Despesas", f"R$ {abs(despesas):.2f}")
        
        with col_saldo:
            st.metric("Saldo", f"R$ {saldo:.2f}", delta=f"{saldo:.2f}")
    
    with col2:
        # Gráfico de distribuição por categoria
        st.subheader("Distribuição por Categoria")
        fig_categorias = criar_grafico_categorias(df_filtrado)
        if fig_categorias:
            st.plotly_chart(fig_categorias, use_container_width=True)
    
    # Gráfico de evolução mensal
    st.subheader("Evolução Mensal")
    fig_evolucao = criar_grafico_evolucao(df)
    st.plotly_chart(fig_evolucao, use_container_width=True)
    
    # Informações sobre o projeto
    st.markdown("---")
    st.markdown("""
    ### Sobre o Projeto
    
    Este dashboard foi desenvolvido para ajudar na análise de finanças pessoais, permitindo visualizar gastos, receitas e tendências ao longo do tempo.
    
    **Funcionalidades:**
    - Visualização de transações
    - Filtros por mês e categoria
    - Resumo financeiro
    - Gráficos de distribuição e evolução
    
    **Tecnologias utilizadas:**
    - Python
    - Streamlit
    - Pandas
    - Plotly
    """)

if __name__ == "__main__":
    main()
