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
completo=pd.read_csv('users_completo.csv')
ligas=pd.read_json("http://vaiteqatar.online:8000/bet_groups")
leagues={}
for i in range(len(ligas)):
    leagues[ligas['name'][i]]=pd.json_normalize(ligas['players'][i])
##### Manipulate datasets
bets=pd.read_csv('https://raw.githubusercontent.com/serenini/dadosbolao/main/bets.csv', index_col='id')
scores=pd.read_csv('game_scores.csv')
matches=pd.read_csv('matches.csv', nrows=48)
completo=pd.read_json("http://vaiteqatar.online:8000/users")
scores.rename(columns={'HomeTeamScore':'HomeTeamResult','AwayTeamScore':'AwayTeamResult'}, inplace=True)
bets['Aposta']=bets['HomeTeamScore'].astype('str')+"x"+bets['AwayTeamScore'].astype('str')
matches['match']=matches['MatchNumber'].astype(str)+"-"+matches['HomeTeam']+ " x "+matches['AwayTeam']
bets=pd.merge(bets, completo, left_on='punter_username',right_on='username', how='left')
bets=bets[['id','game_number', 'HomeTeamScore', 'AwayTeamScore', 'punter_username',
        'name','Aposta' ]]
bets.rename(columns={"name": "Nome"}, inplace=True)
bets=pd.merge(bets,scores, left_on='game_number', right_on='MatchNumber', how='left')
bets.drop('MatchNumber', axis=1, inplace=True)
bets['Resultado']=bets['HomeTeamResult'].astype(int).astype('str')+"x"+bets['AwayTeamResult'].astype(int).astype('str')
bets['Jogo']=bets['HomeTeam']+" x "+bets['AwayTeam']
bets['points']=0
bets=bets[['id','Nome','Jogo', 'game_number', 'HomeTeamScore', 'AwayTeamScore',
       'punter_username',  'Aposta', 'HomeTeamResult', 'AwayTeamResult',
       'HomeTeam', 'AwayTeam', 'Resultado',  'points']]
bets.loc[bets['AwayTeamResult'].isnull(),'points']=np.NaN #
bets.loc[(bets['HomeTeamScore']>bets['AwayTeamScore'])&(bets['HomeTeamResult']>bets['AwayTeamResult']), 'points']=1
bets.loc[(bets['HomeTeamScore']<bets['AwayTeamScore'])&(bets['HomeTeamResult']<bets['AwayTeamResult']), 'points']=1
bets.loc[(bets['HomeTeamScore']==bets['AwayTeamScore'])&(bets['HomeTeamResult']==bets['AwayTeamResult']), 'points']=1
bets.loc[(bets['HomeTeamScore']==bets['HomeTeamResult'])&(bets['AwayTeamScore']==bets['AwayTeamResult']), 'points']=3
bets['Pontuação']=bets['points'].astype(int).astype('str')

###############################################################
def HIGHLIGHT(row):
    red = 'background-color: red;'
    yellow = 'background-color: yellow;'
    green = 'background-color: green;'


    if row['Pontuação'] == "3":
        return [green]
    elif row['Pontuação'] == "1":
        return [yellow]
    elif row['Pontuação'] == "0":
        return [red]

########################################################
st.set_page_config(layout="wide")

st.markdown("## Palpites da galera")   ## Main Title

tab_grafico, tab_individual= st.tabs(["Análise por jogo", "Seus Palpites"])
###############################################################

with tab_grafico:
    
    Jogo = st.selectbox("Selecione a pelada desejada", matches['match'].to_list())
    game_selected=matches[matches['match']==Jogo]['MatchNumber'].tolist()
    bets_selected=bets[bets['game_number']==game_selected[0]]
    #################################################################
    bar_fig=plt.figure(figsize=(8,4))
    ax=sns.countplot(x=bets_selected['Aposta'], color='red',edgecolor='blue', order=bets_selected['Aposta'].value_counts().index)
    ax.bar_label(ax.containers[0])
    plt.xlabel('Aposta')
    plt.ylabel('Número de apostas')
    plt.title (Jogo)
    bar_fig
    #################################################################
    st.markdown("#### Filtre o Aposta pra vem quem tá cravando")
    Aposta_selecionado = st.selectbox("Aposta", ["TODOS"]+bets_selected.sort_values('Aposta')['Aposta'].unique().tolist())
    st.markdown("### Filtre por liga e ligue o secador")
    liga_selecionada = st.selectbox("Liga", list(ligas['name']))
    #################################################################
    bets_selected=bets_selected[bets_selected['id'].isin(leagues[liga_selecionada]['id'])]
    if Aposta_selecionado=="TODOS":
        bets_selected_2=bets_selected
    else:
        bets_selected_2=bets_selected[bets_selected['Aposta']==Aposta_selecionado]
    st.dataframe(data=bets_selected_2[['Nome','Aposta']],use_container_width=True) 
###############################################################
with tab_individual:
    nome_jogador = st.selectbox("Apostador", bets.sort_values('Nome')['Nome'].unique().tolist())
    bets=bets[bets['HomeTeamResult'].notna()]
    bets_name=bets[bets['Nome']==nome_jogador][['Jogo','Aposta','Resultado','Pontuação']]
    bets_name_style=bets_name.style.apply(HIGHLIGHT, subset=[ 'Pontuação'], axis=1).set_properties(**{'text-align': 'center'})
    st.dataframe(data=bets_name_style.hide_index(),use_container_width=True)
