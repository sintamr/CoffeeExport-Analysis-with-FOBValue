import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set konfigurasi
st.set_page_config(page_title="Analisis Kopi Indonesia", layout="wide")
st.title("📊 Analisis Data Perkebunan & Ekspor Kopi Indonesia")

# Load data
luasdanproduksi = pd.read_excel("Dataset/Luas dan produksi (upload).xlsx")
ekspor = pd.read_excel("Dataset/Nilai ekspor (upload).xlsx")

gabungan = pd.concat([luasdanproduksi, ekspor], ignore_index=True)
gabungan = gabungan.drop(index=[38,57], errors='ignore')

# Ringkasan Data
st.subheader("Ringkasan Data Gabungan")
st.dataframe(gabungan.describe(include='all'))

# Top 5 Provinsi berdasarkan Luas Areal
st.subheader("Top 5 Provinsi Berdasarkan Luas Areal")
top5_provinsi = gabungan.nlargest(5, 'Luas Areal Perkebunan Kopi (Ribu Hektar)')

fig, ax1 = plt.subplots(figsize=(7, 3))
sns.barplot(
    x='38 Provinsi',
    y='Luas Areal Perkebunan Kopi (Ribu Hektar)',
    data=top5_provinsi,
    label='Luas Areal',
    color='skyblue',
    ax=ax1
)

ax2 = ax1.twinx()
sns.lineplot(
    x='38 Provinsi',
    y='Produksi Perkebunan Kopi (Ribu Ton)',
    data=top5_provinsi,
    marker='o',
    color='red',
    ax=ax2
)

ax1.set_xlabel('Provinsi')
ax1.set_ylabel('Luas Areal')
ax2.set_ylabel('Produksi')
fig.tight_layout()
st.pyplot(fig)

# Scatterplot Luas vs Produksi
st.subheader("Luas Areal vs Produksi")
fig2, ax = plt.subplots(figsize=(6, 4))
sns.scatterplot(x='Luas Areal Perkebunan Kopi (Ribu Hektar)',
                y='Produksi Perkebunan Kopi (Ribu Ton)', data=gabungan, ax=ax)
ax.set_title('Luas Areal vs Produksi')
st.pyplot(fig2)

# Ekspor vs FOB
st.subheader("Ekspor Kopi vs Nilai FOB")
fig3, ax1 = plt.subplots(figsize=(10, 5))
sns.lineplot(x='Negara Tujuan', y='Nilai FOB (US$)', data=gabungan, color='red', marker='o', ax=ax1)
ax1.set_xticklabels(gabungan['Negara Tujuan'], rotation=45, ha='right')
ax2 = ax1.twinx()
sns.barplot(x='Negara Tujuan', y='Berat Bersih Ekspor Kopi (Ton)', data=gabungan, color='blue', ax=ax2)
ax1.set_ylabel('Nilai FOB (US$)')
ax2.set_ylabel('Berat Bersih Ekspor Kopi (Ton)')
fig3.tight_layout()
st.pyplot(fig3)

# Pie Chart Produksi vs Ekspor
st.subheader("Perbandingan Total Produksi dan Ekspor Kopi")
produksi_total = gabungan['Produksi Perkebunan Kopi (Ribu Ton)'].sum()
ekspor_total = gabungan['Berat Bersih Ekspor Kopi (Ton)'].sum()

data = {'Produksi': produksi_total, 'Ekspor': ekspor_total}
fig4, ax = plt.subplots(figsize=(4, 4))
ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig4)
