# Proyek Analisis Data: Bike Sharing Dataset
## Ringkasan Proyek

Proyek ini menganalisis faktor yang mempengaruhi penyewaan sepeda menggunakan dataset Bike Sharing (2011-2012). Dua pertanyaan bisnis yang dijawab:
1. Pengaruh kondisi cuaca terhadap jumlah penyewaan
2. Pola penyewaan berdasarkan musim dan tipe pengguna (casual vs registered)

Hasil analisis ditampilkan dalam dashboard interaktif menggunakan Streamlit.

## Struktur Folder
```bash
submission/
├── dashboard/
│ ├── dashboard.py # File utama dashboard
│ └── main_data.csv # Data hasil cleaning
├── data/
│ ├── day.csv # Dataset mentah
│ └── Notebook.ipynb # Notebook analisis
├── requirements.txt # Daftar library
├── runtime.txt # Versi Python
└── README.md # Dokumentasi
```

### Langkah-langkah Menjalankan Proyek di VS Code

1. Download dan Buka folder proyek di VS Code.
2. Buka terminal VS Code melalui menu **Terminal > New Terminal**.
3. Jalankan instalasi dependency:
```bash
pip install -r requirements.txt
```
4. Jalankan dashboard dengan:
```bash
cd dashboard
streamlit run dashboard.py
```
