import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ========== KONFIGURASI HALAMAN ==========
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# ========== LOAD DATA ==========
@st.cache_data
def load_data():
    df = pd.read_csv('main_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# ========== SIDEBAR FILTER ==========
st.sidebar.header("🔍 Filter Data")

# Filter Tahun
tahun_options = sorted(df['year'].unique())
selected_tahun = st.sidebar.selectbox("Pilih Tahun", tahun_options)

# Filter Musim (multi-select)
musim_options = df['season'].unique().tolist()
selected_musim = st.sidebar.multiselect("Pilih Musim", musim_options, default=musim_options)

# Filter data
filtered_df = df[(df['year'] == selected_tahun) & (df['season'].isin(selected_musim))]

# ========== HEADER ==========
st.title("🚲 Bike Sharing Dashboard")
st.markdown("---")

# ========== METRICS ==========
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_hari = len(filtered_df)
    st.metric("📅 Total Hari", f"{total_hari} hari")

with col2:
    total_penyewaan = filtered_df['total_rentals'].sum()
    st.metric("🚲 Total Penyewaan", f"{total_penyewaan:,}")

with col3:
    rata_rata = filtered_df['total_rentals'].mean()
    st.metric("📈 Rata-rata per Hari", f"{rata_rata:.0f}")

with col4:
    ratio = filtered_df['registered'].mean() / filtered_df['casual'].mean()
    st.metric("👥 Registered : Casual", f"{ratio:.1f} : 1")

st.markdown("---")

# ========== PERTANYAAN 1 ==========
st.header("📌 Pertanyaan 1: Pengaruh Kondisi Cuaca terhadap Penyewaan")

col1, col2 = st.columns(2)

with col1:
    # Barplot rata-rata penyewaan per kondisi cuaca
    fig, ax = plt.subplots(figsize=(8, 5))
    
    weather_order = ['Clear/Few clouds', 'Mist/Cloudy', 'Light Rain/Snow']
    weather_means = []
    for w in weather_order:
        if w in filtered_df['weather_condition'].values:
            mean_val = filtered_df[filtered_df['weather_condition'] == w]['total_rentals'].mean()
            weather_means.append(mean_val)
    
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    bars = ax.bar(weather_order[:len(weather_means)], weather_means, 
                  color=colors[:len(weather_means)], edgecolor='black', linewidth=1.5)
    
    ax.set_title('Rata-rata Penyewaan per Kondisi Cuaca', fontsize=14, fontweight='bold')
    ax.set_xlabel('Kondisi Cuaca', fontsize=12)
    ax.set_ylabel('Rata-rata Penyewaan per Hari', fontsize=12)
    
    for bar, val in zip(bars, weather_means):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
                f'{val:.0f}', ha='center', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # Boxplot distribusi penyewaan per kondisi cuaca
    fig, ax = plt.subplots(figsize=(8, 5))
    
    sns.boxplot(data=filtered_df, x='weather_condition', y='total_rentals',
                order=weather_order, hue='weather_condition', 
                palette=colors, legend=False, ax=ax)
    
    ax.set_title('Distribusi Penyewaan per Kondisi Cuaca', fontsize=14, fontweight='bold')
    ax.set_xlabel('Kondisi Cuaca', fontsize=12)
    ax.set_ylabel('Total Penyewaan per Hari', fontsize=12)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# Insight Pertanyaan 1
with st.expander("📝 Lihat Insight Pertanyaan 1"):
    st.write("""
    - **Cuaca cerah** memiliki rata-rata penyewaan tertinggi yaitu **4.877 sepeda per hari**
    - **Cuaca berawan** berada di posisi menengah dengan **4.036 sepeda per hari**
    - **Cuaca hujan** memiliki rata-rata penyewaan terendah hanya **1.803 sepeda per hari**
    - Terjadi penurunan drastis sebesar **63%** saat hujan dibandingkan cuaca cerah
    - Cuaca buruk menjadi **batasan keras (hard constraint)** untuk bersepeda
    """)

st.markdown("---")

# ========== PERTANYAAN 2 ==========
st.header("📌 Pertanyaan 2: Pola Penyewaan berdasarkan Musim dan Tipe Pengguna")

col1, col2 = st.columns(2)

with col1:
    # Barplot rata-rata penyewaan per musim
    fig, ax = plt.subplots(figsize=(8, 5))
    
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    season_means = [filtered_df[filtered_df['season'] == s]['total_rentals'].mean() for s in season_order]
    season_colors = ['#2ecc71', '#f1c40f', '#e67e22', '#3498db']
    
    bars = ax.bar(season_order, season_means, color=season_colors, edgecolor='black', linewidth=1.5)
    
    ax.set_title('Rata-rata Penyewaan per Musim', fontsize=14, fontweight='bold')
    ax.set_xlabel('Musim', fontsize=12)
    ax.set_ylabel('Rata-rata Penyewaan per Hari', fontsize=12)
    
    for bar, val in zip(bars, season_means):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
                f'{val:.0f}', ha='center', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    # Grouped barplot casual vs registered per musim
    fig, ax = plt.subplots(figsize=(8, 5))
    
    season_user = filtered_df.groupby('season')[['casual', 'registered']].mean().reset_index()
    season_user_melted = season_user.melt(id_vars='season', value_vars=['casual', 'registered'],
                                           var_name='user_type', value_name='avg_rentals')
    
    sns.barplot(data=season_user_melted, x='season', y='avg_rentals', hue='user_type',
                order=season_order, palette={'casual': '#2ecc71', 'registered': '#3498db'}, ax=ax)
    
    ax.set_title('Perbandingan Casual vs Registered per Musim', fontsize=14, fontweight='bold')
    ax.set_xlabel('Musim', fontsize=12)
    ax.set_ylabel('Rata-rata Penyewaan per Hari', fontsize=12)
    ax.legend(title='Tipe Pengguna')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# Tren Bulanan
fig, ax = plt.subplots(figsize=(12, 5))

monthly_data = filtered_df.groupby('month').agg({
    'total_rentals': 'mean',
    'casual': 'mean',
    'registered': 'mean'
}).reset_index()

ax.plot(monthly_data['month'], monthly_data['casual'], 
        marker='o', linewidth=2, markersize=8, label='Casual', color='#2ecc71')
ax.plot(monthly_data['month'], monthly_data['registered'], 
        marker='s', linewidth=2, markersize=8, label='Registered', color='#3498db')
ax.plot(monthly_data['month'], monthly_data['total_rentals'], 
        marker='^', linewidth=2.5, markersize=9, label='Total', color='#e74c3c')

ax.set_title('Tren Penyewaan Sepeda per Bulan (Casual vs Registered)', fontsize=14, fontweight='bold')
ax.set_xlabel('Bulan', fontsize=12)
ax.set_ylabel('Rata-rata Penyewaan per Hari', fontsize=12)
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 
                    'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des'])
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, linestyle='--')

