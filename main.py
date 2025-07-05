import json
from models.transaksi import Pemasukan, Pengeluaran
from models.user import User
from models.reminder import SaldoReminder, PengeluaranReminder

DATA_FILE = "data/transaksi.json"
import os

# Buat folder dan file jika belum ada
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists("data/transaksi.json"):
    with open("data/transaksi.json", "w") as f:
        f.write("[]")

def load_transaksi():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            transaksi_list = []
            for item in data:
                if item["tipe"] == "pemasukan":
                    transaksi_list.append(Pemasukan(item["judul"], item["jumlah"], item["tanggal"]))
                elif item["tipe"] == "pengeluaran":
                    transaksi_list.append(Pengeluaran(item["judul"], item["jumlah"], item["tanggal"]))
            return transaksi_list
    except:
        return []

def save_transaksi(transaksi_list):
    with open(DATA_FILE, "w") as f:
        json.dump([t.to_dict() for t in transaksi_list], f, indent=4)

def tampilkan_menu():
    print("\n=== MoneyMind: Pengingat Keuangan Pribadi ===")
    print("1. Lihat semua transaksi")
    print("2. Tambah pemasukan")
    print("3. Tambah pengeluaran")
    print("4. Hapus transaksi")
    print("5. Kirim pengingat keuangan")
    print("0. Keluar")

def main():
    transaksi_list = load_transaksi()
    user = User("Pengguna")
    saldo_reminder = SaldoReminder()
    pengeluaran_reminder = PengeluaranReminder()

    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            if not transaksi_list:
                print("Belum ada transaksi.")
            else:
                for i, t in enumerate(transaksi_list):
                    print(f"{i+1}. {t}")

        elif pilihan == "2":
            judul = input("Judul pemasukan: ")
            jumlah = float(input("Jumlah: "))
            tanggal = input("Tanggal (YYYY-MM-DD): ")
            pemasukan = Pemasukan(judul, jumlah, tanggal)
            transaksi_list.append(pemasukan)
            save_transaksi(transaksi_list)
            print("Pemasukan berhasil ditambahkan.")

        elif pilihan == "3":
            judul = input("Judul pengeluaran: ")
            jumlah = float(input("Jumlah: "))
            tanggal = input("Tanggal (YYYY-MM-DD): ")
            pengeluaran = Pengeluaran(judul, jumlah, tanggal)
            transaksi_list.append(pengeluaran)
            save_transaksi(transaksi_list)
            print("Pengeluaran berhasil ditambahkan.")

        elif pilihan == "4":
            for i, t in enumerate(transaksi_list):
                print(f"{i+1}. {t}")
            idx = int(input("Masukkan nomor yang ingin dihapus: ")) - 1
            if 0 <= idx < len(transaksi_list):
                del transaksi_list[idx]
                save_transaksi(transaksi_list)
                print("Transaksi berhasil dihapus.")
            else:
                print("Nomor tidak valid.")

        elif pilihan == "5":
            saldo_reminder.kirim_pengingat(transaksi_list)
            pengeluaran_reminder.kirim_pengingat(transaksi_list)

        elif pilihan == "0":
            print("Terima kasih telah menggunakan MoneyMind!")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
