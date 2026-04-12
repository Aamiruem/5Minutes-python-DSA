
import streamlit as st
import pandas as pd

def init_state():
    if "playlist" not in st.session_state:
        st.session_state.playlist = [] 

def to_df(playlist):
    if not playlist:
        return pd.DataFrame(columns=["#","Title","Artist","Duration (mm:ss)"])
    rows = []
    for i, s in enumerate(playlist, start=1):
        mm = int(s.get("duration", 0)) // 60
        ss = int(s.get("duration", 0)) % 60
        rows.append({"#": i, "Title": s.get("title",""), "Artist": s.get("artist",""), "Duration (mm:ss)": f"{mm:02d}:{ss:02d}"})
    return pd.DataFrame(rows)

def parse_duration(text):
    text = (text or "").strip()
    if not text:
        return 0

    if ":" in text:
        try:
            mm, ss = text.split(":")
            return int(mm)*60 + int(ss)
        except:
            return 0
    try:
        return int(text)
    except:
        return 0


def linear_search(playlist, query):
    q = query.lower()
    hits = []
    for idx, s in enumerate(playlist):
        if q in s["title"].lower() or q in s["artist"].lower():
            hits.append(idx)
    return hits

def binary_search_titles(playlist, title):
    lo, hi = 0, len(playlist)-1
    target = title.lower()
    while lo <= hi:
        mid = (lo + hi) // 2
        mid_title = playlist[mid]["title"].lower()
        if mid_title == target:
            return mid
        if mid_title < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

st.set_page_config(page_title="Dynamic Playlist Manager")
st.title("Dynamic Playlist Manager")

init_state()

with st.sidebar:
    st.header("Utilities")
    st.write("Import/export playlist as CSV. Columns: title,artist,duration (seconds or mm:ss).")
    uploaded = st.file_uploader("Import CSV", type=["csv"])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        new_list = []
        for _, r in df.iterrows():
            d = r.get("duration", r.get("Duration", ""))
            new_list.append({
                "title": str(r.get("title", r.get("Title",""))),
                "artist": str(r.get("artist", r.get("Artist",""))),
                "duration": parse_duration(str(d))
            })
        st.session_state.playlist = new_list
        st.success(f"Imported {len(new_list)} songs.")
    if st.session_state.playlist:
        df = pd.DataFrame([
            {"title": s["title"], "artist": s["artist"], "duration": s["duration"]}
            for s in st.session_state.playlist
        ])
        st.download_button("⬇️ Export CSV", data=df.to_csv(index=False), file_name="playlist.csv", mime="text/csv")


colA, colB = st.columns([2,1], gap="large")
with colA:
    st.subheader("➕ Add / Insert")
    with st.form("add_form", clear_on_submit=True):
        t = st.text_input("Title", placeholder="Song title")
        a = st.text_input("Artist", placeholder="Artist name")
        d = st.text_input("Duration (mm:ss or seconds)", placeholder="3:45")
        submitted = st.form_submit_button("Add to playlist")
        if submitted:
            if not t:
                st.error("Title is required.")
            else:
                song = {"title": t, "artist": a, "duration": parse_duration(d)}
                st.session_state.playlist.append(song)
                st.success(f"Added: {t}")

with colB:
    st.subheader("🗑️ Remove")
    if st.session_state.playlist:
            title_q = st.text_input("Exact title to remove")
            if st.button("Remove by title"):
                idxs = [i for i,s in enumerate(st.session_state.playlist) if s["title"].strip().lower() == title_q.strip().lower()]
                if idxs:
                    st.session_state.playlist.pop(idxs[0])
                    st.success(f"Removed: {title_q}")
                else:
                    st.warning("Title not found.")
    else:
        st.info("Playlist is empty.")

st.divider()

st.subheader("Reversing & Sorting")
c1, c2 = st.columns(2)
with c1:
    if st.button("Reverse playlist"):
        st.session_state.playlist.reverse()
with c2:
    if st.session_state.playlist:
        how = st.selectbox("Sort by", ["Title (A→Z)", "Artist (A→Z)", "Duration (short→long)"])
        if st.button("Sort"):
            if how.startswith("Title"):
                st.session_state.playlist.sort(key=lambda s: s["title"].lower())
            elif how.startswith("Artist"):
                st.session_state.playlist.sort(key=lambda s: s["artist"].lower())
            else:
                st.session_state.playlist.sort(key=lambda s: s["duration"])

st.subheader("🔎 Search")
if st.session_state.playlist:
    query = st.text_input("Search by title or artist (linear search)")
    if st.button("Linear search"):
        hits = linear_search(st.session_state.playlist, query)
        if hits:
            st.success(f"Found {len(hits)} match(es) at positions: " + ", ".join(str(i+1) for i in hits))
        else:
            st.warning("No matches.")
    st.caption("Binary search requires the list to be sorted by Title (A→Z).")
    title_exact = st.text_input("Binary search by exact title")
    if st.button("Binary search"):
        idx = binary_search_titles(st.session_state.playlist, title_exact)
        if idx != -1:
            st.success(f"Found at position {idx+1}")
        else:
            st.warning("Not found or playlist not sorted by title.")
else:
    st.info("Add songs to enable search operations.")

st.divider()

st.subheader("📃 Current Playlist")
st.dataframe(to_df(st.session_state.playlist), hide_index=True, use_container_width=True)