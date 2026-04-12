import streamlit as st
import random

def alloc_matrix(r, c, fill=0):
    return [[fill for _ in range(c)] for _ in range(r)]

def random_matrix(r, c, low=0, high=9):
    m = alloc_matrix(r, c)
    for i, row in enumerate(m):
        for j in range(len(row)):
            row[j] = random.randint(low, high)
    return m

def transpose(mat):
    r, c = len(mat), len(mat[0]) 
    t = alloc_matrix(c, r)
    for i in range(r):
        row = mat[i]
        for j in range(c):
            t[j][i] = row[j]
    return t

def add(a, b):
    r, c = len(a), len(a[0])
    res = alloc_matrix(r, c)
    for i in range(r):
        ra, rb = a[i], b[i]
        for j in range(c):
            res[i][j] = ra[j] + rb[j]
    return res

def multiply(a, b):
    ra, ca = len(a), len(a[0])
    rb, cb = len(b), len(b[0])
    if ca != rb:
        raise ValueError("Incompatible dims for multiply")
    res = alloc_matrix(ra, cb)
    for i in range(ra):
        for j in range(cb):
            s = 0
            for k in range(ca):
                s += a[i][k] * b[k][j]
            res[i][j] = s
    return res

st.title("Pointer-style Matrix")

op = st.selectbox("Operation", ["Add", "Multiply", "Transpose"])
if op == "Transpose":
    r = st.number_input("Rows", min_value=1, value=3)
    c = st.number_input("Cols", min_value=1, value=3)
    m = st.button("Use Random Matrix")
    if m:
        A = random_matrix(r, c)
        st.write("Matrix A:", A)
        st.write("Transpose:", transpose(A))
else:
    r1 = st.number_input("A rows", min_value=1, value=2, key="r1")
    c1 = st.number_input("A cols", min_value=1, value=2, key="c1")
    if op == "Add":
        r2, c2 = r1, c1
    else:
        r2 = st.number_input("B rows", min_value=1, value=2, key="r2")
        c2 = st.number_input("B cols", min_value=1, value=2, key="c2")
    if st.button("Generate Random Matrices"):
        A = random_matrix(r1, c1)
        B = random_matrix(r2, c2)
        st.write("A:", A)
        st.write("B:", B)
        try:
            if op == "Add":
                st.write("A + B:", add(A, B))
            else:
                st.write("A × B:", multiply(A, B))
        except Exception as e:
            st.error(e)
