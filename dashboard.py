import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(page_title="Data Statistik Sektoral", layout="wide")

# Judul umum
st.title("📊 Data Statistik Sektoral Kota Lubuk Linggau")
st.markdown("---")

# Sidebar navigasi
menu = st.sidebar.radio("Pilih OPD", [
    "Dinas Lingkungan Hidup (DLH)",
    "Dinas Tenaga Kerja",
    "Dinas Kesehatan",
    "Dinas Koperasi dan UKM",
    "Dinas Pertanian"
])

# Fungsi load data untuk masing-masing OPD
@st.cache_data
def load_dlh():
    return pd.read_excel("data/DLH.xlsx")

@st.cache_data
def load_disnaker():
    return pd.read_excel("data/disnaker.xlsx")

@st.cache_data
def load_dinkes():
    return pd.read_excel("data/dinkes.xlsx")

@st.cache_data
def load_diskop():
    return pd.read_excel("data/diskop.xlsx")

@st.cache_data
def load_dinper():
    return pd.read_excel("data/dinper.xlsx")

# Konten sesuai OPD
if menu == "Dinas Lingkungan Hidup (DLH)":
    st.header("♻️ Statistik Dinas Lingkungan Hidup")
    df = load_dlh()
    st.dataframe(df)
    if 'NILAI 2024 SEMESTER I' in df.columns:
        st.subheader("Visualisasi Data")
        fig, ax = plt.subplots()
        sns.barplot(data=df, y="NAMA", x="NILAI 2024 SEMESTER I", ax=ax)
        ax.set_title("Nilai Indikator DLH - 2024")
        st.pyplot(fig)

elif menu == "Dinas Tenaga Kerja":
    st.header("👷 Statistik Dinas Tenaga Kerja")
    df = load_disnaker()
    st.dataframe(df)
    if 'Jumlah' in df.columns:
        st.subheader("Visualisasi Data")
        st.bar_chart(df.set_index('Keterangan')['Jumlah'])

elif menu == "Dinas Kesehatan":
    st.header("🏥 Statistik Dinas Kesehatan")
    df = load_dinkes()
    st.dataframe(df)
    if '2023' in df.columns:
        st.subheader("Perbandingan Data")
        st.line_chart(df.set_index('Uraian')['2023'])

elif menu == "Dinas Koperasi dan UKM":
    st.header("💼 Statistik Dinas Koperasi dan UKM")
    df = load_diskop()
    st.dataframe(df)
    if '2024' in df.columns:
        umkm_df = df[df['Uraian'].str.contains("UMKM", case=False)]
        st.subheader("Jumlah UMKM per Bidang Usaha")
        st.bar_chart(umkm_df.set_index("Uraian")["2024"])

elif menu == "Dinas Pertanian":
    st.header("🌾 Statistik Dinas Pertanian")
    df = load_dinper()
    st.dataframe(df)
    if '2023' in df.columns:
        st.subheader("Tren Produksi Pertanian")
        fig, ax = plt.subplots()
        df.plot(kind='bar', x='Uraian', y='2023', ax=ax)
        st.pyplot(fig)
