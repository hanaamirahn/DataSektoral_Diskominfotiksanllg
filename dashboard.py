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

# ------------------------------
# Visualisasi dasar (contoh)
# Kamu bisa ganti sesuai EDA notebook
# ------------------------------

st.subheader(f"📈 Visualisasi Data {selected_opd}")

if selected_opd == "DLH":
    # Contoh visualisasi DLH
    st.write("Contoh: Jumlah data per kolom")
    st.bar_chart(df.count())

elif selected_opd == "DISNAKER":
    st.write("Contoh: Statistik Deskriptif")
    st.write(df.describe())

    # Contoh visualisasi tambahan
    if "Bidang" in df.columns:
        bidang_counts = df['Bidang'].value_counts()
        fig, ax = plt.subplots()
        bidang_counts.plot(kind='bar', ax=ax)
        ax.set_title("Jumlah Bidang")
        st.pyplot(fig)

elif selected_opd == "DINKES":
    st.write("Contoh: Histogram Kolom Numerik")
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    if len(num_cols) > 0:
        col = st.selectbox("Pilih Kolom", num_cols)
        fig, ax = plt.subplots()
        sns.histplot(df[col], kde=True, ax=ax)
        ax.set_title(f"Histogram {col}")
        st.pyplot(fig)

elif selected_opd == "DISKOP":
    st.write("Contoh: Pie Chart Uraian")
    if "Uraian" in df.columns:
        uraian_counts = df['Uraian'].value_counts().head(5)
        fig, ax = plt.subplots()
        ax.pie(uraian_counts, labels=uraian_counts.index, autopct='%1.1f%%')
        ax.set_title("5 Besar Uraian")
        st.pyplot(fig)

elif selected_opd == "DINPER":
    st.write("Contoh: Barplot Jumlah per Kategori")
    if "Kategori" in df.columns:
        kategori_counts = df['Kategori'].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=kategori_counts.index, y=kategori_counts.values, ax=ax)
        ax.set_title("Jumlah per Kategori")
        st.pyplot(fig)
