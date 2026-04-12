import streamlit as st
import pandas as pd

st.title('Startup Budget Allocator — 0/1 Knapsack DP')
st.markdown('Upload CSV with columns: name,cost,profit')

uploaded = st.file_uploader('CSV: name,cost,profit', type=['csv'])
if uploaded:
    df = pd.read_csv(uploaded)

    budget = st.number_input('Budget', min_value=1, value=10)
    names = df['name'].tolist()
    costs = list(map(int,df['cost'].tolist()))
    profits = list(map(int,df['profit'].tolist()))
    n = len(costs)
    dp = [[0]*(budget+1) for _ in range(n+1)]
    for i in range(1,n+1):
        for b in range(budget+1):
            dp[i][b] = dp[i-1][b]
            if costs[i-1] <= b:
                v = profits[i-1] + dp[i-1][b-costs[i-1]]
                if v > dp[i][b]:
                    dp[i][b] = v

    res=[]
    b=budget
    for i in range(n,0,-1):
        if dp[i][b] != dp[i-1][b]:
            res.append(i-1)
            b -= costs[i-1]
    res = list(reversed(res))
    st.metric('Max Profit', int(dp[n][budget]))
    st.write('Selected ideas:')
    st.table(pd.DataFrame([{'name':names[i],'cost':costs[i],'profit':profits[i]} for i in res]))
    st.write('All ideas:')
    st.table(df)
