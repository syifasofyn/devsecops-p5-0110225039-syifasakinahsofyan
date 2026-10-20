from manager import TaskManager


def print_menu():
    print("\n=== TO-DO LIST CLI ===")
    print("1. Lihat semua tugas")
    print("2. Tambah tugas baru")
    print("3. Tandai tugas selesai")
    print("4. Hapus tugas")
    print("5. Keluar")


def main():
    manager = TaskManager()
    while True:
        print_menu()
        choice = input("Pilih menu (1-5): ").strip()
        if choice == "1":
            tasks = manager.list_tasks()
            if not tasks:
                print("Belum ada tugas.")
            else:
                for t in tasks:
                    status = "[V]" if t.done else "[ ]"
                    print(f"{status} {t.id}. {t.title}")
        elif choice == "2":
            title = input("Masukkan judul tugas: ")
            try:
                task = manager.add_task(title)
                print(f"Tugas berhasil ditambahkan (ID: {task.id})")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "3":
            tid = input("Masukkan ID tugas yang selesai: ")
            try:
                manager.complete_task(tid)
                print("Tugas berhasil ditandai selesai.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "4":
            tid = input("Masukkan ID tugas yang akan dihapus: ")
            try:
                manager.delete_task(tid)
                print("Tugas berhasil dihapus.")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "5":
            print("Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()