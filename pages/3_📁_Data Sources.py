import streamlit as st

st.set_page_config(
    page_title="Data Sources",
    page_icon="📁", 
    layout="wide"
)

col1, col2 = st.columns(2)
st.markdown("<div style='height: 20px'/>", unsafe_allow_html=True)
with col1:
    st.write("## **Lionel Messi vs Cristiano Ronaldo Club Goals**")
with col2:
    st.markdown("<div style='height: 20px'/>", unsafe_allow_html=True)
    st.write("https://www.kaggle.com/datasets/azminetoushikwasi/lionel-messi-vs-cristiano-ronaldo-club-goals")

col1, col2 = st.columns(2)
st.markdown("<div style='height: 20px'/>", unsafe_allow_html=True)
with col1:
    st.write("## **Messi vs Ronaldo Dataset**")
with col2:
    st.markdown("<div style='height: 20px'/>", unsafe_allow_html=True)
    st.write("https://www.kaggle.com/datasets/ogbuzurukelechi/messi-vs-ronaldo-dataset")

col1, col2 = st.columns(2)
st.markdown("<div style='height: 20px'/>", unsafe_allow_html=True)
with col1:
    st.write("## **Wikipedia (Lionel Messi)**")
with col2:
    st.markdown("<div style='height: 20px'/>", unsafe_allow_html=True)
    st.write("https://en.wikipedia.org/wiki/Lionel_Messi")

col1, col2 = st.columns(2)
st.markdown("<div style='height: 20px'/>", unsafe_allow_html=True)
with col1:
    st.write("## **Wikipedia (Cristiano Ronaldo)**")
with col2:
    st.markdown("<div style='height: 20px'/>", unsafe_allow_html=True)
    st.write("https://en.wikipedia.org/wiki/Cristiano_Ronaldo")

