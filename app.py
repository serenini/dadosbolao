#!/usr/bin/env python
# coding: utf-8

# In[5]:


#creates a file named app.py 
import streamlit as st
import pandas as pd
import numpy as np

 

 
#function to define the app_layout
def app_layout():
    st.title("Cost and Fuel Saving Calculator")
    distance=st.slider("Weekly Distance",min_value=0,max_value=500)
    price=st.slider("Fuel Price",min_value=10,max_value=120)
    mileage=20
    st.header("Weekly Savings")
    col1,col2,col3=st.beta_columns(3)
    
    with col1:
      st.subheader("Total Cost Saved")
      st.subheader(round((distance/mileage)*price,2))
    with col2:
      st.subheader("Total Fuel Saved")
      st.subheader("{} Litres".format(distance//15))
    with col3:
      st.subheader("CO2 emissions avoided")
      st.subheader("{:.2f} Kilogram".format((distance/15)*0.121))
    st.header("Yearly Savings")
    col1,col2,col3=st.beta_columns(3)
    
    with col1:
      st.subheader("Total Cost Saved")
      st.subheader(round((distance/mileage)*price*53,2))
    with col2:
      st.subheader("Total Fuel Saved")
      st.subheader("{:.2f} Litres".format((distance//15)*53))
    with col3:
      st.subheader("CO2 emissions avoided")
      st.subheader("{:.2f} Kilogram".format((distance/15)*0.121*53))
 
 
if __name__=='__main__':
  app_layout()


# In[ ]:




