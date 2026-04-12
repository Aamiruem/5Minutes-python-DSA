
import streamlit as st

class Node:
    def __init__(self, id, title):
        self.id = id
        self.title = title
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.n = 0
    def prepend(self, node):
        node.next = self.head
        self.head = node
        self.n += 1
    def append(self, node):
        if not self.head:
            self.head = node
            self.n = 1
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node
        self.n += 1
    def insert_at(self, node, pos):
        if pos <= 1:
            self.prepend(node)
            return True
        if pos > self.n:
            self.append(node)
            return True
        i = 1
        cur = self.head
        while i < pos - 1 and cur.next:
            cur = cur.next
            i += 1
        node.next = cur.next
        cur.next = node
        self.n += 1
        return True
    def delete_start(self):
        if not self.head:
            return False
        self.head = self.head.next
        self.n -= 1
        return True
    def delete_end(self):
        if not self.head:
            return False
        if not self.head.next:
            self.head = None
            self.n = 0
            return True
        prev = None
        cur = self.head
        while cur.next:
            prev, cur = cur, cur.next
        prev.next = None
        self.n -= 1
        return True
    def delete_at(self, pos):
        if pos <= 1:
            return self.delete_start()
        if pos > self.n:
            return False
        i = 1
        prev = self.head
        cur = self.head.next
        while i < pos - 1 and cur:
            prev, cur = cur, cur.next
            i += 1
        if cur is None:
            return False
        prev.next = cur.next
        self.n -= 1
        return True
    def search(self, text):
        text = text.strip().lower()
        hits = []
        i = 1
        cur = self.head
        while cur:
            if text and text in cur.title.lower():
                hits.append((i, cur.id, cur.title))
            cur = cur.next
            i += 1
        return hits
    def to_rows(self):
        rows = []
        i = 1
        cur = self.head
        while cur:
            rows.append({"#": i, "ID": cur.id, "Title": cur.title})
            cur = cur.next
            i += 1
        return rows

def init_state():
    if "ll" not in st.session_state:
        st.session_state.ll = LinkedList()
    if "next_id" not in st.session_state:
        st.session_state.next_id = 1

st.set_page_config(page_title="To-Do Task Manager")
st.title("To-Do Task Manager")

init_state()

st.subheader("Add Task")
t = st.text_input("Task title")
col1, col2 = st.columns(2)
with col1:
    where = st.radio("Insert where", ["Start","End","Position"], horizontal=True, key="add_where")
with col2:
    pos = st.number_input("Position (1-based)", min_value=1, step=1, value=1, disabled=(st.session_state.get("add_where")!="Position"), key="add_pos")
if st.button("Add"):
    if not t.strip():
        st.warning("Enter a task")
    else:
        node = Node(st.session_state.next_id, t.strip())
        if where == "Start":
            st.session_state.ll.prepend(node)
        elif where == "End":
            st.session_state.ll.append(node)
        else:
            st.session_state.ll.insert_at(node, int(pos))
        st.session_state.next_id += 1
        st.success("Added")

st.divider()
st.subheader("Delete Task")
colA, colB = st.columns(2)
with colA:
    dwhere = st.radio("Delete from", ["Start","End","Position"], horizontal=True, key="del_where")
with colB:
    dpos = st.number_input("Position (1-based)", min_value=1, step=1, value=1, disabled=(st.session_state.get("del_where")!="Position"), key="del_pos")
if st.button("Delete"):
    ok = False
    if dwhere == "Start":
        ok = st.session_state.ll.delete_start()
    elif dwhere == "End":
        ok = st.session_state.ll.delete_end()
    else:
        ok = st.session_state.ll.delete_at(int(dpos))
    st.success("Deleted") if ok else st.warning("Nothing to delete")

st.divider()
st.subheader("Search")
q = st.text_input("Find tasks containing")
if st.button("Search"):
    hits = st.session_state.ll.search(q)
    if hits:
        st.write("\n".join([f"pos {p}: #{i} — {title}" for p, i, title in hits]))
    else:
        st.info("No matches")

st.divider()
st.subheader("Tasks")
rows = st.session_state.ll.to_rows()
if rows:
    st.table(rows)
else:
    st.caption("No tasks")
st.metric("Total", st.session_state.ll.n)