# Menandai titik puncak
max_month = monthly_data.loc[monthly_data['total_rentals'].idxmax(), 'month']
max_value = monthly_data['total_rentals'].max()
ax.annotate(f'Puncak: {max_value:.0f}', xy=(max_month, max_value), 
            xytext=(max_month+0.5, max_value-500),
            arrowprops=dict(arrowstyle='->', color='red'), fontsize=10, fontweight='bold')

plt.tight_layout()
st.pyplot(fig)
plt.close()

# Insight Pertanyaan 2
with st.expander("📝 Lihat Insight Pertanyaan 2"):
    st.write("""
    - **Musim gugur (Fall)** memiliki rata-rata penyewaan tertinggi: **5.644 sepeda per hari**
    - **Musim semi (Spring)** memiliki rata-rata penyewaan terendah: **2.636 sepeda per hari**
    - **Pengguna registered** mendominasi di semua musim (81% dari total penyewaan)
    - **Puncak penyewaan** terjadi pada bulan **September** dengan lebih dari 7.700 sepeda per hari
    - Pengguna registered lebih **stabil** sepanjang tahun, pengguna casual lebih **volatil**
    """)

st.markdown("---")

# ========== KESIMPULAN & REKOMENDASI ==========
st.header("📝 Kesimpulan & Rekomendasi")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Kesimpulan")
    st.write("""
    **Pertanyaan 1 - Pengaruh Cuaca:**
    - Cuaca cerah: 4.877 sepeda/hari (tertinggi)
    - Cuaca hujan: 1.803 sepeda/hari (terendah)
    - Penurunan 63% saat hujan
    - Suhu berkorelasi positif (0,63) dengan penyewaan

    **Pertanyaan 2 - Pola Musim & Tipe Pengguna:**
    - Musim gugur: 5.644 sepeda/hari (tertinggi)
    - Musim semi: 2.636 sepeda/hari (terendah)
    - Registered mendominasi (81%)
    - Puncak di bulan September (7.700+)
    """)

with col2:
    st.subheader("Rekomendasi")
    st.write("""
    1. **Tingkatkan ketersediaan sepeda** saat cuaca cerah dan musim panas/gugur
    2. **Berikan diskon** di musim dingin untuk menjaga loyalitas registered
    3. **Targetkan promosi casual** di akhir pekan dan musim panas
    4. **Pasang perlengkapan anti-hujan** (jas hujan, penutup sepeda) di musim hujan
    5. **Fokus akuisisi registered** karena mereka lebih stabil dan menguntungkan
    """)

st.markdown("---")
st.caption("Dashboard by Hasanul Fikri | Bike Sharing Dataset 2011-2012")