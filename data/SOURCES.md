# Sumber Data — Analisis ISPA Indonesia 2026

## Sifat dataset: KOMPILASI, bukan file mentah resmi

Dataset ini **dikompilasi** dari angka-angka resmi yang dipublikasikan (rilis pers
Kemenkes dan laporan yang mengutipnya). Tidak ada file CSV mentah ISPA yang bisa
diunduh dari data.go.id atau Jakarta Open Data pada saat proyek ini dibuat
(dicek 16 Oktober 2026). Setiap angka di bawah ini dicatat bersama sumber dan
tanggalnya. Tidak ada satu pun angka yang dikarang.

## DUA SERI YANG TIDAK BOLEH DICAMPUR

1. **Seri nasional SKDR** — laporan ISPA seluruh Indonesia melalui Sistem
   Kewaspadaan Dini dan Respons (SKDR). Total nasional 14.088.945 laporan
   hingga minggu epidemiologi ke-38 tahun 2026.
2. **Seri pemantauan karhutla** — pemantauan khusus dampak kesehatan karhutla
   di 63 kabupaten/kota, 7 provinsi. Total 283.270 kasus (18 Agustus–13 Oktober
   2026).

Kedua seri ini memiliki **cakupan dan tanggal yang berbeda**. Seri karhutla
BUKAN bagian yang dijumlahkan ke seri nasional di dalam analisis ini, dan
keduanya tidak pernah digabung dalam satu total atau satu chart.

## Sumber per angka

### Seri nasional SKDR
| Angka | Nilai | Sumber | Tanggal rilis |
|---|---|---|---|
| Total nasional 2026 (s.d. minggu ke-38) | 14.088.945 laporan | Kemenkes, Situation Report Penyakit Infeksi Emerging dan Potensial KLB/Wabah, dikutip GoodStats | GoodStats 13 Okt 2026 |
| Jawa Barat | 2.533.888 | Kemenkes via SKDR s.d. 3 Okt 2026, dikutip GoodStats | 13 Okt 2026 |
| Jawa Tengah | 2.358.930 | Kemenkes via SKDR s.d. 3 Okt 2026, dikutip GoodStats | 13 Okt 2026 |
| DKI Jakarta | 1.600.814 | Kemenkes via SKDR s.d. 3 Okt 2026, dikutip GoodStats | 13 Okt 2026 |
| Jawa Timur | 1.374.373 | Kemenkes via SKDR s.d. 3 Okt 2026, dikutip GoodStats | 13 Okt 2026 |
| Banten | 832.030 | Kemenkes via SKDR, grafik 10 provinsi, dikutip GoodStats | 13 Okt 2026 |
| Sulawesi Selatan | 408.770 | Kemenkes via SKDR, grafik 10 provinsi, dikutip GoodStats | 13 Okt 2026 |
| DI Yogyakarta | 388.380 | Kemenkes via SKDR, grafik 10 provinsi, dikutip GoodStats | 13 Okt 2026 |
| Sumatera Utara | 364.050 | Kemenkes via SKDR, grafik 10 provinsi, dikutip GoodStats | 13 Okt 2026 |
| Sumatera Barat | 337.200 | Kemenkes via SKDR, grafik 10 provinsi, dikutip GoodStats | 13 Okt 2026 |
| Nusa Tenggara Barat | 331.950 | Kemenkes via SKDR, grafik 10 provinsi, dikutip GoodStats | 13 Okt 2026 |
| Laporan per minggu, minggu 27–31 | >400.000 | Kemenkes, dikutip GoodStats | 13 Okt 2026 |
| Laporan per minggu, minggu 32–37 | ~420.000 | Kemenkes, dikutip GoodStats | 13 Okt 2026 |

Catatan: angka 4 provinsi teratas dikutip eksak dari teks artikel. Angka
peringkat 5–10 dibaca dari grafik batang GoodStats (nilai dalam ribuan, dua
desimal) sehingga merupakan nilai yang dibulatkan. Hal ini dicatat di kolom
`catatan` pada file CSV.

