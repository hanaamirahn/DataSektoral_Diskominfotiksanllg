import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul halaman
st.set_page_config(page_title="Dashboard Statistik Lubuk Linggau", layout="wide")
st.title("📊 Data Statistik Sektoral Kota Lubuk Linggau")
st.markdown("---")

# Sidebar menu
menu = st.sidebar.radio("Pilih OPD:", [
    "Dinas Lingkungan Hidup (DLH)",
    "Dinas Tenaga Kerja",
    "Dinas Kesehatan",
    "Dinas Koperasi dan UKM",
    "Dinas Pertanian"
])

# ========== 1. DLH ==========
if menu == "Dinas Lingkungan Hidup (DLH)":
    st.header("♻️ Dinas Lingkungan Hidup")
    # Contoh kode dari notebook DLH
    import pandas as pd
    dlh_df = pd.read_csv("/content/Dinas Lingkungan Hidup.csv")
    alat_mask = dlh_df['NAMA'].str.contains("Jumlah", case=False)
    alat_data = dlh_df[alat_mask][['NAMA', 'NILAI 2024 SEMESTER I']].copy()
    alat_data['NILAI 2024 SEMESTER I'] = pd.to_numeric(alat_data['NILAI 2024 SEMESTER I'], errors='coerce')
    st.dataframe(alat_data)
    st.bar_chart(alat_data.set_index("NAMA"))

# ========== 2. Disnaker ==========
elif menu == "Dinas Tenaga Kerja":
    st.header("👷 Dinas Tenaga Kerja")
    df = pd.read_csv("/content/disnaker.csv")
    st.dataframe(df)
    st.bar_chart(df.set_index("Keterangan")["Jumlah"])

# ========== 3. Dinkes ==========
elif menu == "Dinas Kesehatan":
    st.header("🏥 Dinas Kesehatan")
    df = pd.read_csv("/content/dinkes.csv")
    st.dataframe(df)
    if "2023" in df.columns:
        st.line_chart(df.set_index("Uraian")["2023"])

# ========== 4. Diskop ==========
elif menu == "Dinas Koperasi dan UKM":
    st.header("💼 Dinas Koperasi dan UKM")
    df = pd.read_csv("/content/diskop.csv")
    umkm_df = df[df["Uraian"].str.contains("UMKM", case=False)].copy()
    st.dataframe(umkm_df)
    st.bar_chart(umkm_df.set_index("Uraian")["2024"])

# ========== 5. Dinper ==========
elif menu == "Dinas Pertanian":
    st.header("🌾 Dinas Pertanian")
    df = pd.read_csv("/content/Dinas Pertanian.csv")
    st.dataframe(df)
    if "2023" in df.columns:
        st.bar_chart(df.set_index("Uraian")["2023"])
