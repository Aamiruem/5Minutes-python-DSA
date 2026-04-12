import streamlit as st
from collections import defaultdict

st.title("Social Connection Tracer")
st.write("Enter connections (edges) and find if two people are connected using DFS")

def build_graph(edge_list):
    g = defaultdict(list)
    for a,b in edge_list:
        g[a].append(b)
        g[b].append(a)
    return g

def dfs_path(graph, start, goal):
    visited = set()
    path = []
    def dfs(u):
        visited.add(u)
        path.append(u)
        if u == goal:
            return True
        for v in graph.get(u, []):
            if v not in visited:
                if dfs(v):
                    return True
        path.pop()
        return False
    found = dfs(start)
    return path if found else None

st.subheader("Input Edges")
text_edges = st.text_area("Enter edges (one per line, format: A,B)", "A,B\nA,C\nB,D\nC,E")
edges = []
for ln in text_edges.splitlines():
    ln = ln.strip()
    if not ln or "," not in ln:
        continue
    a,b = [x.strip() for x in ln.split(",",1)]
    edges.append((a,b))

if edges:
    g = build_graph(edges)
    nodes = sorted(g.keys())
    start = st.text_input("Source node", value=nodes[0] if nodes else "")
    goal = st.text_input("Target node", value=nodes[1] if len(nodes)>1 else "")
    if st.button("Find Connection Path"):
        if start not in g or goal not in g:
            st.error("Source or target not found in graph.")
        else:
            path = dfs_path(g, start, goal)
            if path:
                st.success(f"Path found: {' → '.join(path)}")
                st.info(f"Length (edges): {len(path)-1}")
            else:
                st.warning(f"No path found between {start} and {goal}.")
