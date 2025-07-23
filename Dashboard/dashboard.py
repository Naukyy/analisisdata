import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Memuat dataset
data_hour = pd.read_csv('data/hour.csv')

st.title('Dashboard Sepeda Sharing')

# Menampilkan data
st.write("Data Sepeda Sewa per Jam")
st.write(data_hour.head())

# Visualisasi
st.write("Distribusi Sepeda yang Disewa per Jam")
plt.figure(figsize=(10, 6))
sns.histplot(data_hour['cnt'], kde=True)
st.pyplot(plt)

selected_hour = st.slider('Pilih Jam', min_value=0, max_value=23)
filtered_data = data_hour[data_hour['hr'] == selected_hour]
st.write(filtered_data)
