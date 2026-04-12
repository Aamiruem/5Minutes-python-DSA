import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt

st.title('IoT Smart Home Wiring Planner — Kruskal MST')
uploaded = st.file_uploader('CSV: id,x,y,wall_penalty', type=['csv'])

def dist(a,b):
    return math.hypot(a['x']-b['x'], a['y']-b['y'])

def find(x):
    while parent[x]!=x:
        parent[x]=parent[parent[x]]
        x=parent[x]
    return x

def union(a,b):
    ra,rb=find(a),find(b)
    if ra==rb: return False
    if rank[ra]<rank[rb]:
        parent[ra]=rb
    else:
        parent[rb]=ra
        if rank[ra]==rank[rb]:
            rank[ra]+=1
    return True
    
if uploaded:
    df = pd.read_csv(uploaded)

    wall_factor = st.slider('Wall penalty multiplier', 0.0, 5.0, 1.0)
    wireless_mult = st.slider('Wireless distance multiplier', 0.5, 3.0, 1.5)

    nodes = df[['id','x','y']].to_dict('records')
    pen = df.get('wall_penalty', pd.Series([0]*len(df))).tolist()
    n = len(nodes)

    edges = []
    for i in range(n):
        for j in range(i+1,n):
            d = dist(nodes[i], nodes[j])
            wired = d + wall_factor*(pen[i]+pen[j])/2
            cost = wired
            edges.append((cost,i,j,d))

    edges.sort(key=lambda x:x[0])
    parent=list(range(n))
    rank=[0]*n


    mst=[]
    total=0.0
    for w,i,j,d in edges:
        if union(i,j):
            mst.append((i,j,w,d))
            total+=w
        if len(mst)==n-1: break

    st.metric('Estimated total cable cost', round(total,3))
    fig,ax=plt.subplots()
    for e in mst:
        i,j,_,_ = e
        x=[nodes[i]['x'], nodes[j]['x']]
        y=[nodes[i]['y'], nodes[j]['y']]
        ax.plot(x,y,'-k',linewidth=1)
    xs=[nd['x'] for nd in nodes]
    ys=[nd['y'] for nd in nodes]
    ax.scatter(xs,ys,s=50)
    for idx,nd in enumerate(nodes):
        ax.text(nd['x'], nd['y'], nd['id'], fontsize=9, ha='right')
    ax.set_title('Proposed wiring (MST)')
    st.pyplot(fig)

    st.write('Selected edges:')
    out = [{'from':nodes[i]['id'],'to':nodes[j]['id'],'cost':round(w,3),'raw_dist':round(d,3)} for i,j,w,d in mst]
    st.table(pd.DataFrame(out))
    st.write('All devices:')
    st.table(df)
