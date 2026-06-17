import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import statsmodels.formula.api as smf
    import pandas as pd 
    import numpy as np 
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pingouin as pg

    return np, pd, pg, plt, sns


@app.cell
def _():
    f_jemaah = "Jumlah Jemaah Haji yang Diberangkatkan ke Tanah Suci Mekah Menurut Provinsi, 2018.csv"
    f_kemiskinan = "Persentase Penduduk Miskin (P0) Menurut Provinsi dan Daerah, 2018.csv"
    f_aps = "Angka Partisipasi Sekolah (APS) Menurut Provinsi dan Kelompok Umur, 2018.csv"
    f_fasilitas = "Jumlah Desa yang Memiliki Fasilitas Sekolah Menurut Provinsi dan Tingkat Pendidikan, 2018.csv"
    f_pidana = "Risiko Penduduk Terkena Tindak Pidana (Per 100.000 Penduduk) , 2018.csv"
    f_hamil = "Proporsi Perempuan Pernah Kawin 15-49 tahun yang Melahirkan Anak Lahir Hidup Yang Pertama Kali Berumur Kurang dari 20 tahun Menurut Kabupaten_Kota, 2018.csv"

    ks = ["", "-", "Unknown", "NA"]

    return f_aps, f_fasilitas, f_hamil, f_jemaah, f_kemiskinan, f_pidana, ks


@app.cell
def _(f_jemaah, pd):
    dt_jemaah = pd.read_csv(f_jemaah)
    dt_jemaah["Provinsi"] = dt_jemaah["Provinsi"].str.upper()[0:]
    dt_jemaah = dt_jemaah.dropna().head(-1).reset_index(drop=True)
    dt_jemaah
    return (dt_jemaah,)


@app.cell
def _(f_kemiskinan, ks, np, pd):
    dt_kemiskinan = pd.read_csv(f_kemiskinan)
    dt_kemiskinan = dt_kemiskinan[4:][["38 Provinsi", "Unnamed: 7", "Unnamed: 8"]]
    dt_kemiskinan = dt_kemiskinan.rename(columns={"38 Provinsi": "Provinsi", "Unnamed: 7": "Kemiskinan Semester 1", "Unnamed: 8": "Kemiskinan Semester 2"})

    dt_kemiskinan = dt_kemiskinan.replace(ks, np.nan).dropna().reset_index(drop=True)
    dt_kemiskinan["Kemiskinan Semester 1"] = dt_kemiskinan["Kemiskinan Semester 1"].astype(float)
    dt_kemiskinan["Kemiskinan Semester 2"] = dt_kemiskinan["Kemiskinan Semester 2"].astype(float)
    dt_kemiskinan
    return (dt_kemiskinan,)


@app.cell
def _(f_aps, ks, np, pd):
    dt_aps = pd.read_csv(f_aps)
    dt_aps = dt_aps.rename(columns={"38 Provinsi": "Provinsi", "Unnamed: 1": "APS 7-21", "Unnamed: 2": "APS 13-15", "Unnamed: 3": "APS 16-18"}).drop("Unnamed: 4", axis=1).replace(ks, np.nan).dropna().reset_index(drop=True)
    dt_aps[["APS 7-21", "APS 13-15", "APS 16-18"]] = dt_aps[["APS 7-21", "APS 13-15", "APS 16-18"]].astype(float) 
    dt_aps 
    return (dt_aps,)


@app.cell
def _(f_fasilitas, ks, np, pd):
    dt_fasilitas = pd.read_csv(f_fasilitas)
    dt_fasilitas = dt_fasilitas.rename(columns={"38 Provinsi": "Provinsi", "Unnamed: 1": "Fasilitas SD", "Unnamed: 2": "Fasilitas SMP", "Unnamed: 3": "Fasilitas SMU", "Unnamed: 4": "Fasilitas SMK"}).drop("Unnamed: 5", axis=1)[3:]
    dt_fasilitas = dt_fasilitas.replace(ks, np.nan).dropna().reset_index(drop=True)
    _kol = ["Fasilitas SD", "Fasilitas SMP", "Fasilitas SMU", "Fasilitas SMK"]
    dt_fasilitas[_kol] = dt_fasilitas[_kol].astype(float)
    dt_fasilitas
    return (dt_fasilitas,)


@app.cell
def _(f_pidana, pd):
    dt_pidana = pd.read_csv(f_pidana)
    dt_pidana = dt_pidana[2:].rename(columns={"Kepolisian Daerah": "Provinsi", "Unnamed: 1": "Pidana"})
    dt_pidana["Pidana"] = dt_pidana["Pidana"].astype(float)
    dt_pidana
    return (dt_pidana,)


@app.cell
def _(f_hamil, ks, np, pd):
    dt_hamil = pd.read_csv(f_hamil)
    dt_hamil = dt_hamil[2:].rename(columns={"Provinsi/Kabupaten/Kota/Indonesia": "Provinsi", "Unnamed: 1": "Hamil"}).replace(ks, np.nan).dropna().reset_index(drop=True)
    dt_hamil["Hamil"] = dt_hamil["Hamil"].astype(float)
    dt_hamil 
    return (dt_hamil,)


