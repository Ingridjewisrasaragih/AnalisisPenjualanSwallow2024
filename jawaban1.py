import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk membuat data bulanan
def generate_monthly_data(year, month):
    sandal_types = ['Swallow A', 'Swallow B', 'Swallow C']
    harga_per_unit = {'Swallow A': 100, 'Swallow B': 120, 'Swallow C': 150}
    biaya_per_unit = {'Swallow A': 60, 'Swallow B': 70, 'Swallow C': 80}
    
    # Menghasilkan tanggal untuk bulan tertentu
    dates = pd.date_range(start=f'{year}-{month:02d}-01', periods=1, freq='M')
    data = []
    
    for sandal in sandal_types:
        produksi = np.random.randint(100, 500)  # Produksi bulanan
        persediaan = np.random.randint(1000, 5000)  # Persediaan bulanan
        promosi = np.random.randint(50, 200)  # Promosi bulanan
        penjualan = produksi + np.random.randint(10, 100)  # Penjualan bulanan
        
        # Hitung laba
        laba = (penjualan * harga_per_unit[sandal]) - (produksi * biaya_per_unit[sandal])
        
        data.append({
            'bulan': dates[0],
            'jenis_sandal': sandal,
            'produksi': produksi,
            'persediaan': persediaan,
            'promosi': promosi,
            'penjualan': penjualan,
            'laba': laba
        })
    
    return pd.DataFrame(data)

# Menghasilkan data untuk semua bulan di tahun 2024
df_list = [generate_monthly_data(2024, month) for month in range(1, 13)]
df_all = pd.concat(df_list)

# 1. Produksi dan Penjualan
# Menghitung total produksi dan penjualan per jenis sandal
total_produksi = df_all.groupby('jenis_sandal')['produksi'].sum()
total_penjualan = df_all.groupby('jenis_sandal')['penjualan'].sum()

# 2. Persediaan dan Manajemen Stok
# Menghitung persediaan akhir per jenis sandal
persediaan_akhir = df_all.groupby('jenis_sandal')['persediaan'].sum()

# 3. Efektivitas Promosi
# Menghitung total promosi per jenis sandal
total_promosi = df_all.groupby('jenis_sandal')['promosi'].sum()

# 4. Analisis Keuangan
# Menghitung laba per bulan
laba_per_bulan = df_all.groupby(df_all['bulan'].dt.to_period('M'))['laba'].sum()

# 5. Kinerja Tahunan
# Menghitung total laba tahunan
total_laba_tahunan = df_all['laba'].sum()

# 6. Visualisasi

# Bar Chart: Produksi, Persediaan, dan Penjualan
plt.figure(figsize=(14, 7))
df_june_grouped = df_all[df_all['bulan'].dt.month == 6].groupby('bulan').sum()
colors = ['#4CAF50', '#FF9800', '#2196F3']
bar_width = 0.25
index = np.arange(len(df_june_grouped))

plt.bar(index, df_june_grouped['produksi'], width=bar_width, label='Produksi', color=colors[0], align='center')
plt.bar(index + bar_width, df_june_grouped['persediaan'], width=bar_width, label='Persediaan', color=colors[1], align='center')
plt.bar(index + 2 * bar_width, df_june_grouped['penjualan'], width=bar_width, label='Penjualan', color=colors[2], align='center')

plt.title('Produksi, Persediaan, dan Penjualan Sendal Swallow - Juni 2024', fontsize=16)
plt.xlabel('Bulan', fontsize=14)
plt.ylabel('Jumlah', fontsize=14)
plt.xticks(index + bar_width / 2, df_june_grouped.index.strftime('%Y-%m'), rotation=45, fontsize=12)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Histogram: Distribusi Produksi, Persediaan, Promosi, dan Penjualan
plt.figure(figsize=(18, 16))
for i, sandal in enumerate(['Swallow A', 'Swallow B', 'Swallow C'], 1):
    df_sandal = df_all[df_all['jenis_sandal'] == sandal]
    
    plt.subplot(3, 4, i*4-3)
    sns.histplot(df_sandal['produksi'], kde=True, color='blue')
    plt.title(f'Distribusi Produksi {sandal}', fontsize=14)
    plt.xlabel('Jumlah Produksi', fontsize=12)
    plt.ylabel('Frekuensi', fontsize=12)
    
    plt.subplot(3, 4, i*4-2)
    sns.histplot(df_sandal['persediaan'], kde=True, color='green')
    plt.title(f'Distribusi Persediaan {sandal}', fontsize=14)
    plt.xlabel('Jumlah Persediaan', fontsize=12)
    plt.ylabel('Frekuensi', fontsize=12)
    
    plt.subplot(3, 4, i*4-1)
    sns.histplot(df_sandal['promosi'], kde=True, color='purple')
    plt.title(f'Distribusi Promosi {sandal}', fontsize=14)
    plt.xlabel('Jumlah Promosi', fontsize=12)
    plt.ylabel('Frekuensi', fontsize=12)
    
    plt.subplot(3, 4, i*4)
    sns.histplot(df_sandal['penjualan'], kde=True, color='red')
    plt.title(f'Distribusi Penjualan {sandal}', fontsize=14)
    plt.xlabel('Jumlah Penjualan', fontsize=12)
    plt.ylabel('Frekuensi', fontsize=12)

plt.tight_layout()
plt.show()

# Pie Chart: Total Produksi, Persediaan, Promosi, dan Penjualan
plt.figure(figsize=(10, 10))
sizes = [total_produksi.sum(), persediaan_akhir.sum(), total_promosi.sum(), total_penjualan.sum()]
labels = ['Produksi', 'Persediaan', 'Promosi', 'Penjualan']
colors = ['#FF5733', '#33FF57', '#3357FF', '#F1C40F']

plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, wedgeprops={'edgecolor': 'black'})
plt.title('Distribusi Total Produksi, Persediaan, Promosi, dan Penjualan Sendal Swallow - 2024', fontsize=16)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
