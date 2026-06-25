
import streamlit as st
import pandas as pd

# here i read the final data that i made after cleaning
data = pd.read_csv("gold_final.csv")

# when i saved the csv the date return like text
# so i change it again to date because i will use it in the app
data["Date"] = pd.to_datetime(data["Date"])

# this is the title that will show in streamlit
st.title("Gold Price EDA")

# this is small explain about what the app is
st.write("This page show gold prices and economic events analysis.")

# for now i show the first rows to check the data is working
st.table(data.head())