@app.cell
def _(dt_aps, dt_fasilitas, dt_hamil, dt_jemaah, dt_kemiskinan, dt_pidana):
    # Gabung datanya ok
    mhow = "inner"

    data = dt_hamil.merge(dt_aps, on="Provinsi", how=mhow) \
                    .merge(dt_fasilitas, on="Provinsi", how=mhow) \
                    .merge(dt_jemaah, on="Provinsi", how=mhow) \
                    .merge(dt_kemiskinan, on="Provinsi", how=mhow) \
                    .merge(dt_pidana, on="Provinsi", how=mhow)
    data
    return (data,)


@app.cell
def _(data, pg):
    # Uji Normalitas Univariat
    normal_uni = pg.normality(data)
    print(normal_uni)

    # Uji Normalitas Multivariat
    kolom_numerik = data.select_dtypes(include=['float64', 'int64']).columns
    normal_multi = pg.multivariate_normality(data[kolom_numerik])
    print(normal_multi)

    # Uji Homoskedastisitas
    uji_box_m = pg.box_m(data, dvs=kolom_numerik.tolist(), group='Provinsi')
    print(uji_box_m)
    return


@app.cell
def _(data, pg):
    # ini yg katanya paling op
    jawa_bali = ["JAWA BARAT", "JAWA TENGAH", "JAWA TIMUR", "DKI JAKARTA", "BANTEN", "BALI", "DI YOGYAKARTA"]

    # wilayah
    data['Wilayah'] = data['Provinsi'].apply(lambda x: 'Jawa & Bali' if x in jawa_bali else 'Luar Jawa & Bali')

    # Kruskall-wallis
    _sd = pg.kruskal(data=data, dv='Fasilitas SD', between='Wilayah')
    _smp = pg.kruskal(data=data, dv='Fasilitas SMP', between='Wilayah')
    _smu = pg.kruskal(data=data, dv='Fasilitas SMU', between='Wilayah')
    _smk = pg.kruskal(data=data, dv='Fasilitas SMK', between='Wilayah')
    print("Butuh pemerataan fasilitas SD di luar Jawa?", "Secara statistik,", "iya." if (_sd.p_unc.Kruskal < 0.05) else "tidak.")
    print("Butuh pemerataan fasilitas SMP di luar Jawa?", "Secara statistik,", "iya." if (_smp.p_unc.Kruskal < 0.05) else "tidak.")
    print("Butuh pemerataan fasilitas SMU di luar Jawa?", "Secara statistik,", "iya." if (_smu.p_unc.Kruskal < 0.05) else "tidak.")
    print("Butuh pemerataan fasilitas SMK di luar Jawa?", "Secara statistik,", "iya." if (_smk.p_unc.Kruskal < 0.05) else "tidak.")
    return


@app.cell
def _(data, plt, sns):
    # 1. Mengatur gaya dan tema yang elegan khas jurnal akademik
    sns.set_theme(style="whitegrid", context="paper")

    # 2. Menyiapkan kanvas (figure) dengan 4 kotak (2 baris x 2 kolom)
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))

    # Daftar kolom yang akan di-plot
    kolom_fasilitas = ['Fasilitas SD', 'Fasilitas SMP', 'Fasilitas SMU', 'Fasilitas SMK']
    judul_grafik = ['Fasilitas SD (Tidak Signifikan)', 'Fasilitas SMP (Tidak Signifikan)', 
                    'Fasilitas SMU (SIGNIFIKAN)', 'Fasilitas SMK (SIGNIFIKAN)']

    # 3. Melakukan plotting secara otomatis menggunakan perulangan (loop)
    for i, ax in enumerate(axes.flatten()):
        # Membuat boxplot
        sns.boxplot(
            data=data, 
            x='Wilayah', 
            y=kolom_fasilitas[i], 
            hue='Wilayah', # Memberikan warna berbeda antar wilayah
            palette=['#2ca02c', '#d62728'], # Hijau untuk Jawa/Bali, Merah untuk Luar
            ax=ax,
            width=0.5,
            linewidth=1.5
        )
    
        # 4. Mempercantik label dan judul setiap grafik kecil
        ax.set_title(judul_grafik[i], fontsize=12, fontweight='bold', pad=10)
        ax.set_xlabel('') # Menghilangkan tulisan "Wilayah" di sumbu X agar lebih bersih
        ax.set_ylabel('Jumlah Fasilitas', fontsize=10)


    # 5. Merapikan jarak antar grafik dan menambahkan Judul Utama
    plt.suptitle('Ketimpangan Fasilitas Pendidikan: Jawa & Bali vs Luar Jawa & Bali', 
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()

    # Tampilkan grafiknya!
    plt.show()
    return


if __name__ == "__main__":
    app.run()
