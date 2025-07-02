# Instagram Network Analysis

## Deskripsi Project
Aplikasi ini menganalisis data Instagram (misal: hasil scraping) untuk menemukan insight seperti jaringan pengguna, analisis sentimen, kata kunci penting, dan statistik aktivitas. Cocok untuk riset sosial, pemetaan isu, atau analisis kampanye digital.

## Teknologi yang Digunakan
- **Backend:** FastAPI (Python)
- **Frontend:** ReactJS (Material UI)
- **Data Science:** pandas, scikit-learn, networkx, matplotlib, wordcloud, vaderSentiment

## Fitur Utama
- **Upload Data:** Mendukung file CSV/JSON dengan kolom seperti username, caption, tanggal_posting, tagged_users, likes.
- **Analisis Jaringan:** Visualisasi hubungan antar pengguna (mention/tag), deteksi influencer (degree & betweenness centrality).
- **Analisis Teks:** Ekstraksi kata kunci (TF-IDF), frekuensi kata, wordcloud, deteksi hashtag populer.
- **Analisis Sentimen:** Klasifikasi sentimen caption (positif, netral, negatif) dan top user berdasarkan sentimen.
- **Statistik Data:** Total user, total post, rata-rata likes, panjang caption, hashtag unik, user paling aktif, hari paling aktif, dsb.
- **Visualisasi:** Wordcloud, graph jaringan, tabel hasil analisis.

## Contoh Input
File CSV dengan format seperti berikut (lihat juga `dummy.csv`):

```
username,caption,tanggal_posting,tagged_users,likes
aktivis1,"Aksi demo menolak #tambangnikel di Raja Ampat! #SaveRajaAmpat",2024-06-01,"aktivis2;warga1",120
... (baris lain)
```

## Output
Setelah upload dan analisis, aplikasi menampilkan:
- Statistik data (user, post, likes, hashtag, dsb)
- Top hashtag, top user (post/likes), top mentioned user
- Wordcloud & kata kunci (TF-IDF)
- Grafik jaringan (influencer & detail centrality)
- Statistik sentimen & top user per kategori sentimen
- Visualisasi interaktif di frontend

## Cara Menjalankan
### 1. Persiapan Backend
- Masuk ke folder `backend`
- Install dependensi Python:
  ```bash
  pip install -r requirements.txt
  ```
- Jalankan backend (FastAPI):
  ```bash
  uvicorn app.main:app --reload
  ```

### 2. Persiapan Frontend
- Masuk ke folder `frontend`
- Install dependensi Node.js:
  ```bash
  npm install
  ```
- Jalankan frontend:
  ```bash
  npm start
  ```

### 3. Jalankan Sekaligus (Windows)
- Jalankan file `.\start-all.bat` di root project untuk membuka backend & frontend secara otomatis di 2 terminal.

### 4. Akses Aplikasi
- Buka browser ke [http://localhost:3000](http://localhost:3000) untuk frontend.
- Backend API tersedia di [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI).

## Dependensi
### Backend (lihat `backend/requirements.txt`)
- fastapi, uvicorn, pandas, networkx, scikit-learn, nltk, vaderSentiment, matplotlib, wordcloud, pyvis, python-multipart

### Frontend (lihat `frontend/package.json`)
- React, Material UI, Chart.js, react-chartjs-2, dayjs, material-react-table, dll.

## Struktur Folder
- `backend/` : kode backend (API, analisis, model)
- `frontend/` : kode frontend (React UI)
- `dummy.csv` : contoh data input
- `start-all.bat` : script untuk menjalankan backend & frontend sekaligus

## Catatan
- Pastikan Python & Node.js sudah terinstall.
- Data input harus sesuai format (lihat contoh).
- Untuk analisis optimal, gunakan data hasil scraping Instagram yang relevan. 