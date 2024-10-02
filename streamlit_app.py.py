import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_csv('sample_data/day.csv')
data2 = pd.read_csv('sample_data/hour.csv')

data.isnull().sum()

data['dteday'] = pd.to_datetime(data['dteday'])

season_data = data.groupby('season')['cnt'].mean()
print(season_data)

st.title("Data Peminjaman sepeda ")

heatmap_data = data.pivot_table(values='cnt', index='season', columns='weekday', aggfunc='sum')
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='.0f', linewidths=.5)
plt.title('Total Peminjaman Sepeda per Musim dan Hari dalam Seminggu')
plt.xlabel('Hari dalam Seminggu')
plt.ylabel('Musim')
plt.xticks(ticks=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], labels=['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'])
plt.yticks(ticks=[0.5, 1.5, 2.5, 3.5], labels=['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur'])
plt.show()



page = st.sidebar.radio("Page:", ["Visualisasi", "EDA", "RFM"])



if page == "Visualisasi":

    st.write("## Chart Peminjaman Sepeda Per Bulan")
    fig, ax = plt.subplots()
    data.groupby('mnth')['cnt'].sum().plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Total Peminjaman Sepeda per Bulan')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Peminjaman')

    st.pyplot(fig)

    st.write("## Chart Peminjaman Sepeda Per Musim")

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    data.groupby('season')['cnt'].sum().plot(kind='bar', ax=ax2, color='orange')
    ax2.set_title('Total Peminjaman Sepeda per Musim')
    ax2.set_xlabel('Musim')
    ax2.set_ylabel('Jumlah Peminjaman')
    ax2.set_xticklabels(['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur'], rotation=0)

    st.pyplot(fig2)
    
    st.write("## Visualisasi Jumlah Peminjaman Sepeda per Jam")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    data2.groupby('hr')['cnt'].sum().plot(kind='line', ax=ax3, marker='o', color='green')
    ax3.set_title('Total Peminjaman Sepeda per Jam')
    ax3.set_xlabel('Jam')
    ax3.set_ylabel('Jumlah Peminjaman')
    st.pyplot(fig3)
    
    st.write("## Visualisasi Jumlah Peminjaman Sepeda per Hari dalam Seminggu")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    data.groupby('weekday')['cnt'].sum().plot(kind='bar', ax=ax2, color='skyblue')
    ax2.set_title('Total Peminjaman Sepeda per Hari dalam Seminggu')
    ax2.set_xlabel('Hari dalam Seminggu')
    ax2.set_ylabel('Jumlah Peminjaman')
    ax2.set_xticklabels(['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'], rotation=0)
    st.pyplot(fig2)

elif page == "EDA":
    st.title("Exploratory Data Analysis (EDA)")
    
    st.write("## Dataset Bike Sharing (Data Harian)")
    st.dataframe(data.head(40))

    st.write("## Dataset Bike Sharing (Data Per Jam)")
    st.dataframe(data2.head(40))
    
    st.write("## Statistik Deskriptif Dataset")
    st.write(data.describe())


    st.write("## Distribusi Jumlah Peminjaman Sepeda")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['cnt'], bins=30, kde=True, ax=ax)
    ax.set_title('Distribusi Jumlah Peminjaman Sepeda')
    st.pyplot(fig)

    st.write("## Heatmap Korelasi")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    correlation = data.corr()
    sns.heatmap(correlation, annot=True, fmt=".2f", cmap='coolwarm', ax=ax2)
    st.pyplot(fig2)

elif page == "RFM":
    st.title("Analisis RFM (Recency, Frequency, Monetary)")
    st.write("## Deskripsi RFM")
    st.write("Analisis RFM bertujuan untuk memahami perilaku pengguna berdasarkan tiga aspek utama:")
    st.write("- **Recency**: Seberapa baru pengguna melakukan pembelian.")
    st.write("- **Frequency**: Seberapa sering pengguna melakukan pembelian.")
    st.write("- **Monetary**: Seberapa banyak pengguna membelanjakan.")
    
    rfm_data = data.groupby('instant').agg({
        'cnt': 'sum',
        'temp': 'mean', 
        'hum': 'mean'    
    }).reset_index()

    rfm_data['Recency'] = rfm_data['instant']#berdasar waktu
    rfm_data['Frequency'] = rfm_data['cnt'] #berdasarkan total sewa
    rfm_data['Monetary'] = rfm_data['cnt'] * rfm_data['temp']  # Contoh, Monetary dihitung dari total sewa dikali suhu

    st.write("## Data RFM")
    st.dataframe(rfm_data)

    st.write("## Visualisasi Data RFM")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=rfm_data, x='Recency', y='Frequency', size='Monetary', sizes=(20, 200), ax=ax3)
    ax3.set_title('Analisis RFM')
    ax3.set_xlabel('Recency')
    ax3.set_ylabel('Frequency')
    st.pyplot(fig3)

