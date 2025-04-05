import streamlit as st
st.set_page_config(page_title="Digital 101 - Revision",page_icon=":material/home:")
pg = st.navigation([st.Page("./pages/1_home.py",icon="👋"),st.Page("./pages/2_learn.py",icon=":material/menu_book:")])
pg.run()