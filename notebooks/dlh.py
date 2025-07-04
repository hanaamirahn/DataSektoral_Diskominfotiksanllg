# -*- coding: utf-8 -*-
"""DLH.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HJAslbbWkDT6_NPgfjzB4_KxadL_mbGK
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""# **Data Wragling**

**Gathering Data**
"""

dlh_df = pd.read_csv("/content/DLH.csv")
print(dlh_df.shape)
print(dlh_df)

"""**Assessing Data**"""

# Menampilkan informasi pada dataset
dlh_df.info()

# Memeriksa missing value
dlh_df.isna().sum()

# Memeriksa duplikasi data
print("Jumlah duplikasi: ", dlh_df.duplicated().sum())

"""**Cleaning Data**"""

# Menghapus kolom yang tidak diperlukan
dlh_df = dlh_df.drop(columns=["BIDANG"])
print(dlh_df)

# Mengubah semua nama kolom menjadi string
dlh_df.columns = dlh_df.columns.map(str)
print(dlh_df)

# Mengubah Tipe Data Menjadi Integer Kecuali Pada Satuan Persen
# Ubah nilai ke string, hapus karakter aneh, lalu ubah ke float dulu
dlh_df['NILAI 2024 SEMESTER I'] = dlh_df['NILAI 2024 SEMESTER I'].astype(str).str.replace(r'[^\d\.]', '', regex=True)

# Buat masker: indeks yang BUKAN 8-19
mask = ~dlh_df.index.isin(range(8, 20))

# Ubah hanya yang di luar indeks 8-19 ke integer
dlh_df.loc[mask, 'NILAI 2024 SEMESTER I'] = pd.to_numeric(
    dlh_df.loc[mask, 'NILAI 2024 SEMESTER I'], errors='coerce'
).fillna(0).astype(int)

dlh_df.info()
print(dlh_df)

# Save data clean
dlh_df.to_csv('dlh_clean.csv', index=False)

"""# **Exploratory Data Analysis (EDA)**"""

# Statistik deskriptif numerik
dlh_df.describe()

# Cek distribusi tiap kolom kategorikal
for col in dlh_df.select_dtypes(include='object').columns:
    print(f"\nDistribusi kategori pada kolom {col}:")
    print(dlh_df[col].value_counts())

# Melihat Volume Air Limbah
# Filter hanya baris yang mengandung data Volume Air Limbah
limbah_mask = dlh_df['NAMA'].str.contains("Volume Air Limbah", case=False)
limbah_data = dlh_df[limbah_mask][['NAMA', 'NILAI 2024 SEMESTER I']].copy()

# Ekstrak nama kecamatan
limbah_data['Kecamatan'] = limbah_data['NAMA'].str.replace('Volume Air Limbah Kecamatan ', '', regex=False)

# Buat tabel volume limbah per kecamatan
limbah_table = limbah_data[['Kecamatan', 'NILAI 2024 SEMESTER I']].rename(columns={
    'NILAI 2024 SEMESTER I': 'Volume Limbah (Liter)'
})

# Tambahkan total di baris akhir
total_row = pd.DataFrame({
    'Kecamatan': ['Total'],
    'Volume Limbah (Liter)': [limbah_table['Volume Limbah (Liter)'].sum()]
})

# Gabungkan tabel dengan total
limbah_table = pd.concat([limbah_table, total_row], ignore_index=True)

# Cetak tabel
print("Volume Air Limbah Di Kota Lubuklinggau Tahun 2024:")
print(limbah_table)

# Melihat Komposisi Sampah
# Filter baris komposisi sampah
komposisi_mask = dlh_df['NAMA'].str.contains("Komposisi Sampah", case=False)
komposisi_data = dlh_df[komposisi_mask][['NAMA', 'NILAI 2024 SEMESTER I']].copy()

# Pastikan nilainya dalam bentuk float
komposisi_data['NILAI 2024 SEMESTER I'] = pd.to_numeric(komposisi_data['NILAI 2024 SEMESTER I'], errors='coerce')

# Ekstrak jenis sampah
komposisi_data['Jenis Sampah'] = komposisi_data['NAMA'].str.replace('Komposisi Sampah ', '', regex=False)

# Buat tabel
komposisi_table = komposisi_data[['Jenis Sampah', 'NILAI 2024 SEMESTER I']].rename(columns={
    'NILAI 2024 SEMESTER I': 'Persentase (%)'
})

# Tambahkan total baris (tanpa pembulatan)
total_row = pd.DataFrame({
    'Jenis Sampah': ['Total'],
    'Persentase (%)': [komposisi_table['Persentase (%)'].sum()]
})

# Gabungkan
komposisi_table = pd.concat([komposisi_table, total_row], ignore_index=True)

# Tampilkan tabel
print("Komposisi Sampah Kota Lubuk Linggau Tahun 2024:")
print(komposisi_table.to_string(index=False))

# Melihat Jumlah Alat Angkut Sampah
# Melihat Jumlah Alat Angkut Sampah
alat_mask = dlh_df['NAMA'].str.contains("Jumlah", case=False)
alat_data = dlh_df[alat_mask][['NAMA', 'NILAI 2024 SEMESTER I']].copy()

