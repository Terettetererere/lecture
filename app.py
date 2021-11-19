import streamlit as st
import pandas as pd 
import plotly.express as px
from importlib.resources import *

st.title("Streamlit Demo")
st.subheader("by S.T.")

df = px.data.iris()

st.write(df)

st.write(px.scatter(df,x="sepal_length",y="sepal_width",color="species"))
