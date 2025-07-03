import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# PENGATURAN UMUM HALAMAN
# -----------------------------
st.set_page_config(
    page_title="DATA STATISTIK SEKTORAL KOTA LUBUK LINGGAU",
    layout="wide"
)

st.title("📊 DATA STATISTIK SEKTORAL KOTA LUBUK LINGGAU")

# -----------------------------
# SIDEBAR PILIHAN OPD
# -----------------------------
opd_list = {
    "DLH": "dataset/DLH.csv",
    "DISKOP": "dataset/Dinas Koperasi UMKM.csv",
    "DINKES": "dataset/Dinkes.csv",
    "DINAKER": "dataset/Disnaker.csv",
    "DINPER": "dataset/Dinas Pertanian.csv",
}

selected_opd = st.sidebar.selectbox(
    "Pilih OPD",
    list(opd_list.keys())
)

# -----------------------------
# LOAD DATA
# -----------------------------
data_path = opd_list[selected_opd]
df = pd.read_csv(data_path)

# -----------------------------
# TAMPILKAN DATA + VISUALISASI
# -----------------------------
st.header(f"📌 Data & Visualisasi {selected_opd}")

# -----------------------------
# DLH
# -----------------------------
if selected_opd == "DLH":
    # Volume Air Limbah
    limbah_data = df[df['NAMA'].str.contains("Volume Air Limbah", case=False)].copy()
    limbah_data['Kecamatan'] = limbah_data['NAMA'].str.replace('Volume Air Limbah Kecamatan ', '', regex=False)
    limbah_table = limbah_data[['Kecamatan', 'NILAI 2024 SEMESTER I']].rename(columns={'NILAI 2024 SEMESTER I': 'Volume Limbah (Liter)'})
    total = limbah_table['Volume Limbah (Liter)'].sum()
    limbah_table = pd.concat([limbah_table, pd.DataFrame({'Kecamatan': ['Total'], 'Volume Limbah (Liter)': [total]})], ignore_index=True)

    st.subheader("Tabel Volume Air Limbah Di Kota Lubuklinggau Tahun 2024")
    st.dataframe(limbah_table)

    st.subheader("Diagram Volume Air Limbah per Kecamatan Tahun 2024")
    limbah_plot = limbah_table[limbah_table['Kecamatan'] != 'Total'].sort_values('Volume Limbah (Liter)', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=limbah_plot, x='Kecamatan', y='Volume Limbah (Liter)', palette="Spectral", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Komposisi Sampah
    komposisi_data = df[df['NAMA'].str.contains("Komposisi Sampah", case=False)].copy()
    komposisi_data['Jenis Sampah'] = komposisi_data['NAMA'].str.replace('Komposisi Sampah ', '', regex=False)
    komposisi_table = komposisi_data[['Jenis Sampah', 'NILAI 2024 SEMESTER I']].rename(columns={'NILAI 2024 SEMESTER I': 'Persentase (%)'})
    total = komposisi_table['Persentase (%)'].sum()
    komposisi_table = pd.concat([komposisi_table, pd.DataFrame({'Jenis Sampah': ['Total'], 'Persentase (%)': [total]})], ignore_index=True)

    st.subheader("Tabel Komposisi Sampah Kota Lubuk Linggau Tahun 2024")
    st.dataframe(komposisi_table)

    st.subheader("Diagram Komposisi Sampah Kota Lubuk Linggau Tahun 2024")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(komposisi_table[:-1]['Persentase (%)'], labels=komposisi_table[:-1]['Jenis Sampah'], autopct='%1.1f%%', startangle=140)
    st.pyplot(fig)

    # Jumlah Alat Angkut Sampah
    alat_data = df[df['NAMA'].str.contains("Jumlah", case=False)].copy()
    alat_data['Jenis Alat'] = alat_data['NAMA'].str.replace('Jumlah Alat Angkut Sampah ', '', regex=False)
    alat_table = alat_data[['Jenis Alat', 'NILAI 2024 SEMESTER I']].rename(columns={'NILAI 2024 SEMESTER I': 'Jumlah'})
    total = alat_table['Jumlah'].sum()
    alat_table = pd.concat([alat_table, pd.DataFrame({'Jenis Alat': ['Total'], 'Jumlah': [total]})], ignore_index=True)

    st.subheader("Tabel Jumlah Alat Angkut Sampah Kota Lubuklinggau Tahun 2024")
    st.dataframe(alat_table)

    st.subheader("Diagram Jumlah Alat Angkut Sampah Kota Lubuklinggau Tahun 2024")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=alat_table[:-1], y='Jenis Alat', x='Jumlah', palette="Dark2", ax=ax)
    st.pyplot(fig)

