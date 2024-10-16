import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_table("data/gas.tsv")
df['DATA INICIAL'] = pd.to_datetime(df['DATA INICIAL'])

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
   
   return round(df[mask]['PREÇO MÉDIO REVENDA'].mean(), 2), df[mask]['COEF DE VARIAÇÃO DISTRIBUIÇÃO']

price_regiao_df = pd.DataFrame({
   'REGIÃO': regions,
   'PREÇO MÉDIO': [median_price(region)[0] for region in regions],
   'COEF VARIAÇÃO': [median_price(region[1]) for region in regions]
})

# st.subheader("Coeficientes de variação de preço por região")
# price_regiao_df['COEF VARIAÇÃO']
# price_variation = st.metric(label="Norte", value=price_regiao_df['COEF VARIAÇÃO'].values)

st.subheader('Preço X Região')
st.bar_chart(price_regiao_df, x='REGIÃO', y='PREÇO MÉDIO', x_label='Região', y_label='Preço')

st.divider()