import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Data Statistik Lubuklinggau", layout="wide")

# Judul utama
st.title("📊 Data Statistik Sektoral Kota Lubuk Linggau")
st.markdown("---")

# Sidebar pilihan OPD
menu = st.sidebar.radio("Pilih OPD:", [
    "Dinas Lingkungan Hidup (DLH)",
    "Dinas Tenaga Kerja",
    "Dinas Kesehatan",
    "Dinas Koperasi dan UKM",
    "Dinas Pertanian"
])

# ======= DLH =======
if menu == "Dinas Lingkungan Hidup (DLH)":
    st.header("♻️ Dinas Lingkungan Hidup")
    dlh_df = pd.read_csv("data/DLH.csv")  # pastikan nama dan lokasi file benar
    alat_mask = dlh_df['NAMA'].str.contains("Jumlah", case=False)
    alat_data = dlh_df[alat_mask][['NAMA', 'NILAI 2024 SEMESTER I']].copy()
    alat_data['NILAI 2024 SEMESTER I'] = pd.to_numeric(alat_data['NILAI 2024 SEMESTER I'], errors='coerce')
    st.dataframe(alat_data)
    st.bar_chart(alat_data.set_index("NAMA"))

# ======= DISNAKER =======
elif menu == "Dinas Tenaga Kerja":
    st.header("👷 Dinas Tenaga Kerja")
    df = pd.read_csv("data/disnaker.csv")
    st.dataframe(df)
    if "Jumlah" in df.columns:
        st.bar_chart(df.set_index("Keterangan")["Jumlah"])

# ======= DINKES =======
elif menu == "Dinas Kesehatan":
    st.header("🏥 Dinas Kesehatan")
    df = pd.read_csv("data/dinkes.csv")
    st.dataframe(df)
    if "2023" in df.columns and "Uraian" in df.columns:
        st.line_chart(df.set_index("Uraian")["2023"])

# ======= DISKOP =======
elif menu == "Dinas Koperasi dan UKM":
    st.header("💼 Dinas Koperasi dan UKM")
    df = pd.read_csv("data/diskop.csv")
    st.dataframe(df)
    if "Uraian" in df.columns and "2024" in df.columns:
        umkm_df = df[df["Uraian"].str.contains("UMKM", case=False)]
        st.bar_chart(umkm_df.set_index("Uraian")["2024"])

# ======= DINPER =======
elif menu == "Dinas Pertanian":
    st.header("🌾 Dinas Pertanian")
    df = pd.read_csv("data/dinper.csv")
    st.dataframe(df)
    if "Uraian" in df.columns and "2023" in df.columns:
        st.bar_chart(df.set_index("Uraian")["2023"])
