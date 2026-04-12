import streamlit as st
import pandas as pd

def load_sample():
    return [
        {"id":101,"title":"The Silent Patient","author":"Alex Michaelides"},
        {"id":58,"title":"Atomic Habits","author":"James Clear"},
        {"id":302,"title":"Clean Code","author":"Robert C. Martin"},
        {"id":215,"title":"Deep Work","author":"Cal Newport"},
        {"id":77,"title":"The Alchemist","author":"Paulo Coelho"},
        {"id":199,"title":"Sapiens","author":"Yuval Noah Harari"},
        {"id":410,"title":"1984","author":"George Orwell"},
        {"id":123,"title":"The Pragmatic Programmer","author":"Andrew Hunt"},
        {"id":7,"title":"To Kill a Mockingbird","author":"Harper Lee"},
        {"id":88,"title":"The Power of Habit","author":"Charles Duhigg"}
    ]

def bubble_sort(arr, key):
    a = arr[:]
    n = len(a)
    comps = 0
    for i in range(n):
        for j in range(0, n-i-1):
            comps += 1
            if key(a[j]) > key(a[j+1]):
                a[j], a[j+1] = a[j+1], a[j]
    return a, comps

def selection_sort(arr, key):
    a = arr[:]
    n = len(a)
    comps = 0
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            comps += 1
            if key(a[j]) < key(a[min_idx]):
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a, comps

def merge_sort(arr, key):
    comps = [0]
    def merge(left, right):
        i=j=0
        out=[]
        while i<len(left) and j<len(right):
            comps[0]+=1
            if key(left[i])<=key(right[j]):
                out.append(left[i]); i+=1
            else:
                out.append(right[j]); j+=1
        out.extend(left[i:]); out.extend(right[j:])
        return out
    def ms(a):
        if len(a)<=1: return a
        m=len(a)//2
        return merge(ms(a[:m]), ms(a[m:]))
    return ms(arr[:]), comps[0]

def linear_search_by_title(books, query):
    q=(query or "").strip().lower()
    hits=[]; comps=0
    for b in books:
        comps+=1
        if q and q in b["title"].lower():
            hits.append(b)
    return hits, comps

def binary_search_by_id(sorted_books, target_id):
    lo=0; hi=len(sorted_books)-1; comps=0
    while lo<=hi:
        mid=(lo+hi)//2
        comps+=1
        mid_id=sorted_books[mid]["id"]
        if mid_id==target_id:
            return sorted_books[mid], comps
        if mid_id<target_id:
            lo=mid+1
        else:
            hi=mid-1
    return None, comps

st.set_page_config(page_title="Library Catalog (Core Sorts)")
st.title("Library Catalog")

if "books" not in st.session_state:
    st.session_state.books = load_sample()

st.subheader("Sort books")
alg = st.selectbox("Algorithm", ["bubble","selection","merge"], index=2)
field = st.selectbox("Field", ["id","title","author"], index=1)
asc = st.checkbox("Ascending", value=True)
books = list(st.session_state.books)

key = (lambda x: x[field]) if field!="title" and field!="author" else (lambda x: x[field].lower())
if alg=="bubble":
    sorted_books, comps = bubble_sort(books, key)
elif alg=="selection":
    sorted_books, comps = selection_sort(books, key)
else:
    sorted_books, comps = merge_sort(books, key)
if not asc:
    sorted_books = list(reversed(sorted_books))
st.write(f"comparisons: {comps}")
st.dataframe(pd.DataFrame(sorted_books), use_container_width=True)

st.subheader("Search")
col1,col2 = st.columns(2)
with col1:
    title_q = st.text_input("Search title (linear)")
    if st.button("Search title"):
        hits, comps = linear_search_by_title(sorted_books, title_q)
        if hits:
            st.success(f"found {len(hits)} comps:{comps}")
            st.table(pd.DataFrame(hits))
        else:
            st.info(f"no matches comps:{comps}")
with col2:
    id_q = st.number_input("Search id (binary)", min_value=0, step=1, key="bid")
    if st.button("Search id"):
        sb = sorted(books, key=lambda x: x["id"])
        result, comps = binary_search_by_id(sb, int(id_q))
        if result:
            st.success(f"found comps:{comps}"); st.json(result)
        else:
            st.info(f"not found comps:{comps}")

st.subheader("Add / Remove")
with st.form("crud", clear_on_submit=True):
    nid = st.number_input("id", min_value=0, step=1, value=0)
    nt = st.text_input("title")
    na = st.text_input("author")
    act = st.selectbox("action", ["add","remove"])
    sub = st.form_submit_button("go")
    if sub:
        if act=="add":
            st.session_state.books.append({"id":int(nid), "title":nt, "author":na})
            st.success("added")
        else:
            st.session_state.books = [b for b in st.session_state.books if b["id"]!=int(nid)]
            st.success("removed")