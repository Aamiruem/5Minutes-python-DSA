
import streamlit as st
from collections import deque
from datetime import datetime

def init_state():
    if "queue" not in st.session_state:
        st.session_state.queue = deque()  
    if "next_id" not in st.session_state:
        st.session_state.next_id = 1
    if "last_processed" not in st.session_state:
        st.session_state.last_processed = None

def enqueue(name: str):
    ticket = {
        "id": st.session_state.next_id,
        "name": name.strip() or f"Guest-{st.session_state.next_id}",
        "time": datetime.now().strftime("%H:%M:%S"),
    }
    st.session_state.queue.append(ticket)
    st.session_state.next_id += 1

def dequeue():
    if st.session_state.queue:
        st.session_state.last_processed = st.session_state.queue.popleft()

def peek():
    if st.session_state.queue:
        return st.session_state.queue[0]
    return None

def clear_queue():
    st.session_state.queue.clear()
    st.session_state.last_processed = None


st.set_page_config(page_title="Ticket Counter (Queue Based)")
st.title("🎟️ Ticket Counter — Queue (FIFO)")

init_state()

left, right = st.columns([2,1], gap="large")

with left:
    st.subheader("Enqueue")
    name = st.text_input("Customer name (optional)", placeholder="e.g., name")
    if st.button("Add to Queue ➕"):
        enqueue(name)
        st.success("Added to queue.")
    st.divider()

    st.subheader("Process Queue")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Dequeue (Process Next)", disabled=(len(st.session_state.queue) == 0)):
            dequeue()
    with c2:
        nxt = peek()
        if st.button("Peek Next", disabled=(len(st.session_state.queue) == 0)):
            nxt = peek()
            if nxt:
                st.info(f"Next: #{nxt['id']} — {nxt['name']} (at {nxt['time']})")
    with c3:
        if st.button("Clear Queue", type="secondary", disabled=(len(st.session_state.queue) == 0 and st.session_state.last_processed is None)):
            clear_queue()
            st.warning("Queue cleared.")

    st.divider()
    st.subheader("Queue View (Front → Back)")
    if st.session_state.queue:
        header = f"{'Pos':<4} {'Ticket':<8} {'Name':<18} {'Arrived':<10}"
        st.code(header + "\n" + "-"*45 + "\n" + "\n".join(
            f"{i+1:<4} #{t['id']:<8} {t['name']:<18} {t['time']:<10}"
            for i, t in enumerate(list(st.session_state.queue))
        ))
    else:
        st.caption("Queue is empty.")

with right:
    st.subheader("Now Serving")
    if st.session_state.last_processed:
        t = st.session_state.last_processed
        st.success(f"Processed: #{t['id']} — {t['name']} (arrived {t['time']})")
    else:
        st.info("No ticket processed yet.")