# DAX Measures — ISPA Indonesia 2026

## Catatan level (PENTING — baca dulu)

Proyek ini punya **dua seri yang tidak boleh dicampur**, dan kit ini menjaganya
dengan tabel fakta terpisah per seri dan per grain:

| Tabel fakta | Seri | Grain (1 baris =) | Untuk visual... |
|---|---|---|---|
| `fact_total_nasional` | SKDR | 1 baris ringkasan (total seluruh provinsi, s.d. minggu ke-38 2026) | KPI total nasional, penyebut pangsa provinsi |
| `fact_kasus_provinsi` | SKDR | 1 provinsi (HANYA 10 provinsi teratas) | Peringkat provinsi, pangsa, per kapita |
| `fact_kasus_mingguan` | SKDR | 1 periode laporan (rentang minggu yang dipublikasikan sumber) | Tren laporan mingguan |
| `fact_karhutla_series` | Karhutla | 1 tanggal snapshot (kumulatif) | Pertumbuhan kumulatif karhutla |
| `fact_karhutla_provinsi` | Karhutla | 1 provinsi / gabungan provinsi | Sebaran karhutla antarprovinsi |
| `fact_karhutla_usia` | Karhutla | 1 tanggal snapshot × 1 kelompok usia | Pangsa balita |
| `fact_ispu` | ISPU | 1 wilayah (snapshot 12 Okt 2026, 15:00 WIB) | PM2.5 per wilayah |
| `fact_jakarta_bulanan` | Jakarta | 1 bulan (seri Dinkes DKI, Jan–Jun 2023) | Tren bulanan Jakarta |

Aturan kerasnya:

1. **Jangan pernah menjumlahkan SKDR dengan karhutla.** Cakupan dan periode
   kedua seri berbeda; seri karhutla bukan bagian yang ditambahkan ke total
   nasional SKDR.
2. **Jumlah `fact_kasus_provinsi` bukan total nasional.** Tabel itu hanya
   berisi 10 provinsi teratas (10.530.385). Total nasional 14.088.945 ada di
   `fact_total_nasional` (tabel 1 baris, sengaja TANPA relasi, berperan
   sebagai tabel parameter).
3. **Grain mingguan adalah periode, bukan minggu individu.** Sumber hanya
   mempublikasikan rentang (minggu 27–31 dan 32–37), jadi
   `fact_kasus_mingguan` berisi 1 baris per periode. Kolom
   `total_laporan_periode_estimasi` adalah perkalian laporan per minggu ×
   jumlah minggu, dan untuk periode pertama merupakan batas bawah (sumber
   melaporkan "melampaui 400.000 per minggu").
4. **Per kapita memakai populasi BPS 2026 satu vintage** dari
   `dim_provinsi`. DI Yogyakarta, Sumatera Barat, dan Nusa Tenggara Barat
   tidak punya populasi satu vintage yang terverifikasi, jadi nilai
   per kapitanya kosong (blank) — itu disengaja, bukan error.
5. **Baris "5 provinsi lain (gabungan)"** di `fact_karhutla_provinsi` adalah
   gabungan Kalimantan Barat, Kalimantan Tengah, Kalimantan Timur, Jambi,
   dan Riau (rincian per provinsi tidak dipublikasikan sumber). Jangan
   perlakukan sebagai satu provinsi pada peta.

Relasi: `dim_provinsi[provinsi_id]` 1—* `fact_kasus_provinsi[provinsi_id]`,
`dim_provinsi[provinsi_id]` 1—* `fact_karhutla_provinsi[provinsi_id]`,
`dim_minggu[periode_id]` 1—* `fact_kasus_mingguan[periode_id]`,
`dim_kelompok_usia[kelompok_usia_id]` 1—* `fact_karhutla_usia[kelompok_usia_id]`,
`dim_wilayah[wilayah_id]` 1—* `fact_ispu[wilayah_id]`.
`fact_total_nasional`, `fact_karhutla_series`, dan `fact_jakarta_bulanan`
berdiri sendiri tanpa relasi. Tidak ada tabel yang ditandai sebagai date
table (alasannya di `build_guide.md`).

## Verifikasi angka (dihitung dari CSV kit ini)

