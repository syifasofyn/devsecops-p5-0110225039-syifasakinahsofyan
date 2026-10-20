# Aplikasi To-Do List dengan Pipeline DevSecOps

## 1. Nama Aplikasi dan Fungsinya
**To-Do List CLI** adalah aplikasi manajemen tugas berbasis command line.
Pengguna dapat menambah tugas, melihat daftar tugas, menandai tugas selesai,
dan menghapus tugas. Data disimpan dalam file `tasks.json`.

## 2. Bahasa dan Framework
- Bahasa: Python 3
- Framework: tidak ada (hanya library bawaan Python)
- Unit test: `unittest`
- SAST tool: Bandit

## 3. Cara Menjalankan Aplikasi
```bash
git clone https://github.com/[USERNAME]/devsecops-p5-[NIM].git
cd devsecops-p5-[NIM]
python main.py
```

Menjalankan unit test:
```bash
python -m unittest discover -s tests -v
```

## 4. Struktur Proyek
| File | Fungsi |
|---|---|
| `main.py` | Menu utama program |
| `task.py` | Model data tugas |
| `storage.py` | Simpan/baca data JSON |
| `manager.py` | Logika pengelolaan tugas |
| `validator.py` | Validasi input |
| `tests/test_manager.py` | Unit test |
| `quality_gate.py` | Penentu lulus/gagal hasil SAST |

## 5. Overview Pipeline CI/CD
Workflow: `.github/workflows/devsecops.yml`

**Trigger:** push ke branch `main` dan pull request ke branch `main`.

**Job `build`** (ubuntu-latest):
1. Checkout kode
2. Setup Python 3.12
3. Install dependencies
4. Menjalankan unit test

**Job `sast-scan`** (ubuntu-latest, `needs: build`):
1. Checkout kode
2. Setup Python 3.12
3. Install Bandit
4. Menjalankan Bandit dan menyimpan laporan JSON
5. Upload laporan sebagai artifact
6. **Quality Gate**: pipeline GAGAL jika ada temuan HIGH atau MEDIUM,
   dan LULUS jika tidak ada.