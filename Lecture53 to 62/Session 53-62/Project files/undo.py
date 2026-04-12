
import streamlit as st

def init_state():
    if "current_text" not in st.session_state:
        st.session_state.current_text = ""
    if "undo_stack" not in st.session_state:
        st.session_state.undo_stack = [] 
    if "redo_stack" not in st.session_state:
        st.session_state.redo_stack = []  
    if "editor_input" not in st.session_state:
        st.session_state.editor_input = st.session_state.current_text

    if "pending_sync" not in st.session_state:
        st.session_state.pending_sync = None

def push_undo(state):
    st.session_state.undo_stack.append(state)

def push_redo(state):
    st.session_state.redo_stack.append(state)

def request_sync_editor(value: str):
    st.session_state.pending_sync = value
    st.rerun()

def apply_change(new_text):
    push_undo(st.session_state.current_text)
    st.session_state.current_text = new_text
    st.session_state.redo_stack.clear()
    request_sync_editor(new_text)

def do_undo():
    if st.session_state.undo_stack:
        prev = st.session_state.undo_stack.pop()
        push_redo(st.session_state.current_text)
        st.session_state.current_text = prev
        request_sync_editor(prev)

def do_redo():
    if st.session_state.redo_stack:
        nxt = st.session_state.redo_stack.pop()
        push_undo(st.session_state.current_text)
        st.session_state.current_text = nxt
        request_sync_editor(nxt)

def do_clear():
    push_undo(st.session_state.current_text)
    st.session_state.current_text = ""
    st.session_state.redo_stack.clear()
    request_sync_editor("")

st.set_page_config(page_title="Undo-Redo Text Editor (Stacks)")
st.title("Undo-Redo Text Editor (Stack Based)")

init_state()


if st.session_state.pending_sync is not None:
    st.session_state.editor_input = st.session_state.pending_sync
    st.session_state.pending_sync = None



st.subheader("Editor")
edited = st.text_area("Type text here", key="editor_input", height=300)

c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("Apply Change"):
        if edited != st.session_state.current_text:
            apply_change(edited)
        else:
            st.info("No change detected.")
with c2:
    if st.button("Undo ⬅️", disabled=(len(st.session_state.undo_stack) == 0)):
        do_undo()
with c3:
    if st.button("Redo ➡️", disabled=(len(st.session_state.redo_stack) == 0)):
        do_redo()
with c4:
    if st.button("Clear ✨"):
        do_clear()

st.markdown("#### Current Document")
st.code(st.session_state.current_text or "⟨empty⟩")