| Indikator | Nilai acuan |
|---|---|
| Total Kasus Nasional SKDR (s.d. minggu ke-38 2026) | 14.088.945 |
| Jumlah 10 provinsi teratas SKDR | 10.530.385 |
| Pangsa 10 Provinsi Teratas | 74,7% |
| Provinsi tertinggi: Jawa Barat | 2.533.888 (17,98% dari nasional) |
| Kasus per 1.000 penduduk: DKI Jakarta | 150,0 |
| Kasus per 1.000 penduduk: Banten / Jawa Tengah / Jawa Barat / Jawa Timur | 65,8 / 61,2 / 49,5 / 32,5 |
| Pangsa Pulau Jawa dari 10 provinsi teratas | 86,3% |
| Rata-rata Laporan per Minggu (minggu 27–37) | 410.909 |
| Kenaikan Laporan Mingguan (periode awal ke puncak) | +5,0% (400.000 ke 420.000) |
| Total Kasus Karhutla (snapshot 13 Okt 2026) | 283.270 |
| Karhutla: Kalimantan Selatan / Sumatera Selatan | 74.636 / 74.458 (berdua 52,6%) |
| Kasus Balita Karhutla | 63.711 |
| Pangsa Balita | 22,5% |
| Pertumbuhan Karhutla Kali (27 Agt ke 13 Okt 2026) | 21,1x |
| Rata-rata Kasus Karhutla per Kab Kota (63 kab/kota) | 4.496 |
| Kasus Baru Harian Terakhir (13 Okt 2026) | 3.897 |
| PM2.5 Maks: Barito Kuala | 1.837 (6,1x ambang berbahaya 300) |
| PM2.5 Rata-rata 10 wilayah terburuk | 987,2 |
| Wilayah terburuk asal Kalimantan Tengah | 7 dari 10 wilayah |
| Jakarta bulanan 2023: total Jan–Jun / rata-rata per bulan / tertinggi | 638.291 / 106.381,8 / Maret 119.734 |

Visual WAJIB cocok dengan tabel ini. Jika berbeda, cek dulu: visual memakai
tabel fakta seri yang benar (SKDR vs karhutla) dan grain yang benar
(provinsi teratas vs total nasional).

## Measures — SKDR PROVINSI (tabel `fact_kasus_provinsi` dan `fact_total_nasional`)

```dax
Total Kasus SKDR =
SUM ( fact_kasus_provinsi[kasus_skdr_2026] )

Total Kasus Nasional SKDR =
SUM ( fact_total_nasional[total_kasus_skdr_2026] )

Pangsa Provinsi % =
DIVIDE ( [Total Kasus SKDR], [Total Kasus Nasional SKDR] ) * 100

Pangsa 10 Provinsi Teratas % =
DIVIDE (
    CALCULATE ( [Total Kasus SKDR], ALL ( dim_provinsi ) ),
    [Total Kasus Nasional SKDR]
) * 100

Kasus per 1000 Penduduk =
DIVIDE (
    SUM ( fact_kasus_provinsi[kasus_skdr_2026] ),
    SUM ( dim_provinsi[populasi_2026] )
) * 1000

Peringkat Provinsi =
RANKX (
    ALL ( dim_provinsi[provinsi] ),
    [Total Kasus SKDR],
    ,
    DESC,
    DENSE
)
```

Catatan: `Kasus per 1000 Penduduk` pada pilihan banyak provinsi menghasilkan
rate gabungan (total kasus dibagi total populasi pilihan), dan tampil kosong
untuk provinsi tanpa populasi terverifikasi.

## Measures — SKDR MINGGUAN (tabel `fact_kasus_mingguan`)

```dax
Rata-rata Laporan per Minggu =
DIVIDE (
    SUMX (
        fact_kasus_mingguan,
        fact_kasus_mingguan[laporan_per_minggu] * fact_kasus_mingguan[jumlah_minggu]
    ),
    SUM ( fact_kasus_mingguan[jumlah_minggu] )
)

Laporan Mingguan Maks =
MAX ( fact_kasus_mingguan[laporan_per_minggu] )

Kenaikan Laporan Mingguan % =
VAR awal =
    CALCULATE ( [Laporan Mingguan Maks], dim_minggu[label_periode] = "Awal musim kemarau" )
VAR puncak =
    CALCULATE ( [Laporan Mingguan Maks], dim_minggu[label_periode] = "Puncak musim kemarau" )
RETURN
    DIVIDE ( puncak - awal, awal ) * 100
```

Catatan: rata-rata ini tertimbang jumlah minggu per periode dan hanya
mencakup minggu 27–37 yang dilaporkan sumber. Hasil acuan: 410.909.

## Measures — KARHUTLA SERI WAKTU (tabel `fact_karhutla_series`)

```dax
Total Kasus Karhutla =
CALCULATE (
    SUM ( fact_karhutla_series[kasus_kumulatif] ),
    LASTDATE ( fact_karhutla_series[tanggal] )
)

Kasus Baru Harian Terakhir =
CALCULATE (
    SUM ( fact_karhutla_series[kasus_baru_harian] ),
    LASTDATE ( fact_karhutla_series[tanggal] )
)

Pertumbuhan Karhutla Kali =
VAR terakhir =
    CALCULATE (
        SUM ( fact_karhutla_series[kasus_kumulatif] ),
        LASTDATE ( fact_karhutla_series[tanggal] )
    )
VAR pertama =
    CALCULATE (
        SUM ( fact_karhutla_series[kasus_kumulatif] ),
        FIRSTDATE ( fact_karhutla_series[tanggal] )
    )
RETURN
    DIVIDE ( terakhir, pertama )

Rata-rata Kasus Karhutla per Kab Kota =
DIVIDE ( [Total Kasus Karhutla], 63 )
```