# -----------------------------
# DISKOP
# -----------------------------
elif selected_opd == "DISKOP":
    umkm_data = df[df['Uraian'].str.contains("UMKM", case=False)].copy()
    umkm_data['Bidang Usaha'] = umkm_data['Uraian'].str.replace('Jumlah UMKM Bidang ', '', regex=False)
    umkm_table = umkm_data[['Bidang Usaha', '2024']].rename(columns={'2024': 'Jumlah'})
    umkm_table = pd.concat([umkm_table, pd.DataFrame({'Bidang Usaha': ['Total'], 'Jumlah': [umkm_table['Jumlah'].sum()]})], ignore_index=True)

    st.subheader("Tabel Jumlah UMKM Kota Lubuk Linggau Tahun 2024")
    st.dataframe(umkm_table)

    st.subheader("Diagram Jumlah UMKM per Bidang Usaha Tahun 2024")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=umkm_table[:-1], y='Bidang Usaha', x='Jumlah', palette="coolwarm", ax=ax)
    st.pyplot(fig)

    # Koperasi Aktif Simpan Pinjam Mandiri
    simpan_aktif = df[df['Uraian'].str.contains("koperasi aktif simpan pinjam", case=False)].copy()
    st.subheader("Tabel Jumlah Koperasi Aktif Simpan Pinjam Mandiri")
    st.dataframe(simpan_aktif)

    st.subheader("Diagram Jumlah Koperasi Aktif Simpan Pinjam Mandiri (2022–2024)")
    fig, ax = plt.subplots()
    tahun = ['2022', '2023', '2024']
    jumlah = [simpan_aktif[tahun].values[0] for tahun in tahun]
    ax.plot(tahun, jumlah, marker='o', linestyle='-', color='teal')
    st.pyplot(fig)

    # Koperasi Aktif Serba Usaha Mandiri
    serba_aktif = df[df['Uraian'].str.contains("koperasi aktif serba usaha", case=False)].copy()
    st.subheader("Tabel Jumlah Koperasi Aktif Serba Usaha Mandiri")
    st.dataframe(serba_aktif)

    st.subheader("Diagram Jumlah Koperasi Aktif Serba Usaha Mandiri (2022–2024)")
    fig, ax = plt.subplots()
    jumlah = [serba_aktif[tahun].values[0] for tahun in tahun]
    ax.barh(tahun, jumlah, color='skyblue')
    st.pyplot(fig)

# -----------------------------
# DINKES
# -----------------------------
elif selected_opd == "DINKES":
    penyakit = df[df['Jenis Data'].str.contains("Penderita", case=False)].copy()
    st.subheader("Tabel Jenis Penyakit Menular Tahun 2024")
    st.dataframe(penyakit[['Jenis Data', '2024']])

    st.subheader("Diagram Jumlah Penyakit Menular Tahun 2024 per Jenis")
    fig, ax = plt.subplots(figsize=(10, 6))
    penyakit_sorted = penyakit[['Jenis Data', '2024']].sort_values(by='2024', ascending=True)
    sns.barplot(data=penyakit_sorted, x='2024', y='Jenis Data', palette="flare", ax=ax)
    st.pyplot(fig)

    balita = df[df['Jenis Data'].str.contains("Balita", case=False)].copy()
    st.subheader("Tabel Jumlah Balita Wasting dan Stunting 2024")
    st.dataframe(balita[['Jenis Data', '2024']])

    st.subheader("Diagram Distribusi Jumlah Balita Wasting dan Stunting 2024")
    fig, ax = plt.subplots()
    ax.pie(balita['2024'], labels=balita['Jenis Data'], autopct='%1.1f%%', startangle=140)
    st.pyplot(fig)

    tenagamedis = df[df['Jenis Data'].str.contains("Dokter", case=False)].copy()
    st.subheader("Jumlah Tenaga Medis Tahun 2024")
    st.dataframe(tenagamedis[['Jenis Data', '2024']])

    st.subheader("Jumlah Tenaga Kesehatan Tahun 2024")
    nakes_keywords = ['Bidan', 'Perawat', 'Apoteker', 'Teknis Kefarmasian', 'Psikologis Klinis']
    nakes = df[df['Jenis Data'].str.contains('|'.join(nakes_keywords), case=False)].copy()
    st.dataframe(nakes[['Jenis Data', '2024']])

    st.subheader("Diagram Jumlah Tenaga Kesehatan Tahun 2024")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(nakes['2024'], labels=nakes['Jenis Data'], autopct='%1.1f%%', startangle=140)
    st.pyplot(fig)
