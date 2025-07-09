import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="DATA STATISTIK SEKTORAL KOTA LUBUK LINGGAU",
    layout="wide"
)

st.markdown(
    """
    <h1 style='text-align: center;'>🏛️ DATA STATISTIK SEKTORAL KOTA LUBUK LINGGAU 📊</h1>
    """,
    unsafe_allow_html=True
)

opd_list = {
    "Dinas Lingkungan Hidup": "dataset/dlh_clean.csv",
    "Dinas Koperasi dan UMKM": "dataset/diskop_clean.csv",
    "Dinas Kesehatan": "dataset/dinkes_clean.csv",
    "Dinas Ketenagakerjaan": "dataset/disnaker_clean.csv",
    "Dinas Pertanian": "dataset/dinper_clean.csv",
}

selected_opd = st.sidebar.selectbox(
    "Pilih OPD",
    list(opd_list.keys())
)

data_path = opd_list[selected_opd]
df = pd.read_csv(data_path)

st.markdown(
    f"""
    <h2 style='text-align: center;'> {selected_opd}</h2>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# DLH
# -----------------------------
if selected_opd == "Dinas Lingkungan Hidup":
    limbah_data = df[df['NAMA'].str.contains("Volume Air Limbah", case=False)].copy()
    limbah_data['Kecamatan'] = limbah_data['NAMA'].str.replace('Volume Air Limbah Kecamatan ', '', regex=False)
    limbah_table = limbah_data[['Kecamatan', 'NILAI 2024 SEMESTER I']].rename(columns={'NILAI 2024 SEMESTER I': 'Volume Limbah (Liter)'})
    total = limbah_table['Volume Limbah (Liter)'].sum()
    limbah_table = pd.concat([limbah_table, pd.DataFrame({'Kecamatan': ['Total'], 'Volume Limbah (Liter)': [total]})], ignore_index=True)
    st.subheader("Volume Air Limbah Tahun 2024")
    st.dataframe(limbah_table)

    fig, ax = plt.subplots(figsize=(10, 6))
    plot = sns.barplot(data=limbah_table[limbah_table['Kecamatan'] != 'Total'], x='Kecamatan', y='Volume Limbah (Liter)', palette="Spectral", ax=ax)
    plt.xticks(rotation=45)
    for p in plot.patches:
        ax.annotate(f"{p.get_height():,.0f}", 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', xytext=(0, 8), textcoords='offset points')
    st.pyplot(fig)

    komposisi_data = df[df['NAMA'].str.contains("Komposisi Sampah", case=False)].copy()
    komposisi_data['Jenis Sampah'] = komposisi_data['NAMA'].str.replace('Komposisi Sampah ', '', regex=False)
    komposisi_table = komposisi_data[['Jenis Sampah', 'NILAI 2024 SEMESTER I']].rename(columns={'NILAI 2024 SEMESTER I': 'Persentase (%)'})
    total = komposisi_table['Persentase (%)'].sum()
    komposisi_table = pd.concat([komposisi_table, pd.DataFrame({'Jenis Sampah': ['Total'], 'Persentase (%)': [total]})], ignore_index=True)
    st.subheader("Komposisi Sampah Tahun 2024")
    st.dataframe(komposisi_table)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(komposisi_table[:-1]['Persentase (%)'], labels=komposisi_table[:-1]['Jenis Sampah'], autopct='%1.1f%%', startangle=140)
    st.pyplot(fig)

    alat_data = df[df['NAMA'].str.contains("Jumlah", case=False)].copy()
    alat_data['Jenis Alat'] = alat_data['NAMA'].str.replace('Jumlah Alat Angkut Sampah ', '', regex=False)
    alat_table = alat_data[['Jenis Alat', 'NILAI 2024 SEMESTER I']].rename(columns={'NILAI 2024 SEMESTER I': 'Jumlah'})
    total = alat_table['Jumlah'].sum()
    alat_table = pd.concat([alat_table, pd.DataFrame({'Jenis Alat': ['Total'], 'Jumlah': [total]})], ignore_index=True)
    st.subheader("Jumlah Alat Angkut Sampah Tahun 2024")
    st.dataframe(alat_table)

    fig, ax = plt.subplots(figsize=(10, 6))
    plot = sns.barplot(data=alat_table[:-1], y='Jenis Alat', x='Jumlah', palette="Dark2", ax=ax)
    for p in plot.patches:
        ax.annotate(f"{p.get_width():,.0f}", 
                    (p.get_width(), p.get_y() + p.get_height() / 2), 
                    ha='left', va='center', xytext=(5, 0), textcoords='offset points')
    st.pyplot(fig)

# -----------------------------
# DISKOP
# -----------------------------
elif selected_opd == "Dinas Koperasi dan UMKM":
    umkm_data = df[df['Uraian'].str.contains("UMKM", case=False)].copy()
    umkm_data['Bidang Usaha'] = umkm_data['Uraian'].str.replace('Jumlah UMKM Bidang ', '', regex=False)
    umkm_table = umkm_data[['Bidang Usaha', '2024']].rename(columns={'2024': 'Jumlah'})
    umkm_table = pd.concat([umkm_table, pd.DataFrame({'Bidang Usaha': ['Total'], 'Jumlah': [umkm_table['Jumlah'].sum()]})], ignore_index=True)
    st.subheader("Jumlah UMKM Tahun 2024")
    st.dataframe(umkm_table)

    fig, ax = plt.subplots(figsize=(10, 6))
    plot = sns.barplot(data=umkm_table[:-1], y='Bidang Usaha', x='Jumlah', palette="coolwarm", ax=ax)
    for p in plot.patches:
        ax.annotate(f"{p.get_width():,.0f}",
                    (p.get_width(), p.get_y() + p.get_height() / 2),
                    ha='left', va='center', xytext=(5, 0), textcoords='offset points')
    st.pyplot(fig)

    simpan_aktif = df[df['Uraian'].str.contains("koperasi aktif simpan pinjam", case=False)].copy()
    st.subheader("Jumlah Koperasi Aktif Simpan Pinjam Mandiri Tahun (2022–2024)")
    st.dataframe(simpan_aktif)

    fig, ax = plt.subplots()
    tahun = ['2022', '2023', '2024']
    jumlah = [simpan_aktif[tahun].values[0] for tahun in tahun]
    ax.plot(tahun, jumlah, marker='o', linestyle='-', color='teal')
    for i, val in enumerate(jumlah):
        ax.text(i, val + 1, f"{val}")
    st.pyplot(fig)

    serba_aktif = df[df['Uraian'].str.contains("koperasi aktif serba usaha", case=False)].copy()
    st.subheader("Jumlah Koperasi Aktif Serba Usaha Mandiri Tahun (2022–2024)")
    st.dataframe(serba_aktif)

    fig, ax = plt.subplots()
    jumlah = [serba_aktif[tahun].values[0] for tahun in tahun]
    bars = ax.barh(tahun, jumlah, color='skyblue')
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1, bar.get_y() + bar.get_height() / 2, f"{width}", va='center')
    st.pyplot(fig)

# -----------------------------
# DINKES
# -----------------------------
elif selected_opd == "Dinas Kesehatan":
    penyakit = df[df['Jenis Data'].str.contains("Penderita", case=False)].copy()
    st.subheader("Jumlah Penyakit Menular Tahun 2024")
    st.dataframe(penyakit[['Jenis Data', '2024']])
    fig, ax = plt.subplots(figsize=(10, 6))
    plot = sns.barplot(data=penyakit, x='2024', y='Jenis Data', palette="flare", ax=ax)
    for p in plot.patches:
        ax.annotate(f"{p.get_width():,.0f}",
                    (p.get_width(), p.get_y() + p.get_height() / 2),
                    ha='left', va='center', xytext=(5, 0), textcoords='offset points')
    st.pyplot(fig)

    balita = df[df['Jenis Data'].str.contains("Balita", case=False)].copy()
    st.subheader("Jumlah Balita Wasting dan Stunting Tahun 2024")
    st.dataframe(balita[['Jenis Data', '2024']])
    fig, ax = plt.subplots()
    ax.pie(balita['2024'], labels=balita['Jenis Data'], autopct='%1.1f%%', startangle=140)
    st.pyplot(fig)

    tenagamedis = df[df['Jenis Data'].str.contains("Dokter", case=False)].copy()
    st.subheader("Jumlah Tenaga Medis Tahun 2024")
    st.dataframe(tenagamedis[['Jenis Data', '2024']])
    nakes_keywords = ['Bidan', 'Perawat', 'Apoteker', 'Teknis Kefarmasian', 'Psikologis Klinis']
    nakes = df[df['Jenis Data'].str.contains('|'.join(nakes_keywords), case=False)].copy()
    st.subheader("Jumlah Tenaga Kesehatan Tahun 2024")
    st.dataframe(nakes[['Jenis Data', '2024']])
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(nakes['2024'], labels=nakes['Jenis Data'], autopct='%1.1f%%', startangle=140)
    st.pyplot(fig)

# -----------------------------
# DISNAKER
# -----------------------------
elif selected_opd == "Dinas Ketenagakerjaan":

    # Ambil hanya kolom tahun
    tahun_cols = [col for col in df.columns if col.isdigit()]

    # ===============================
    # Tabel Total Keseluruhan & Pencari Kerja Per Tahun
    # ===============================
    df_laki = df[df["Uraian"].str.contains("Laki", case=False)].copy()
    df_perempuan = df[df["Uraian"].str.contains("Perempuan", case=False)].copy()

    total_laki = df_laki[tahun_cols].astype(int).sum()
    total_perempuan = df_perempuan[tahun_cols].astype(int).sum()
    total_keseluruhan = total_laki + total_perempuan

    tabel_per_tahun = pd.DataFrame({
        "Tahun": tahun_cols,
        "Total Laki-laki": total_laki.values,
        "Total Perempuan": total_perempuan.values,
        "Total Keseluruhan": total_keseluruhan.values
    })

    st.subheader("Jumlah Pencari Kerja Per Tahun")
    st.dataframe(tabel_per_tahun)

    # ===============================
    # Diagram Jumlah Pencari Kerja Laki-laki dan Perempuan
    # ===============================
    df_total = pd.DataFrame({
        "Tahun": tahun_cols,
        "Laki-laki": total_laki.values,
        "Perempuan": total_perempuan.values
    })

    df_long = df_total.melt(id_vars="Tahun", var_name="Jenis Kelamin", value_name="Jumlah")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_long, x="Tahun", y="Jumlah", hue="Jenis Kelamin", ax=ax,
                palette={"Laki-laki": "#A2C8EC", "Perempuan": "#F7B6C2"})
    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f', label_type='edge')
    ax.set_title("Jumlah Pencari Kerja per Jenis Kelamin")
    st.pyplot(fig)

    # ===============================
    # Diagram Total Pencari Kerja Tiap Tahun
    # ===============================
    fig, ax = plt.subplots()
    ax.plot(tahun_cols, total_keseluruhan.values, marker='o', linestyle='-', color='green')
    for i, val in enumerate(total_keseluruhan.values):
        ax.text(i, val + 10, f"{int(val):,}", ha='center')
    ax.set_xlabel("Tahun")
    ax.set_ylabel("Jumlah")
    ax.set_title("Total Pencari Kerja Tiap Tahun")
    st.pyplot(fig)

    
    # ===============================
    # Tabel Jumlah Pencari Kerja Berdasarkan Pendidikan
    # ===============================
    df_pendidikan = df[df['Uraian'].str.contains('Tamatan', case=False)].copy()
    df_pendidikan[tahun_cols] = df_pendidikan[tahun_cols].apply(pd.to_numeric, errors='coerce')
    df_pendidikan['Total'] = df_pendidikan[tahun_cols].sum(axis=1)
    df_pendidikan.set_index('Uraian', inplace=True)

    st.subheader("Jumlah Pencari Kerja Berdasarkan Pendidikan per Tahun")
    st.dataframe(df_pendidikan[tahun_cols + ['Total']])

    # ===============================
    # Diagram Pie Distribusi Pendidikan Tahun 2024
    # ===============================
    data_2024 = df_pendidikan['2024']
    data_2024 = data_2024[data_2024 > 0]
    short_labels = [label.replace("Tamatan ", "") for label in data_2024.index]
    colors = sns.color_palette("pastel")[0:len(data_2024)]

    fig, ax = plt.subplots(figsize=(10, 8))
    patches, texts, autotexts = ax.pie(
        data_2024.values,
        labels=short_labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        textprops={'fontsize': 11}
    )
    for autotext in autotexts:
        autotext.set_color('black')
    ax.set_title("Tamatan Pendidikan Pencari Kerja Tahun 2024", fontsize=15)
    st.pyplot(fig)

    # ===============================
    # Tabel Jumlah Tenaga Kerja di Luar Negeri
    # ===============================
    df_ln = df[df["Uraian"].str.contains("Tenaga Kerja di Luar Negeri", case=False)].copy()
    df_ln[tahun_cols] = df_ln[tahun_cols].apply(pd.to_numeric, errors='coerce')
    total_ln_pertahun = df_ln[tahun_cols].sum()

    tabel_ln = pd.DataFrame({
        "Tahun": tahun_cols,
        "Jumlah": total_ln_pertahun.values
    })
    tabel_ln.loc[len(tabel_ln)] = ["Total", total_ln_pertahun.sum()]

    st.subheader("Jumlah Tenaga Kerja Dari Kota Lubuk Linggau di Luar Negeri")
    st.dataframe(tabel_ln)

    # ===============================
    # Diagram Jumlah TKI di Luar Negeri
    # ===============================
    fig, ax = plt.subplots()
    sns.barplot(data=tabel_ln[:-1], x='Tahun', y='Jumlah', palette='crest', ax=ax)
    for p in ax.patches:
        ax.annotate(f"{int(p.get_height()):,}",
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom')
    ax.set_ylabel("Jumlah Tenaga Kerja")
    ax.set_title("Jumlah TKI dari Lubuk Linggau")
    st.pyplot(fig)


# -----------------------------
# DINPER
# -----------------------------
elif selected_opd == "Dinas Pertanian":
    lahan = df[df['Uraian'].str.contains("Lahan", case=False)].copy()
    st.subheader("Luas Lahan Pertanian per Jenis Tahun 2023")
    fig, ax = plt.subplots()
    plot = sns.barplot(data=lahan, y='Uraian', x='2023', palette='Set2', ax=ax)

    # Tambahkan label sumbu X dan Y
    ax.set_xlabel("Tahun 2023")
    ax.set_ylabel("Jenis Lahan")

    # Tambahkan anotasi di batang
    for p in plot.patches:
        ax.annotate(f"{p.get_width():,.0f}",
                    (p.get_width(), p.get_y() + p.get_height() / 2),
                    ha='left', va='center', xytext=(5, 0), textcoords='offset points')
    
    st.pyplot(fig)
    
    buah = df[df['Uraian'].str.contains("Buah", case=False)].copy()
    st.subheader("Jumlah Produksi Buah per Kecamatan")
    st.dataframe(buah)

    sayur = df[df['Uraian'].str.contains("Sayur", case=False)].copy()
    st.subheader("Jumlah Produksi Sayur per Kecamatan")
    st.dataframe(sayur)

    nabati = df[df['Uraian'].str.contains("Obat Nabati", case=False)].copy()
    st.subheader("Tabel Jumlah Produksi Obat Nabati per Kecamatan")
    st.dataframe(nabati)

    st.subheader("Jumlah Produksi Komoditas Pertanian Tahun 2023")
    fig, ax = plt.subplots()
    plot = sns.barplot(data=buah, y='Uraian', x='2023', palette='flare', ax=ax)
    for p in plot.patches:
        ax.annotate(f"{p.get_width():,.0f}",
                    (p.get_width(), p.get_y() + p.get_height() / 2),
                    ha='left', va='center', xytext=(5, 0), textcoords='offset points')
    st.pyplot(fig)

    ayam = df[df['Uraian'].str.contains("Ayam", case=False)].copy()
    st.subheader("Tabel Jumlah Populasi Ternak Ayam per Kecamatan")
    st.dataframe(ayam)

    st.subheader("Jumlah Populasi Ternak Ayam per Kecamatan (2023)")
    fig, ax = plt.subplots()
    plot = sns.barplot(data=ayam, y='Uraian', x='2023', palette='rocket', ax=ax)
    for p in plot.patches:
        ax.annotate(f"{p.get_width():,.0f}",
                    (p.get_width(), p.get_y() + p.get_height() / 2),
                    ha='left', va='center', xytext=(5, 0), textcoords='offset points')
    st.pyplot(fig)


    itik = df[df['Uraian'].str.contains("Itik", case=False)].copy()
    st.subheader("Tabel Jumlah Populasi Ternak Itik per Kecamatan")
    st.dataframe(itik)
    
    st.subheader("Diagram Jumlah Populasi Ternak Itik per Kecamatan")
    fig, ax = plt.subplots()
    plot = sns.barplot(data=itik, y='Uraian', x='2023', palette='ch:s=.25,rot=-.25', ax=ax)
    for p in plot.patches:
        ax.annotate(f"{p.get_width():,.0f}",
                    (p.get_width(), p.get_y() + p.get_height() / 2),
                    ha='left', va='center', xytext=(5, 0), textcoords='offset points')
    st.pyplot(fig)
