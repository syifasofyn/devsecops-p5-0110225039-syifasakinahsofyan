# Aplikasi To-Do List dengan Pipeline DevSecOps

## 1. Nama Aplikasi dan Fungsinya
**To-Do List CLI** adalah aplikasi manajemen tugas berbasis command line.
Pengguna dapat menambah tugas, melihat daftar tugas, menandai tugas selesai,
dan menghapus tugas. Data disimpan dalam file `tasks.json`.

## 2. Bahasa dan Framework
- Bahasa: Python 3
- Framework: Library standar Python
- Unit Test: `unittest`
- SAST Tools: Bandit, SonarCloud, dan CodeQL

## 3. Cara Menjalankan Aplikasi
```bash
git clone https://github.com/syifasofyn/devsecops-p5-0110225039-syifasakinahsofyan.git
cd devsecops-p5-0110225039-syifasakinahsofyan
python main.py
```

Menjalankan unit test:
```bash
python -m unittest discover -s tests -v
```

## 4. Struktur Proyek
| File / Direktori | Fungsi |
|---|---|
| `main.py` | Antarmuka CLI interaktif menu utama aplikasi |
| `task.py` | Model data tugas (Task) |
| `storage.py` | Penyimpanan data ke file `tasks.json` |
| `manager.py` | Logika bisnis manajemen tugas (tambah, selesai, hapus, daftar) |
| `validator.py` | Validasi judul dan ID tugas |
| `tests/test_manager.py` | Unit test untuk manager dan validator |
| `quality_gate.py` | Script Quality Gate untuk verifikasi temuan Bandit |
| `sonar-project.properties` | Konfigurasi analisis SonarCloud |
| `.github/workflows/devsecops.yml` | Pipeline CI/CD GitHub Actions (Build, Bandit, Quality Gate, SonarCloud) |
| `.github/workflows/codeql.yml` | Pipeline GitHub Actions untuk analisis keamanan mendalam CodeQL |

## 5. Overview Pipeline CI/CD

### A. Workflow DevSecOps (`.github/workflows/devsecops.yml`)
- **Trigger:** `push` dan `pull_request` ke branch `main`.
- **Job `build`** (Runner: `ubuntu-latest`):
  1. Checkout source code.
  2. Setup environment Python 3.12.
  3. Install dependencies dari `requirements.txt`.
  4. Menjalankan unit test otomatis (`unittest`).
- **Job `sast-scan`** (Runner: `ubuntu-latest`, `needs: build`):
  1. Checkout kode lengkap (`fetch-depth: 0`).
  2. Setup environment Python 3.12.
  3. Install dan jalankan scanner **Bandit**.
  4. Simpan dan unggah laporan Bandit (`bandit-report.json`) sebagai artifact.
  5. Eksekusi **Quality Gate Bandit** (`quality_gate.py` memblokir jika ada issue tingkat HIGH / MEDIUM).
  6. Eksekusi **SonarCloud Scan** menggunakan `sonarcloud-github-action` dan `SONAR_TOKEN`.

### B. Workflow CodeQL (`.github/workflows/codeql.yml`)
- **Trigger:** `push` dan `pull_request` ke branch `main`, serta terjadwal mingguan (`cron`).
- **Job `analyze`** (Runner: `ubuntu-latest`):
  1. Checkout kode.
  2. Inisialisasi engine semantic analysis CodeQL untuk bahasa Python.
  3. Analisis keamanan mendalam (SAST) dan unggah hasil ke tab **Security (Code scanning)** di GitHub.