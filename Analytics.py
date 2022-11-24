#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
#import datapane as dp 
#import plotly.express as px
import ipywidgets as widgets
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
#import matplotlib.image as mpimg
from ipywidgets import interact, interactive, fixed, interact_manual
#from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
warnings.filterwarnings('ignore')
#plt.xkcd()


# In[2]:


bets=pd.read_csv('bets.csv', index_col='id')
matches=pd.read_csv('matches.csv', nrows=48)
bets['score']=bets['HomeTeamScore'].astype('str')+"x"+bets['AwayTeamScore'].astype('str')
matches['match']=matches['MatchNumber'].astype(str)+"-"+matches['HomeTeam']+ " x "+matches['AwayTeam']
completo=pd.read_csv('users_completo.csv')
bets=pd.merge(bets, completo, left_on='punter_username',right_on='username', how='left')
bets=bets[['id','game_number', 'HomeTeamScore', 'AwayTeamScore', 'punter_username',
        'name','score' ]]
bets.rename(columns={"name": "Nome", "score": "Placar"}, inplace=True)


# In[9]:


serenini=[22,28,46,47,50,52,53,62,63,64,67,84,87,107,110]


# In[4]:


var = ''
def f(x):
    global var
    var = x
    return x


# In[5]:


# interact(f, x=bets.sort_values('punter_username')['punter_username'].unique()); get user
interact (f, x=matches['match']);


# In[18]:


game_selected=matches[matches['match']==var]['MatchNumber'].tolist()
bets_selected=bets[bets['game_number']==game_selected[0]]
plt.figure(figsize=(10,5))
ax=sns.countplot(bets_selected['Placar'], color='red',edgecolor='blue', order=bets_selected['Placar'].value_counts().index, zorder=2)
ax.bar_label(ax.containers[0])
plt.xlabel('Placar')
plt.ylabel('Número de apostas');
#plt.axhline(1, linestyle='--', color='red', zorder=1)
#plt.yticks(np.append(ax.get_yticks()[1:],1));
#plt.title('França X Austrália');


# In[20]:


#Filtrar ousados
bets_selected[bets_selected['Placar'].map(bets_selected['Placar'].value_counts()) <3]


# In[13]:


#Filtrar placar específico
bets_selected.query("Placar=='4x0'")


# In[21]:


#Filtrar palpites Família Serenini
bets_selected[bets_selected['id'].isin(serenini)]


# In[ ]:


#arr_lena = mpimg.imread('Lenna.jpg')
#imagebox = OffsetImage(arr_lena, zoom=0.31)
#ab = AnnotationBbox(imagebox, (8, 20))
#ax.add_artist(ab)

