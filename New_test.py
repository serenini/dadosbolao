#!/usr/bin/env python
# coding: utf-8

# In[1]:


import seaborn as sns
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
####### Load Dataset #####################
bets=pd.read_csv('bets.csv', index_col='id')
matches=pd.read_csv('matches.csv', nrows=48)
completo=pd.read_json("http://vaiteqatar.online:8000/users")
ligas=pd.read_json("http://vaiteqatar.online:8000/bet_groups")
leagues={}
for i in range(len(ligas)):
    leagues[ligas['name'][i]]=pd.json_normalize(ligas['players'][i])
##### Manipulate datasets

bets['score']=bets['HomeTeamScore'].astype('str')+"x"+bets['AwayTeamScore'].astype('str')
matches['match']=matches['MatchNumber'].astype(str)+"-"+matches['HomeTeam']+ " x "+matches['AwayTeam']
bets=pd.merge(bets, completo, left_on='punter_username',right_on='username', how='left')
bets=bets[['id','game_number', 'HomeTeamScore', 'AwayTeamScore', 'punter_username',
        'name','score' ]]
bets.rename(columns={"name": "Nome", "score": "Placar"}, inplace=True)

########################################################
st.set_page_config(layout="wide")

st.markdown("## Palpites da galera")   ## Main Title
Jogo = st.selectbox("Selecione a pelada desejada", matches['match'].to_list())
game_selected=matches[matches['match']==Jogo]['MatchNumber'].tolist()
bets_selected=bets[bets['game_number']==game_selected[0]]
#################################################################
bar_fig=plt.figure(figsize=(8,4))
ax=sns.countplot(x=bets_selected['Placar'], color='red',edgecolor='blue', order=bets_selected['Placar'].value_counts().index)
ax.bar_label(ax.containers[0])
plt.xlabel('Placar')
plt.ylabel('Número de apostas')
plt.title (Jogo)
bar_fig
#################################################################
st.markdown("#### Filtre o placar pra vem quem tá cravando")
Placar_selecionado = st.selectbox("Placar", ["TODOS"]+bets_selected.sort_values('Placar')['Placar'].unique().tolist())
st.markdown("### Filtre por liga e ligue o secador")
liga_selecionada = st.selectbox("Liga", list(ligas['name']))
#################################################################
bets_selected=bets_selected[bets_selected['id'].isin(leagues[liga_selecionada]['id'])]
if Placar_selecionado=="TODOS":
    bets_selected_2=bets_selected
else:
    bets_selected_2=bets_selected[bets_selected['Placar']==Placar_selecionado]
bets_selected_2[['Nome','Placar']]

