import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------
# Pengaturan halaman
# ------------------------------
st.set_page_config(
    page_title="DATA STATISTIK SEKTORAL KOTA LUBUK LINGGAU",
    layout="wide"
)

st.title("📊 DATA STATISTIK SEKTORAL KOTA LUBUK LINGGAU")

# ------------------------------
# Sidebar OPD Selector
# ------------------------------
opd_list = {
    "DLH": "dataset/DLH.csv",
    "DISNAKER": "dataset/disnaker.csv",
    "DINKES": "dataset/dinkes.csv",
    "DISKOP": "dataset/diskop.csv",
    "DINPER": "dataset/dinper.csv"
}

selected_opd = st.sidebar.selectbox(
    "Pilih OPD",
    list(opd_list.keys())
)

# ------------------------------
# Load dataset sesuai pilihan
# ------------------------------
data_path = opd_list[selected_opd]
df = pd.read_csv(data_path)

st.header(f"📌 Data {selected_opd}")
st.dataframe(df)

st.subheader(f"📈 Visualisasi Data {selected_opd}")

# ------------------------------
# Visualisasi untuk setiap OPD
# ------------------------------

if selected_opd == "DLH":
    # Contoh EDA: Hitung total sampah per tahun
    if 'Tahun' in df.columns and 'Jumlah Sampah' in df.columns:
        fig, ax = plt.subplots()
        df.groupby('Tahun')['Jumlah Sampah'].sum().plot(kind='bar', ax=ax)
        ax.set_title('Total Jumlah Sampah per Tahun')
        ax.set_xlabel('Tahun')
        ax.set_ylabel('Ton')
        st.pyplot(fig)

    # Visualisasi tambahan DLH (contoh)
    if 'Jenis Sampah' in df.columns:
        fig, ax = plt.subplots()
        df['Jenis Sampah'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel('')
        ax.set_title('Distribusi Jenis Sampah')
        st.pyplot(fig)

elif selected_opd == "DISNAKER":
    # Contoh EDA: Jumlah tenaga kerja per bidang
    if 'Bidang' in df.columns and 'Jumlah' in df.columns:
        bidang_counts = df.groupby('Bidang')['Jumlah'].sum()
        fig, ax = plt.subplots()
        bidang_counts.plot(kind='bar', ax=ax)
        ax.set_title('Jumlah Tenaga Kerja per Bidang')
        st.pyplot(fig)

    # Visualisasi tambahan DISNAKER
    if 'Tahun' in df.columns:
        fig, ax = plt.subplots()
        sns.lineplot(data=df, x='Tahun', y='Jumlah', ax=ax)
        ax.set_title('Trend Tenaga Kerja per Tahun')
        st.pyplot(fig)

elif selected_opd == "DINKES":
    # Contoh EDA: Jumlah Fasilitas Kesehatan per Kecamatan
    if 'Kecamatan' in df.columns:
        kecamatan_counts = df['Kecamatan'].value_counts()
        fig, ax = plt.subplots()
        kecamatan_counts.plot(kind='bar', ax=ax)
        ax.set_title('Jumlah Fasilitas Kesehatan per Kecamatan')
        st.pyplot(fig)

    # Visualisasi tambahan DINKES
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(num_cols) > 0:
        col = st.selectbox("Pilih Kolom Numerik", num_cols)
        fig, ax = plt.subplots()
        sns.histplot(df[col], kde=True, ax=ax)
        ax.set_title(f"Distribusi {col}")
        st.pyplot(fig)

elif selected_opd == "DISKOP":
    # Contoh EDA: Jumlah UMKM per Bidang Usaha
    if 'Bidang Usaha' in df.columns and '2024' in df.columns:
        bidang_counts = df.groupby('Bidang Usaha')['2024'].sum()
        fig, ax = plt.subplots()
        bidang_counts.plot(kind='bar', ax=ax)
        ax.set_title('Jumlah UMKM per Bidang Usaha')
        st.pyplot(fig)

    # Visualisasi tambahan DISKOP
    if 'Uraian' in df.columns:
        uraian_counts = df['Uraian'].value_counts().head(10)
        fig, ax = plt.subplots()
        uraian_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel('')
        ax.set_title('10 Besar Uraian')
        st.pyplot(fig)

elif selected_opd == "DINPER":
    # Contoh EDA: Jumlah Program per Tahun
    if 'Tahun' in df.columns and 'Jumlah Program' in df.columns:
        fig, ax = plt.subplots()
        df.groupby('Tahun')['Jumlah Program'].sum().plot(kind='line', marker='o', ax=ax)
        ax.set_title('Jumlah Program per Tahun')
        st.pyplot(fig)

    # Visualisasi tambahan DINPER
    if 'Kategori' in df.columns:
        kategori_counts = df['Kategori'].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=kategori_counts.index, y=kategori_counts.values, ax=ax)
        ax.set_title('Jumlah per Kategori')
        st.pyplot(fig)
