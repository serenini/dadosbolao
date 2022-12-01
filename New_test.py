#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
warnings.filterwarnings('ignore')
#########FUNCTION TO GET DATA FROM GOOGLE SHEETS API################
def get_game_scores_df():
    scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("GoogleSheetsAPIKey.json", scopes)
    file = gspread.authorize(credentials)
    sheet = file.open("GameScores")
    sheet = sheet.worksheet("game_scores")
    return pd.DataFrame(sheet.get_all_records())

##################### Load Dataset #####################
bets=pd.read_csv('https://raw.githubusercontent.com/serenini/dadosbolao/main/bets.csv', index_col='id')
matches=pd.read_csv('matches.csv', nrows=48)
completo=pd.read_json("http://vaiteqatar.online:8000/users")
scores=get_game_scores_df()
ligas=pd.read_json("http://vaiteqatar.online:8000/bet_groups")
leagues={}
for i in range(len(ligas)):
    leagues[ligas['name'][i]]=pd.json_normalize(ligas['players'][i])

################## Manipulate datasets######################

completo["name"] = completo["name"].str.title()
scores.rename(columns={'HomeTeamScore':'HomeTeamResult','AwayTeamScore':'AwayTeamResult'}, inplace=True)
bets['Aposta']=bets['HomeTeamScore'].astype('str')+"x"+bets['AwayTeamScore'].astype('str')
matches['match']=matches['MatchNumber'].astype(str)+"-"+matches['HomeTeam']+ " x "+matches['AwayTeam']
bets=pd.merge(bets, completo, left_on='punter_username',right_on='username', how='left')
bets=bets[['id','game_number', 'HomeTeamScore', 'AwayTeamScore', 'punter_username',
        'name','Aposta' ]]
bets.rename(columns={"name": "Nome"}, inplace=True)
bets=pd.merge(bets,scores, left_on='game_number', right_on='MatchNumber', how='left')
bets.drop('MatchNumber', axis=1, inplace=True)
bets.replace('', np.nan, inplace=True)
bets2=bets[bets['HomeTeamResult'].notna()]
bets2['Resultado']=bets2['HomeTeamResult'].astype(int).astype('str')+"x"+bets2['AwayTeamResult'].astype(int).astype('str')
bets2['Jogo']=bets2['HomeTeam']+" x "+bets2['AwayTeam']
bets2['points']=0
bets2=bets2[['id','Nome','Jogo', 'game_number', 'HomeTeamScore', 'AwayTeamScore',
       'punter_username',  'Aposta', 'HomeTeamResult', 'AwayTeamResult',
       'HomeTeam', 'AwayTeam', 'Resultado',  'points']]
bets2.loc[bets2['AwayTeamResult'].isnull(),'points']=np.NaN #
bets2.loc[(bets2['HomeTeamScore']>bets2['AwayTeamScore'])&(bets2['HomeTeamResult']>bets2['AwayTeamResult']), 'points']=1
bets2.loc[(bets2['HomeTeamScore']<bets2['AwayTeamScore'])&(bets2['HomeTeamResult']<bets2['AwayTeamResult']), 'points']=1
bets2.loc[(bets2['HomeTeamScore']==bets2['AwayTeamScore'])&(bets2['HomeTeamResult']==bets2['AwayTeamResult']), 'points']=1
bets2.loc[(bets2['HomeTeamScore']==bets2['HomeTeamResult'])&(bets2['AwayTeamScore']==bets2['AwayTeamResult']), 'points']=3
bets2['Pontuação']=bets2['points'].astype(int).astype('str')

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

tab_grafico, tab_individual, tab_evolucao, tab_sim= st.tabs(["Palpites Galera", "Seus Palpites", "Gráficos", "Simulador"])
###############################################################

with tab_grafico:
    
    Jogo = st.selectbox("Selecione a pelada desejada", ["0"]+matches['match'].to_list())
    if Jogo=="0":
        game_selected=matches[matches['match']=="1-Qatar x Ecuador"]['MatchNumber'].tolist()
    else:
        game_selected=matches[matches['match']==Jogo]['MatchNumber'].tolist()    
    bets_selected=bets[bets['game_number']==game_selected[0]]
    #################################################################
    if Jogo=="0":
        st.markdown("")
    else:
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
    nome_jogador = st.selectbox("Apostador", bets2.sort_values('Nome')['Nome'].unique().tolist())
    bets_name=bets2[bets2['Nome']==nome_jogador][['Jogo','Aposta','Resultado','Pontuação']]
    bets_name_style=bets_name.style.apply(HIGHLIGHT, subset=[ 'Pontuação'], axis=1).set_properties(**{'text-align': 'center'})
    st.dataframe(data=bets_name_style.hide_index(),use_container_width=True)
#################################################################
whttps://stats.stackexchange.com/questions/540252/how-to-calculate-marginal-effects-with-multinomial-regression-for-survey-data-in
###############################################################
with tab_sim:
    col1, col2 = st.columns(2)
    with col1:
        scores.rename(columns={'MatchNumber':'Jogo', 'HomeTeamResult':'GolsA', 'AwayTeamResult':'GolsB'}, inplace=True)
        grid_table=AgGrid(scores[['Jogo','HomeTeam', 'GolsA', 'GolsB', 'AwayTeam']],fit_columns_on_grid_load = True,editable=True)
        df=grid_table['data']
        
    with col2:
        df=df.astype(str)
        df.replace("","10", inplace=True)
        df.replace(" ","10", inplace=True)
        df['Jogo']=df['Jogo'].astype(int)
        df['GolsB']=df['GolsB'].astype(int)
        df['GolsA']=df['GolsA'].astype(int)
        bets.drop('AwayTeamResult', axis=1,inplace=True)
        bets.drop('HomeTeamResult', axis=1,inplace=True)
        bets=pd.merge(bets,df, left_on='game_number', right_on='Jogo', how='left')
        bets['points']=0
        bets.loc[bets['GolsB'].isnull(),'points']=0 #
        bets.loc[(bets['HomeTeamScore']>bets['AwayTeamScore'])&(bets['GolsA']>bets['GolsB']), 'points']=1
        bets.loc[(bets['HomeTeamScore']<bets['AwayTeamScore'])&(bets['GolsA']<bets['GolsB']), 'points']=1
        bets.loc[(bets['HomeTeamScore']==bets['AwayTeamScore'])&(bets['GolsA']==bets['GolsB']), 'points']=1
        bets.loc[(bets['HomeTeamScore']==bets['GolsA'])&(bets['AwayTeamScore']==bets['GolsB']), 'points']=3
        bets.loc[bets['GolsB']==10, 'points']=0
        #st.dataframe(bets)
        #st.write(bets.dtypes)
        ranking=bets.groupby('Nome').sum().sort_values('points', ascending=False).reset_index()[['Nome','points']]
        ranking['Posição']=np.arange(112)[1:]
        ranking.rename(columns={"points": "Pontos"}, inplace=True)
        st.dataframe(ranking[['Posição', 'Nome', 'Pontos']], height=1500)
