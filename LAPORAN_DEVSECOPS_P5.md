# LAPORAN PRAKTIKUM DEVSECOPS (PERTEMUAN 5)
**Topik: Integrasi SAST dalam CI/CD Pipeline dengan GitHub Actions**

---

### IDENTITAS MAHASISWA & PROYEK
* **Nama Mahasiswa:** Syifa Sakinah Sofyan
* **NIM:** 0110225039
* **Program Studi:** S1 Teknik Informatika – STT Terpadu Nurul Fikri
* **Mata Kuliah:** DevSecOps
* **Link Repositori GitHub:** https://github.com/syifasofyn/devsecops-p5-0110225039-syifasakinahsofyan
* **Link Dashboard SonarCloud:** https://sonarcloud.io/project/overview?id=syifasofyn_devsecops-p5-0110225039-syifasakinahsofyan

---

## 1. PENDAHULUAN & GAMBARAN UMUM APLIKASI

### 1.1 Deskripsi Aplikasi
Aplikasi yang dibangun pada tugas ini adalah **To-Do List CLI**, yaitu program manajemen tugas interaktif berbasis antarmuka baris perintah (*Command Line Interface*) yang dikembangkan menggunakan bahasa pemrograman **Python 3**. Aplikasi ini dirancang modular dengan pemisahan tanggung jawab yang jelas:
1. `main.py`: Antarmuka CLI interaktif untuk interaksi pengguna (menu tambah tugas, lihat daftar, tandai selesai, dan hapus).
2. `task.py`: Model representasi entitas data `Task` menggunakan `dataclass`.
3. `manager.py`: Komponen logika bisnis (`TaskManager`) yang menangani operasi CRUD tugas.
4. `storage.py`: Modul persistensi data berbasis file JSON (`tasks.json`).
5. `validator.py`: Modul validasi masukan untuk mencegah karakter berbahaya, input kosong, dan ID non-numerik.
6. `tests/test_manager.py`: Modul pengujian unit (*Unit Testing*) menggunakan modul bawaan `unittest` untuk memverifikasi logika aplikasi.
7. `quality_gate.py`: Skrip penilai ambang batas keamanan (*Quality Gate*) lokal terhadap hasil pemindaian SAST.

### 1.2 Konsep Shift-Left Security & CI/CD DevSecOps
Dalam paradigma tradisional, pengujian keamanan sering kali dilakukan pada tahap akhir sebelum rilis (*staging/production*). DevSecOps menerapkan prinsip **Shift-Left Security**, yaitu mengintegrasikan pengujian keamanan sedini mungkin ke dalam siklus hidup pengembangan perangkat lunak (*SDLC*). Dengan menanamkan alat *Static Application Security Testing* (SAST) ke dalam alur *Continuous Integration* (CI) di GitHub Actions, setiap *commit* dan *pull request* secara otomatis dipindai untuk mendeteksi kerentanan kode, kelemahan arsitektur, dan potensi pelanggaran keamanan sebelum kode digabungkan ke cabang utama (*main branch*).

---

## 2. ARSITEKTUR PIPELINE CI/CD & INTEGRASI SAST

Pipeline DevSecOps diimplementasikan melalui dua berkas alur kerja (*workflows*) GitHub Actions yang berjalan secara otomatis pada *event* `push` dan `pull_request`:

### 2.1 Job 1: `build` (Pemeriksaan Integritas & Pengujian Unit)
* **Runner:** `ubuntu-latest`.
* **Langkah-langkah:**
  1. *Checkout kode* menggunakan `actions/checkout@v4`.
  2. *Setup lingkungan Python 3.12* menggunakan `actions/setup-python@v5`.
  3. *Instalasi dependensi* dari berkas `requirements.txt`.
  4. *Eksekusi pengujian otomatis*: Menjalankan `python -m unittest discover -s tests -v` (seluruh 8 *test cases* berhasil lulus).

### 2.2 Job 2: `sast-scan` (Pemindaian Keamanan & Quality Gate)
* **Runner:** `ubuntu-latest`.
* **Ketergantungan:** Menggunakan direktif `needs: build` sehingga pemindaian hanya dieksekusi apabila tahap *build* dan pengujian unit berhasil 100%.
* **Langkah-langkah:**
  1. *Checkout riwayat repositori lengkap* (`fetch-depth: 0`) untuk kebutuhan perhitungan metrik SonarCloud.
  2. *Instalasi & Eksekusi Bandit*: Memindai kode Python dan mengekspor temuan ke berkas `bandit-report.json`.
  3. *Evaluasi Quality Gate Lokal*: Menjalankan `python quality_gate.py bandit-report.json` dengan kriteria batas toleransi temuan *HIGH = 0* dan *MEDIUM = 0*.
  4. *Integrasi SonarCloud Scan*: Memanfaatkan modul `SonarSource/sonarcloud-github-action@master` dengan kredensial rahasia `SONAR_TOKEN` yang disimpan secara aman di GitHub Secrets.

