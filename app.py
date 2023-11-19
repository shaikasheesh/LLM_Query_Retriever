import streamlit as st
from query_db import query_from_db

st.title("AtliQ T Shirts: Database Q&A")

question = st.text_input("Question: ")

if question:
    chain = query_from_db()
    response = chain.run(question)

    st.header("Answer")
    st.write(response)