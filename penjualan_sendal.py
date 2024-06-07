import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk membuat data bulanan
def generate_monthly_data(year, month):
    dates = pd.date_range(start=f'{year}-{month:02d}-01', end=f'{year}-{month:02d}-{pd.Timestamp(f"{year}-{month:02d}").days_in_month}', freq='D')
    data = []
    
    for sandal in sandal_types:
        produksi_data = np.random.randint(50, 200, size=len(dates))
        persediaan_data = np.random.randint(1000, 3000, size=len(dates))
        promosi_data = np.random.randint(10, 50, size=len(dates))
        penjualan_data = produksi_data + np.random.randint(10, 50, size=len(dates))  # Penjualan lebih tinggi dari produksi
        
        for i in range(len(dates)):
            produksi = produksi_data[i]
            penjualan = penjualan_data[i]
            persediaan = persediaan_data[i] - penjualan  # Persediaan berkurang dengan penjualan
            
            # Hitung laba
            laba = (penjualan * harga_per_unit[sandal]) - (produksi * biaya_per_unit[sandal])
            
            data.append({
                'tanggal': dates[i],
                'jenis_sandal': sandal,
                'produksi': produksi,
                'persediaan': persediaan,
                'promosi': promosi_data[i],
                'penjualan': penjualan,
                'laba': laba
            })
    
    return pd.DataFrame(data)

# Jenis sandal
sandal_types = ['Swallow A', 'Swallow B', 'Swallow C']

# Harga dan biaya produksi per unit untuk masing-masing jenis sandal
harga_per_unit = {'Swallow A': 100, 'Swallow B': 120, 'Swallow C': 150}
biaya_per_unit = {'Swallow A': 60, 'Swallow B': 70, 'Swallow C': 80}

# Membuat data untuk semua bulan di tahun 2024
df_list = [generate_monthly_data(2024, month) for month in range(1, 13)]

# Menggabungkan data bulanan menjadi satu DataFrame
df_all = pd.concat(df_list)

# Menampilkan data
print(df_all.head())

# Visualisasi dengan diagram batang (bar chart) untuk Juni
plt.figure(figsize=(14, 7))

df_june_grouped = df_list[5].groupby('tanggal').sum()

# Diagram batang untuk produksi, persediaan, dan penjualan
plt.bar(df_june_grouped.index, df_june_grouped['produksi'], width=0.2, label='Produksi', align='center')
plt.bar(df_june_grouped.index + pd.Timedelta(days=0.2), df_june_grouped['persediaan'], width=0.2, label='Persediaan', align='center')
plt.bar(df_june_grouped.index + pd.Timedelta(days=0.4), df_june_grouped['penjualan'], width=0.2, label='Penjualan', align='center')

plt.title('Produksi, Persediaan, dan Penjualan Sendal Swallow - Juni 2024')
plt.xlabel('Tanggal')
plt.ylabel('Jumlah')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Tampilkan grafik
plt.show()

# Visualisasi histogram untuk distribusi produksi, persediaan, promosi, dan penjualan per jenis sandal
plt.figure(figsize=(14, 14))

for i, sandal in enumerate(sandal_types, 1):
    df_sandal = df_list[5][df_list[5]['jenis_sandal'] == sandal]
    
    plt.subplot(3, 4, i*4-3)
    sns.histplot(df_sandal['produksi'], kde=True)
    plt.title(f'Distribusi Produksi {sandal}')
    
    plt.subplot(3, 4, i*4-2)
    sns.histplot(df_sandal['persediaan'], kde=True)
    plt.title(f'Distribusi Persediaan {sandal}')
    
    plt.subplot(3, 4, i*4-1)
    sns.histplot(df_sandal['promosi'], kde=True)
    plt.title(f'Distribusi Promosi {sandal}')
    
    plt.subplot(3, 4, i*4)
    sns.histplot(df_sandal['penjualan'], kde=True)
    plt.title(f'Distribusi Penjualan {sandal}')

plt.tight_layout()
plt.show()

# Visualisasi dengan diagram lingkaran (pie chart) untuk total produksi, persediaan, promosi, dan penjualan
plt.figure(figsize=(8, 8))

total_produksi = df_list[5]['produksi'].sum()
total_persediaan = df_list[5]['persediaan'].sum()
total_promosi = df_list[5]['promosi'].sum()
total_penjualan = df_list[5]['penjualan'].sum()

labels = ['Produksi', 'Persediaan', 'Promosi', 'Penjualan']
sizes = [total_produksi, total_persediaan, total_promosi, total_penjualan]
colors = ['blue', 'green', 'purple', 'red']

plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title('Distribusi Total Produksi, Persediaan, Promosi, dan Penjualan Sendal Swallow - Juni 2024')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Tampilkan grafik
plt.show()

# Visualisasi laba/rugi per bulan
df_all['bulan'] = df_all['tanggal'].dt.to_period('M')
laba_per_bulan = df_all.groupby('bulan')['laba'].sum()

plt.figure(figsize=(14, 7))
ax = laba_per_bulan.plot(kind='bar', color='orange')
plt.axhline(0, color='red', linewidth=1)
plt.title('Laba/Rugi per Bulan untuk Sendal Swallow - 2024')
plt.xlabel('Bulan')
plt.ylabel('Laba/Rugi')
plt.xticks(rotation=45)
plt.tight_layout()

# Tambahkan label pada batang
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}', (p.get_x() * 1.005, p.get_height() * 1.005))

# Tampilkan grafik
plt.show()

# Analisis Laba/Rugi Tahunan
total_laba_tahunan = df_all['laba'].sum()
print(f'Total Laba/Rugi Tahunan untuk Sendal Swallow - 2024: {total_laba_tahunan}')

if total_laba_tahunan > 0:
    print("Perusahaan mengalami keuntungan pada tahun 2024.")
else:
    print("Perusahaan mengalami kerugian pada tahun 2024.")
