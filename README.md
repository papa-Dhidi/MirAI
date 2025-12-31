# MirAI – Website AI Pencari Film

## Deskripsi Proyek

**MirAI** merupakan sebuah website berbasis **Artificial Intelligence (AI)** yang membantu pengguna menemukan film yang **tidak mereka ketahui judulnya**, hanya dengan memasukkan **ciri-ciri, deskripsi, atau gambaran film** yang diingat.

MirAI dikembangkan sebagai **aplikasi web berbasis Django (Python Framework)** dengan memanfaatkan integrasi **IMDb API** untuk data film dan **Gemini AI API** untuk pemrosesan bahasa alami serta rekomendasi cerdas.

Proyek ini dibuat sebagai **tugas kuliah**, sekaligus sebagai studi penerapan AI, API eksternal, dan pengembangan aplikasi web modern.

---

## Tujuan Pembuatan

Tujuan utama dari pengembangan MirAI adalah:

* Membantu pengguna menemukan film berdasarkan ciri-ciri atau deskripsi
* Menerapkan teknologi AI dalam pencarian dan rekomendasi film
* Mengintegrasikan API pihak ketiga (IMDb & Gemini AI)
* Mempelajari pengembangan aplikasi web Django secara modular

---

## Fitur Utama

MirAI memiliki beberapa fitur utama sebagai berikut:

### 🤖 AI Chat (Film Assistant)

* Chat AI untuk mencari rekomendasi film
* Chat AI untuk mendapatkan informasi detail film
* Pencarian film hanya berdasarkan deskripsi atau ciri-ciri

### 🔍 Pencarian Film

* Pencarian film menggunakan kata kunci
* Pencarian film menggunakan filter (genre, tahun, rating, dll)

### 🎬 Discovery & Recommendation

* Halaman **Trending Movies**
* Halaman **Top Rated Movies**
* Halaman **Upcoming Movies**
* Rekomendasi film berbasis AI

### ⭐ Watchlist & Favorite

* Menyimpan film ke **Watchlist**
* Menandai film sebagai **Favorite**
* Halaman khusus Watchlist

### 📊 Dashboard Pengguna

* Riwayat **AI Chat (Continue Your Session)**
* Daftar film **Favorite**
* Daftar film **Watchlist**
* Rekomendasi film dari AI

---

## Teknologi yang Digunakan

* Python 3
* Django Framework
* HTML, CSS, JavaScript
* IMDb API
* Gemini AI API
* Virtual Environment (venv)
* Git & GitHub

---

---

## Penggunaan IMdb dan Gemini AI

Isi file `.env` dengan API Key berikut:

```
IMDB_API_KEY=your_imdb_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

> Tanpa API Key yang valid, fitur pencarian film dan AI Chat tidak akan berfungsi dengan baik.

## Lisensi

Proyek ini dibuat untuk keperluan pembelajaran dan tugas kuliah.