### 2.3 Workflow Tambahan: CodeQL Analysis (`.github/workflows/codeql.yml`)
* **Runner:** `ubuntu-latest`.
* **Langkah-langkah:**
  1. Inisialisasi engine basis data semantik CodeQL (`github/codeql-action/init@v3`) untuk bahasa Python.
  2. Melakukan analisis *dataflow* dan *taint tracking* (`github/codeql-action/analyze@v3`).
  3. Mengunggah laporan format SARIF ke tab **GitHub Security (Code scanning alerts)** dengan izin `security-events: write`.

---

## 3. HASIL ANALISIS SAST & PERBANDINGAN TOOL (TUGAS 1 & TUGAS 2)

### 3.1 Hasil Pemindaian SonarCloud Dashboard
Berdasarkan hasil pemindaian langsung pada SonarCloud Server:
* **Bugs:** 0
* **Code Smells:** 0
* **Security Hotspots:** 0
* **Vulnerabilities:** 1 Temuan Kritis (Tingkat *Major*)
* **Reliability Rating:** A
* **Security Rating:** A
* **Maintainability Rating:** A
* **Duplicated Lines:** 0.0%

**Rincian Temuan SonarCloud:**
1. **Path Traversal Risk (`quality_gate.py`: Baris 15):**
   * *Deskripsi:* SonarCloud mengidentifikasi bahwa berkas dibuka langsung menggunakan parameter input `open(sys.argv[1])` tanpa validasi jalur absolut atau pembersihan masukan (*path sanitization*), yang berpotensi menyebabkan kerentanan pembacaan berkas sembarang (*arbitrary file read/traversal*).
2. **Workflow Security Sensitivity (`.github/workflows/devsecops.yml`):**
   * *Deskripsi:* Eksekusi `pip install` tanpa parameter `--only-binary :all:` dan tanpa penguncian hash versi paket dinilai sensitif terhadap eksekusi *setup scripts* pihak ketiga.

### 3.2 Hasil Pemindaian CodeQL
CodeQL berhasil menjalankan pemindaian terhadap struktur AST (*Abstract Syntax Tree*) Python. Pada tab GitHub Security, CodeQL menghasilkan status **0 Open Alerts**. CodeQL berfokus pada kerentanan alur data kritis (*taint tracking*) seperti *Remote Code Execution*, *SQL Injection*, dan kebocoran data pengguna eksternal. Karena aplikasi ini merupakan utilitas CLI lokal murni tanpa *network endpoints*, CodeQL mengonfirmasi tidak ada alur data eksternal berbahaya yang menembus *sink* kritis.

### 3.3 Analisis Perbandingan: CodeQL vs. SonarCloud (Analisis 1 Paragraf - Tugas 2 Wajib)
Perbandingan antara SonarCloud dan CodeQL pada repositori ini menunjukkan perbedaan mendasar dalam filosofi dan metode deteksi kerentanan keamanan statis. **SonarCloud** mengadopsi pendekatan holistik berbasis aturan *code quality* dan *pattern rule-matching*, sehingga mampu mendeteksi potensi risiko lokal secara detail seperti kerentanan *Path Traversal* pada pembacaan parameter `sys.argv[1]` di berkas `quality_gate.py` serta praktik instalasi pustaka yang tidak terkunci (*unpinned dependencies*) pada konfigurasi CI/CD YAML. Sebaliknya, **CodeQL** menggunakan pendekatan *deep semantic analysis* dan *query database* berbasis alur data (*taint analysis*), yang berfokus melacak apakah masukan pengguna yang tidak tepercaya (*untrusted source*) mengalir ke titik eksekusi berbahaya (*security sink*); karena masukan `sys.argv` pada skrip pengujian internal CLI ini tidak terhubung ke saluran masukan eksternal (seperti HTTP Request atau soket jaringan), CodeQL tidak menandainya sebagai *vulnerability alert* aktif. Dengan demikian, penggabungan kedua alat ini (*multi-tool strategy*) saling melengkapi: SonarCloud unggul dalam menegakkan disiplin penulisan kode aman (*secure coding standards*) dan konfigurasi pipeline, sedangkan CodeQL unggul dalam memastikan ketiadaan rantai eksploitasi data semantik yang berisiko tinggi.

