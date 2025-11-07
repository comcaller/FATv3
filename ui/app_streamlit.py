import os, glob
import streamlit as st

LOG_DIR = "/home/roa/FAT/logs"
st.set_page_config(page_title="FATv3 Monitor", layout="wide")
st.title("FATv3 — Agents")

logs = sorted(glob.glob(os.path.join(LOG_DIR, "*.log")))
cols = st.columns(3)
for i, log in enumerate(logs):
    with cols[i % 3]:
        st.subheader(os.path.basename(log).replace(".log",""))
        st.code(open(log).read()[-2000:], language="log")
