import streamlit as st
import pandas as pd
import numpy as np

# Cleaning DataBase
df = pd.read_table("data/gas.tsv")
df['DATA INICIAL'] = pd.to_datetime(df['DATA INICIAL'])
df['COEF DE VARIAÇÃO DISTRIBUIÇÃO'] = pd.to_numeric(df['COEF DE VARIAÇÃO DISTRIBUIÇÃO'].replace('-', None)) 
df['COEF DE VARIAÇÃO DISTRIBUIÇÃO'] =  df['COEF DE VARIAÇÃO DISTRIBUIÇÃO'] < 0


# Start
st.title("Variação do Preço do Gas - Brasil")
st.write(df.head(100))
year_range = st.slider('Selecione o período desejado', value=[2004, 2021], max_value=2021, min_value=2004)
st.divider()

# Compare price between regions (Norte, Sul, Nordeste, etc...)
regions = ['NORTE', 'SUL', 'NORDESTE', 'SUDESTE', 'CENTRO OESTE']

def median_price(region):
   mask = (
      (df['REGIÃO'] == region) &
      (df['DATA INICIAL'].dt.year >= year_range[0]) &
      (df['DATA INICIAL'].dt.year <= year_range[1])
   )
   
   return round(df[mask]['PREÇO MÉDIO REVENDA'].mean(), 2)

price_regiao_df = pd.DataFrame({
   'REGIÃO': regions,
   'PREÇO MÉDIO': [median_price(region) for region in regions],
   # 'COEF VARIAÇÃO': [median_price(region[1]) for region in regions]
})

price_variation = round(df['COEF DE VARIAÇÃO DISTRIBUIÇÃO'].mean(), 2)

st.subheader("Métricas")
st.metric(label="Coeficientes de variação de preço", value=price_variation)
st.metric(label="Média de preço - Norte", value=round(price_regiao_df['PREÇO MÉDIO'][0].mean(), 2))
st.metric(label="Média de preço - Sul", value=round(price_regiao_df['PREÇO MÉDIO'][1].mean(), 2))
st.metric(label="Média de preço - Nordeste", value=round(price_regiao_df['PREÇO MÉDIO'][2].mean(), 2))
st.metric(label="Média de preço - Sudeste", value=round(price_regiao_df['PREÇO MÉDIO'][3].mean(), 2))
st.metric(label="Média de preço - Centro Oeste", value=round(price_regiao_df['PREÇO MÉDIO'][4].mean(), 2))   


st.subheader('Preço X Região')
st.bar_chart(price_regiao_df, x='REGIÃO', y='PREÇO MÉDIO', x_label='Região', y_label='Preço')

st.divider()