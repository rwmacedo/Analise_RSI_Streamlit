import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
pd.options.mode.chained_assignment = None

st.title("Indicador RSI")
st.subheader("Vamos usar o indicador RSI para ver sinal de compra ou venda de ação")
st.subheader("Você pode consultar o ticker em https://finance.yahoo.com/")
st.write("ATENÇÃO: Isso é um treino de programação, não deve ser usado como indicação de investimento!!!")

# Usuário insere o ticker da ação
ticker = st.text_input("Qual o Ticker da ação que quer consultar?", key="ativo")

# Variável global para armazenar os dados do ativo
dados_ativo = None

# Botão para carregar os dados do ticker inserido
if st.button('Carregar dados'):
    if ticker:  # Verifica se o ticker foi inserido
        try:
            # Tenta baixar os dados do ativo
            dados_ativo = yf.download(ticker, start='2010-12-31')
            if not dados_ativo.empty:
                st.session_state['dados_ativo'] = dados_ativo  # Salva os dados no estado da sessão
                st.line_chart(dados_ativo['Adj Close'])

                # Calcula RSI e outras colunas necessárias
                dados_ativo['retornos'] = dados_ativo['Adj Close'].pct_change().dropna()
                dados_ativo['retornos_positivos'] = dados_ativo['retornos'].apply(lambda x: x if x>0 else 0)
                dados_ativo['retornos_negativos'] = dados_ativo['retornos'].apply(lambda x: abs(x) if x<0 else 0)
                dados_ativo['media_retornos_positivos'] = dados_ativo['retornos_positivos'].rolling(window=22).mean()
                dados_ativo['media_retornos_negativos'] = dados_ativo['retornos_negativos'].rolling(window=22).mean()
                dados_ativo['RSI'] = 100 - (100 / (1 + dados_ativo['media_retornos_positivos'] / dados_ativo['media_retornos_negativos']))
                dados_ativo['compra'] = 'não'
                dados_ativo.loc[dados_ativo['RSI'] < 30, 'compra'] = 'sim'
                dados_ativo['venda'] = 'não'
                dados_ativo.loc[dados_ativo['RSI'] > 70, 'venda'] = 'sim'
                                                
                st.line_chart(dados_ativo['RSI']) # Exibe o RSI no gráfico
            else:
                st.error("Não foi possível encontrar dados para o ticker fornecido.")
        except Exception as e:
            st.error(f"Erro ao baixar dados: {e}")
    else:
        st.error("Por favor, insira um ticker válido.")

# Botão para mostrar o sinal de compra
if st.button('Sinal de compra'):
    if 'dados_ativo' in st.session_state and not st.session_state['dados_ativo'].empty:
        # Pega os dados salvos no estado da sessão
        dados_ativo = st.session_state['dados_ativo']
        # Pega a última linha do DataFrame
        ultima_linha = dados_ativo.iloc[-1]
        data_ultima_linha = dados_ativo.index[-1].date()  # A data da última linha
        sinal_compra = ultima_linha['compra']
        st.write(f"{ticker}, Data: {data_ultima_linha}, Sinal de Compra: {sinal_compra}")
    else:
        st.error("Dados não carregados ou ticker inválido.")
        
if st.button('Sinal de venda'):
    if 'dados_ativo' in st.session_state and not st.session_state['dados_ativo'].empty:
        # Pega os dados salvos no estado da sessão
        dados_ativo = st.session_state['dados_ativo']
        # Pega a última linha do DataFrame
        ultima_linha = dados_ativo.iloc[-1]
        data_ultima_linha = dados_ativo.index[-1].date()  # A data da última linha
        sinal_venda = ultima_linha['venda']
        st.write(f"{ticker}, Data: {data_ultima_linha}, Sinal de venda: {sinal_venda}")
    else:
        st.error("Dados não carregados ou ticker inválido.")
        