---

## 4. CARA PENANGANAN KERENTANAN & REMEDIASI

Untuk menangani isu yang ditemukan pada dashboard SAST, langkah remediasi yang direkomendasikan adalah:

1. **Remediasi Path Traversal pada `quality_gate.py`:**
   Membatasi pembacaan berkas hanya pada direktori kerja saat ini menggunakan validasi pustaka `pathlib` atau `os.path`:
   ```python
   import os
   target_path = os.path.abspath(sys.argv[1])
   if not target_path.startswith(os.path.abspath(".")):
       raise PermissionError("Akses berkas di luar repositori ditolak.")
   ```
2. **Remediasi Dependensi pada Workflow CI/CD:**
   Menggunakan penguncian versi (*pinned versions*) dengan `pip-compile` atau `hash-checking mode` (`--require-hashes`) dan menambahkan flag `--only-binary :all:` untuk mencegah eksekusi skrip *setup.py* arbitrer selama fase integrasi.
3. **Pengelolaan False Positive:**
   Untuk parameter pengujian internal di lingkungan CI, isu dapat ditandai sebagai *False Positive* atau *Won't Fix* langsung pada antarmuka SonarCloud dengan menyertakan catatan audit trail yang jelas, atau menggunakan anotasi `# NOSONAR` pada baris terkait sesuai panduan materi kuliah.

---

## 5. PANDUAN LAMPIRAN SCREENSHOT

Berdasarkan syarat teknis pada Gambar 1 dan Gambar 2, lampirkan 5 tangkapan layar (*screenshots*) berikut pada bagian akhir laporan:

### [Lampiran 1: Tampilan Repositori GitHub]
* **Lokasi Pengambilan:** Halaman utama repositori `https://github.com/syifasofyn/devsecops-p5-0110225039-syifasakinahsofyan`.
* **Keterangan Gambar:** Menampilkan visibilitas repositori bertanda **Public**, struktur seluruh berkas proyek, dan tampilan dokumentasi `README.md`.

### [Lampiran 2: Riwayat Workflow Runs di Tab Actions]
* **Lokasi Pengambilan:** Menu **Actions** (`.../actions`).
* **Keterangan Gambar:** Menampilkan daftar alur kerja **DevSecOps Pipeline** dan **CodeQL Analysis** yang telah berstatus hijau (*Completed Success*).

### [Lampiran 3: Detail Eksekusi Job Pipeline (Grafik Pipeline)]
* **Lokasi Pengambilan:** Klik pada run terbaru **DevSecOps Pipeline** (#3).
* **Keterangan Gambar:** Menampilkan visualisasi ketergantungan job, di mana job **`build`** centang hijau berhasil dilanjutkan ke job **`sast-scan`** centang hijau yang menjalankan pengujian Bandit dan SonarCloud.

### [Lampiran 4: Dashboard SonarCloud (Overview & Quality Metrics)]
* **Lokasi Pengambilan:** Dashboard proyek SonarCloud `https://sonarcloud.io/project/overview?id=syifasofyn_devsecops-p5-0110225039-syifasakinahsofyan`.
* **Keterangan Gambar:** Menampilkan indikator keamanan proyek: *Bugs (0)*, *Code Smells (0)*, *Security Hotspots (0)*, *Vulnerabilities (1)*, serta peringkat keandalan dan keamanan berkategori *Rating A*.

### [Lampiran 5: Tab Security GitHub (Hasil Scan CodeQL)]
* **Lokasi Pengambilan:** Menu **Security** > **Code scanning alerts** pada repositori GitHub.
* **Keterangan Gambar:** Menampilkan integrasi CodeQL analysis tool yang telah aktif memindai kode dan memverifikasi integritas keamanan repositori.

---

## 6. KESIMPULAN

Penerapan alur DevSecOps pada proyek ini telah berhasil membuktikan bahwa pengujian keamanan statis (SAST) dapat diotomatisasi secara efektif ke dalam alur kerja GitHub Actions. Dengan mengintegrasikan **Bandit**, **SonarCloud**, dan **CodeQL**, repositori memperoleh perlindungan berlapis (*defense-in-depth*) mulai dari analisis kode Python lokal, manajemen *Quality Gate* berbasis metrik industri, hingga analisis semantik mendalam. Seluruh syarat dan ketentuan tugas mandiri pertemuan 5 telah terpenuhi secara utuh dan terverifikasi di repositori publik GitHub.