Catatan: `kasus_kumulatif` adalah angka kumulatif per tanggal snapshot, jadi
measure mengambil snapshot terakhir (bukan menjumlahkan semua tanggal).
Angka 63 pada measure terakhir adalah cakupan resmi pemantauan karhutla
(63 kabupaten/kota, 7 provinsi).

## Measures — KARHUTLA PROVINSI (tabel `fact_karhutla_provinsi`)

```dax
Total Kasus Karhutla per Provinsi =
SUM ( fact_karhutla_provinsi[kasus_karhutla] )

Pangsa Provinsi Karhutla % =
DIVIDE (
    [Total Kasus Karhutla per Provinsi],
    CALCULATE ( [Total Kasus Karhutla per Provinsi], ALL ( dim_provinsi ) )
) * 100
```

Catatan: jumlah measure ini pada semua baris = 283.270, sama dengan snapshot
terakhir `fact_karhutla_series`. Keduanya adalah seri karhutla yang sama,
hanya beda grain (waktu vs provinsi).

## Measures — KARHUTLA USIA (tabel `fact_karhutla_usia`)

```dax
Total Kasus Karhutla per Usia =
CALCULATE (
    SUM ( fact_karhutla_usia[kasus] ),
    LASTDATE ( fact_karhutla_usia[tanggal] )
)

Kasus Balita Karhutla =
CALCULATE (
    [Total Kasus Karhutla per Usia],
    dim_kelompok_usia[kelompok_usia] = "Balita (0 sampai 5 tahun)"
)

Pangsa Balita % =
DIVIDE (
    [Kasus Balita Karhutla],
    CALCULATE ( [Total Kasus Karhutla per Usia], ALL ( dim_kelompok_usia ) )
) * 100
```

Catatan: pangsa balita selalu dihitung pada snapshot terakhir (13 Okt 2026).
Pada snapshot 21 Sep 2026 porsinya 23,1% — porsi balita stabil di kisaran
22,5–23,1%.

## Measures — ISPU (tabel `fact_ispu`)

```dax
PM2.5 Maks =
MAX ( fact_ispu[pm25] )

PM2.5 Rata-rata =
AVERAGE ( fact_ispu[pm25] )

Wilayah PM2.5 Tertinggi =
MAXX (
    TOPN ( 1, SUMMARIZE ( fact_ispu, dim_wilayah[wilayah], "p", [PM2.5 Maks] ), [p], DESC ),
    dim_wilayah[wilayah]
)

PM2.5 Kali Ambang Berbahaya =
DIVIDE ( [PM2.5 Maks], 300 )

Jumlah Wilayah Berbahaya =
CALCULATE ( COUNTROWS ( fact_ispu ), fact_ispu[kategori_ispu] = "Berbahaya" )
```

Catatan: ambang kategori Berbahaya ISPU adalah PM2.5 di atas 300. Kesepuluh
wilayah di `fact_ispu` adalah 10 wilayah terburuk pada snapshot 12 Okt 2026
dan semuanya ber kategori Berbahaya, jadi `Jumlah Wilayah Berbahaya` = 10
pada data snapshot ini.

## Measures — JAKARTA BULANAN (tabel `fact_jakarta_bulanan`)

```dax
Total Kasus Jakarta Bulanan =
SUM ( fact_jakarta_bulanan[kasus_jakarta] )

Rata-rata Kasus Jakarta per Bulan =
AVERAGE ( fact_jakarta_bulanan[kasus_jakarta] )

Kasus Jakarta Bulanan Maks =
MAX ( fact_jakarta_bulanan[kasus_jakarta] )
```

Catatan: ini seri bulanan Dinkes DKI Jakarta tahun 2023 (Januari–Juni),
disajikan sebagai konteks musiman. Jangan campur dengan seri SKDR 2026.

## Aturan pakai

1. Satu visual = satu tabel fakta (satu seri, satu grain). Visual SKDR pakai
   measures SKDR; visual karhutla pakai measures KARHUTLA; jangan menaruh
   keduanya dalam satu visual atau satu total.
2. KPI total nasional WAJIB memakai `Total Kasus Nasional SKDR` (dari
   `fact_total_nasional`), bukan jumlah `fact_kasus_provinsi`.
3. Slicer Provinsi dari `dim_provinsi` memengaruhi `fact_kasus_provinsi` dan
   `fact_karhutla_provinsi`, tetapi pada halaman karhutla akan muncul baris
   gabungan "5 provinsi lain (gabungan)" — beri catatan pada visualnya.
4. Slicer tanggal snapshot hanya relevan di halaman karhutla (seri dan usia).
   Jangan pasang di halaman SKDR (tidak ada relasi tanggal ke fact SKDR).
5. Uji tiap measure pada satu filter sederhana dulu sebelum membangun halaman
   penuh. Contoh: tanpa filter apa pun, `Total Kasus Nasional SKDR` harus
   14.088.945, `Pangsa 10 Provinsi Teratas %` harus 74,7%, dan
   `Pangsa Balita %` harus 22,5%.