### Seri pemantauan karhutla
| Angka | Nilai | Sumber | Tanggal rilis |
|---|---|---|---|
| Total 18 Agt–13 Okt 2026 | 283.270 | Kemenkes via Dir. Kesehatan Lingkungan Then Suyanti, dikutip Cobisnis | 14 Okt 2026 |
| Usia >5 tahun | 219.559 | Kemenkes, dikutip Cobisnis | 14 Okt 2026 |
| Usia <5 tahun (balita) | 63.711 | Kemenkes, dikutip Cobisnis | 14 Okt 2026 |
| Kalimantan Selatan | 74.636 | Kemenkes, dikutip Cobisnis | 14 Okt 2026 |
| Sumatera Selatan | 74.458 | Kemenkes, dikutip Cobisnis | 14 Okt 2026 |
| Total Agt–21 Sep 2026 | 174.694 | Kemenkes, dikutip Berita Hari Ini | 23 Sep 2026 |
| Balita Agt–21 Sep 2026 | 40.363 | Kemenkes, dikutip Berita Hari Ini | 23 Sep 2026 |
| Kasus aktif 22 Sep 2026 | 4.533 | Kemenkes, dikutip Berita Hari Ini | 23 Sep 2026 |
| Total s.d. 27 Agt 2026 | 13.449 | Kemenkes, dikutip GoodStats | 14 Okt 2026 |
| Penduduk terdampak s.d. 27 Agt 2026 | 10.674.201 | Kemenkes, dikutip GoodStats | 14 Okt 2026 |
| Kasus baru harian 13 Okt 2026 | 3.897 | Kemenkes, dikutip HalloNews | 15 Okt 2026 |
| Tenaga kesehatan dimobilisasi | 2.106 | Kemenkes, dikutip NTV News | 14 Okt 2026 |
| Masker didistribusikan | >2,8 juta | Kemenkes, dikutip NTV News | 14 Okt 2026 |
| Puskesmas siaga | 1.691 | Kemenkes, dikutip Radar Garut | 22 Sep 2026 |
| RS rujukan siaga | 360 | Kemenkes, dikutip Radar Garut | 22 Sep 2026 |
| Labkesmas siaga | 87 | Kemenkes, dikutip Radar Garut | 22 Sep 2026 |
| 7 provinsi terdampak | Kalbar, Kalteng, Kalsel, Kaltim, Jambi, Riau, Sumsel | Kemenkes, dikutip GoodStats | 14 Okt 2026 |

### Kualitas udara (ISPU)
| Angka | Nilai | Sumber |
|---|---|---|
| 10 wilayah PM2,5 terburuk, 12 Okt 2026 15:00 WIB | Barito Kuala 1.837; Kapuas 1.681; Palangka Raya (Jekan Raya) 1.301; Katingan 1.214; Hulu Sungai Selatan 921; Gunung Mas 674; Barito Selatan (Sanggu) 592; Murung Raya 577; Kotawaringin Timur 568; Muaro Jambi 507 | ISPU KemenLH, dikutip GoodStats |
| Kabupaten/kota kategori berbahaya | 12 (6 Kalteng, 1 Kalsel, 2 Jambi, 2 Sulsel, 1 Riau) | Kemenkes, dikutip Cobisnis, 14 Okt 2026 |
| Wilayah kategori sangat tidak sehat | 9 | Kemenkes, dikutip Cobisnis, 14 Okt 2026 |

Catatan: redaksi sumber berbeda-beda tentang apakah 9 wilayah "sangat tidak
sehat" merupakan bagian dari 12 wilayah "berbahaya" atau kelompok terpisah.
Analisis ini melaporkan kedua angka apa adanya tanpa menjumlahkannya.

### Jakarta
| Angka | Nilai | Sumber |
|---|---|---|
| Kasus Jan–Okt 2025 | 1.966.308 | Dinkes DKI Jakarta, dikutip ValidNews/Antara |
| Kasus Jan–Nov 2025 | 2,5 juta (dibulatkan) | Dinkes DKI Jakarta, dikutip Bisik.id |
| Kenaikan musiman Sep 2026 | +15,7% | Dinkes DKI Jakarta, dikutip NTV News, 22 Sep 2026 |
| Bulanan 2023 | Jan 102.609; Feb 104.638; Mar 119.734; Apr 109.705; Mei 99.130; Jun 102.475 | Dinkes DKI Jakarta, dikutip Sonora, 11 Agu 2023 |

### Populasi (denominator per kapita)
Populasi 2026 per provinsi dari BPS, Statistik Indonesia 2026, dikutip GoodStats
("10 Provinsi dengan Jumlah Penduduk Terbanyak 2026"). Dipakai SATU vintage
yang sama untuk semua perbandingan per kapita: Jawa Barat 51.160.000; Jawa
Tengah 38.560.000; DKI Jakarta 10.670.000; Jawa Timur 42.350.000; Banten
12.640.000; Sulawesi Selatan 9.660.000; Sumatera Utara 15.980.000; Sumatera
Selatan 9.020.000. Untuk DI Yogyakarta, Sumatera Barat, dan Nusa Tenggara Barat
tidak ditemukan angka populasi satu vintage yang terverifikasi, sehingga ketiga
provinsi tersebut dikeluarkan dari peringkat per kapita (nilai absolutnya tetap
ditampilkan).

## Batasan yang harus dipahami
- Angka SKDR adalah **laporan kasus**, bukan jumlah orang unik — satu orang
  bisa tercatat lebih dari sekali jika berobat berulang.
- Cakupan dan kelengkapan pelaporan berbeda antarprovinsi; provinsi dengan
  fasilitas kesehatan lebih banyak cenderung mencatat lebih banyak kasus.
- Korelasi tingkat provinsi (misalnya ISPU buruk dan kasus ISPA tinggi di
  wilayah yang sama) adalah analisis ekologis: tidak membuktikan sebab-akibat
  pada level individu.
- Angka peringkat 5–10 SKDR dibaca dari grafik (dibulatkan), bukan angka eksak.
- Seri karhutla hanya mencakup 63 kabupaten/kota terdampak, bukan seluruh
  provinsi tersebut.
