import streamlit as st
import pandas as pd 
from mypulp import Model,quicksum,GRB
#from importlib.resources import *

st.set_page_config(
    page_title="SaizeApp ",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title('SaizeriyaOptimization')

money = st.sidebar.slider("予算", 300, 5000, 1000, 100)
calorie_limit = st.sidebar.slider("摂取限界カロリー", 300, 3000, 1000, 100)

df = pd.read_csv("saize.csv", index_col=0)

menu_index = [i for i in range(1,len(df)+1)]
menu, P, C, S = {},{},{},{}

for i in menu_index:
    menu[i] = df["name"][i]
    P[i] = df["price"][i]
    C[i] = df["calorie"][i]
    S[i] = df["salt"][i]

model = Model()
x = {}
for i in menu_index:
    x[i] = model.addVar(vtype='B', name=str(i))
model.update()

for i in menu_index:
    model.addConstr(quicksum(P[i]*x[i] for i in menu_index) <= money)
    model.addConstr(quicksum(C[i]*x[i] for i in menu_index) <= calorie_limit)

model.setObjective(quicksum(C[i]*x[i] for i in menu_index), GRB.MAXIMIZE)

if st.checkbox("計算"):
    model.optimize()

    print('Optimal solution:', model.ObjVal)
    print("======================================")
    sum_calorie,sum_price=0,0
    for v in model.getVars():
        if v.X > 0.001:
            st.write(menu[int(v.VarName)],P[int(v.VarName)],"円") 
            sum_calorie+=int(C[int(v.VarName)])
            sum_price+=int(P[int(v.VarName)])
    st.write("=======================================")
    st.write("計",sum_calorie,"キロカロリー")
    st.write("合計金額",sum_price, "円")
