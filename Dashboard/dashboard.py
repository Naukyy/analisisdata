import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk
from datetime import datetime
from sklearn.cluster import KMeans
from streamlit.components.v1 import html

@st.cache_data
def load_data():
    hour_data = pd.read_csv('data/hour.csv')
    day_data = pd.read_csv('data/day.csv')
    return hour_data, day_data

hour_data, day_data = load_data()

st.title("Dicoding Analisis Data Pada Penyewaan Sepeda")
st.sidebar.header("Pilih Analisis")
options = st.sidebar.radio("Pilih jenis analisis:", ("Analisis Suhu & Cuaca", "Analisis Per Hari & Minggu", "RFM Analysis", "Geospasial"))

if options == "Analisis Suhu & Cuaca":
    hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
    hour_data['hour'] = hour_data['dteday'].dt.hour 

    season = st.selectbox("Pilih Musim", ['Spring', 'Summer', 'Fall', 'Winter'])
    season_map = {'Spring': 1, 'Summer': 2, 'Fall': 3, 'Winter': 4}
    filtered_data = hour_data[hour_data['season'] == season_map[season]]
    st.write(f"Data untuk musim {season}:")
    st.write(filtered_data.head()) 

    # Visualisasi hubungan antara suhu dan penyewaan sepeda
    st.write("### Hubungan antara Suhu dan Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='temp', y='cnt', data=hour_data, hue='weathersit', ax=ax)
    ax.set_title("Penyewaan Sepeda vs Suhu")
    st.pyplot(fig)

    # Visualisasi hubungan antara suhu, cuaca, dan jumlah sewa sepeda
    st.subheader("Bagaimana Suhu dan Cuaca Mempengaruhi Rental Sepeda?")
    weather_grouped = hour_data.groupby('weathersit').agg({'cnt': 'sum', 'temp': 'mean', 'atemp': 'mean'}).reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='weathersit', y='cnt', data=weather_grouped, ax=ax, palette="viridis", hue='weathersit', legend=False)
    ax.set_title("Jumlah Sewa Sepeda Berdasarkan Cuaca")
    ax.set_xlabel("Cuaca")
    ax.set_ylabel("Jumlah Sepeda yang Disewa")
    st.pyplot(fig)
    st.write(weather_grouped[['weathersit', 'temp', 'atemp']])

    # Analisis pengaruh cuaca terhadap penyewaan sepeda
    st.write("### Pengaruh Cuaca terhadap Penyewaan Sepeda")
    weather_data = hour_data.groupby('weathersit').agg({'cnt': 'mean'}).reset_index()
    st.bar_chart(weather_data.set_index('weathersit')['cnt'])

if options == "Analisis Per Hari & Minggu":
    st.subheader("Analisis Penyewaan Sepeda Per Hari & Minggu")

    season = st.selectbox("Pilih Musim", ['Spring', 'Summer', 'Fall', 'Winter'])
    season_map = {'Spring': 1, 'Summer': 2, 'Fall': 3, 'Winter': 4}
    filtered_data = hour_data[hour_data['season'] == season_map[season]]
    st.write(f"Data untuk musim {season}:")
    st.write(filtered_data.head())

    # Visualisasi penyewaan sepeda berdasarkan musim
    st.write("### Penyewaan Sepeda Berdasarkan Musim")
    season_data = day_data.groupby('season').agg({'cnt': 'mean'}).reset_index()
    st.bar_chart(season_data.set_index('season')['cnt'])

    # Visualisasi penyewaan sepeda berdasarkan hari dalam minggu
    st.write("### Penyewaan Sepeda Berdasarkan Hari dalam Minggu")
    weekday_data = day_data.groupby('weekday').agg({'cnt': 'mean'}).reset_index()
    st.bar_chart(weekday_data.set_index('weekday')['cnt'])

if options == "RFM Analysis":
    st.subheader("RFM Analysis")
    
    # Mengonversi kolom 'dteday' menjadi datetime
    hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
    hour_data['Recency'] = (hour_data['dteday'].max() - hour_data['dteday']).dt.days
    rfm = hour_data.groupby('registered').agg({'Recency': 'min', 'cnt': 'sum'})
    rfm['Frequency'] = rfm['cnt'] / rfm['Recency']
    rfm['Monetary'] = rfm['cnt'] * 1  

    # Visualisasi RFM
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    sns.boxplot(ax=ax[0], x=rfm['Recency'])
    ax[0].set_title('Recency')
    sns.boxplot(ax=ax[1], x=rfm['Frequency'])
    ax[1].set_title('Frequency')
    st.pyplot(fig)

if options == "Geospasial":
    st.subheader("Peta Lokasi Penyewaan Sepeda")
    
    # Data lokasi 
    data_location = pd.DataFrame({
        'latitude': [37.7749, 37.7849, 37.7949],  
        'longitude': [-122.4194, -122.4294, -122.4394],  
        'nama_lokasi': ["Lokasi A", "Lokasi B", "Lokasi C"],  
    })

    # Peta
    deck = pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=37.7749, 
            longitude=-122.4194,  
            zoom=12,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data_location,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=100,
            ),
        ],
    )

    st.pydeck_chart(deck)
