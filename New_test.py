#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
####### Load Dataset #####################
bets=pd.read_csv('bets.csv', index_col='id')
matches=pd.read_csv('matches.csv', nrows=48)
bets['score']=bets['HomeTeamScore'].astype('str')+"x"+bets['AwayTeamScore'].astype('str')
matches['match']=matches['MatchNumber'].astype(str)+"-"+matches['HomeTeam']+ " x "+matches['AwayTeam']
completo=pd.read_csv('users_completo.csv')
bets=pd.merge(bets, completo, left_on='punter_username',right_on='username', how='left')
bets=bets[['id','game_number', 'HomeTeamScore', 'AwayTeamScore', 'punter_username',
        'name','score' ]]
bets.rename(columns={"name": "Nome", "score": "Placar"}, inplace=True)
########################################################
st.set_page_config(layout="wide")

st.markdown("## Palpites da galera")   ## Main Title

################# Scatter Chart Logic #################

st.sidebar.markdown("### Selecione a pelada desejada")


Jogo = st.sidebar.selectbox("Jogo", matches['match'].to_list())
#################################################################
game_selected=matches[matches['match']==Jogo]['MatchNumber'].tolist()
bets_selected=bets[bets['game_number']==game_selected[0]]
bar_fig=plt.figure(figsize=(10,5))
ax=sns.countplot(x=bets_selected['Placar'], color='red',edgecolor='blue', order=bets_selected['Placar'].value_counts().index)
ax.bar_label(ax.containers[0])
plt.xlabel('Placar')
plt.ylabel('Número de apostas')

##################### Layout Application ##################

container1 = st.container()
with container1:
    bar_fig
    