# Pastikan nilainya numerik
alat_data['NILAI 2024 SEMESTER I'] = pd.to_numeric(alat_data['NILAI 2024 SEMESTER I'], errors='coerce')

# Ekstrak nama alat angkut
alat_data['Jenis Alat Angkut'] = alat_data['NAMA'].str.replace('Jumlah Alat Angkut Sampah ', '', regex=False)

# Hapus kata 'Jumlah ' jika masih ada
alat_data['Jenis Alat Angkut'] = alat_data['Jenis Alat Angkut'].str.replace('Jumlah ', '', regex=False)

# Buat tabel akhir
alat_table = alat_data[['Jenis Alat Angkut', 'NILAI 2024 SEMESTER I']].rename(columns={
    'NILAI 2024 SEMESTER I': 'Jumlah'
})

# Tambahkan total
total_row = pd.DataFrame({
    'Jenis Alat Angkut': ['Total'],
    'Jumlah': [alat_table['Jumlah'].sum()]
})

# Gabungkan tabel
alat_table = pd.concat([alat_table, total_row], ignore_index=True)

# Tampilkan tabel
print("Jumlah Alat Angkut Sampah Kota Lubuklinggau Tahun 2024:")
print(alat_table.to_string(index=False))

"""# **Visualization & Explanatory Analysis**"""

# Volume Limbah Air
# Hapus baris total agar tidak divisualisasikan
limbah_plot = limbah_table[limbah_table['Kecamatan'] != 'Total'].copy()

# Sort nilai dari tinggi ke rendah
limbah_plot = limbah_plot.sort_values('Volume Limbah (Liter)', ascending=False).reset_index(drop=True)

# Buat warna gradasi dari palette
colors = sns.color_palette("Spectral", len(limbah_plot))

# Buat plot
plt.figure(figsize=(12, 7))
bars = plt.bar(
    limbah_plot['Kecamatan'],
    limbah_plot['Volume Limbah (Liter)'],
    color=colors,
    edgecolor='black',
    width=0.6
)

# Tambahkan label nilai di atas bar
for i, value in enumerate(limbah_plot['Volume Limbah (Liter)']):
    plt.text(i, value + value * 0.01, f"{value:,.0f} L", ha='center', fontsize=9)

# Gaya visualisasi
plt.title("Volume Air Limbah per Kecamatan\nKota Lubuk Linggau Tahun 2024", fontsize=16, weight='bold')
plt.xlabel("Kecamatan", fontsize=12)
plt.ylabel("Volume Limbah (Liter)", fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# Komposisi Sampah
# Filter baris komposisi sampah
komposisi_mask = dlh_df['NAMA'].str.contains("Komposisi Sampah", case=False)
komposisi_data = dlh_df[komposisi_mask][['NAMA', 'NILAI 2024 SEMESTER I']].copy()

# Ambil jenis sampah dan nilai persentase
komposisi_data['Jenis Sampah'] = komposisi_data['NAMA'].str.replace("Komposisi Sampah ", "", regex=False)
komposisi_data['Persentase'] = pd.to_numeric(komposisi_data['NILAI 2024 SEMESTER I'], errors='coerce')

# Warna cerah kreatif
colors = sns.color_palette("Set3", len(komposisi_data))

# Plot pie chart
plt.figure(figsize=(8, 8))
patches, texts, autotexts = plt.pie(
    komposisi_data['Persentase'],
    labels=komposisi_data['Jenis Sampah'],
    autopct='%.2f%%',
    startangle=140,
    colors=colors,
    wedgeprops={'edgecolor': 'black'}
)

# Format teks
for text in texts:
    text.set_fontsize(9)
for autotext in autotexts:
    autotext.set_fontsize(9)

plt.title("Komposisi Sampah Kota Lubuk Linggau Tahun 2024", fontsize=14, weight='bold')
plt.tight_layout()
plt.show()

# Alat Pengangkut Sampah
# Hapus baris total untuk visualisasi
alat_plot = alat_table[alat_table['Jenis Alat Angkut'] != 'Total'].copy()
alat_plot = alat_plot.sort_values('Jumlah', ascending=True).reset_index(drop=True)

# Warna kreatif
colors = sns.color_palette("Dark2", len(alat_plot))

# Plot horizontal bar
plt.figure(figsize=(10, 6))
bars = plt.barh(alat_plot['Jenis Alat Angkut'], alat_plot['Jumlah'], color=colors, edgecolor='black')

# Tambahkan label angka
for i, value in enumerate(alat_plot['Jumlah']):
    plt.text(value + 0.3, i, f"{int(value)} unit", va='center', fontsize=9)

plt.title("Jumlah Alat Angkut Sampah\nKota Lubuk Linggau Tahun 2024", fontsize=14, weight='bold')
plt.xlabel("Jumlah Alat (unit)")
plt.ylabel("Jenis Alat Angkut")
plt.grid(axis='x', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.show()