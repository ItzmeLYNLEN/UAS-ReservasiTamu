import tkinter as tk
from tkinter import messagebox, ttk

# Node untuk Doubly Linked List
class NodeReservasi:
    def __init__(self, nama, telepon, tamu, waktu, tanggal): # nama fungsi __init__ adalah standar Python, sebaiknya tidak diubah
        self.nama = nama
        self.telepon = telepon
        self.tamu = tamu
        self.waktu = waktu
        self.tanggal = tanggal
        self.prev = None
        self.next = None

# Struktur Doubly Linked List
class DaftarReservasi:
    def __init__(self): # nama fungsi __init__ adalah standar Python, sebaiknya tidak diubah
        self.head = None
        self.tail = None

    def tambah_reservasi(self, nama, telepon, tamu, waktu, tanggal):
        node_baru = NodeReservasi(nama, telepon, tamu, waktu, tanggal)
        if not self.head:
            self.head = self.tail = node_baru
        else:
            self.tail.next = node_baru
            node_baru.prev = self.tail
            self.tail = node_baru

    def hapus_reservasi(self, nama):
        saat_ini = self.head
        while saat_ini:
            if saat_ini.nama == nama:
                if saat_ini.prev:
                    saat_ini.prev.next = saat_ini.next
                else:
                    self.head = saat_ini.next
                if saat_ini.next:
                    saat_ini.next.prev = saat_ini.prev
                else:
                    self.tail = saat_ini.prev
                return True
            saat_ini = saat_ini.next
        return False

    def dapatkan_semua_reservasi(self):
        list_reservasi = []
        saat_ini = self.head
        while saat_ini:
            list_reservasi.append(f"{saat_ini.nama} | {saat_ini.telepon} | {saat_ini.tamu} | {saat_ini.tanggal} {saat_ini.waktu}")
            saat_ini = saat_ini.next
        return list_reservasi

# GUI Utama
class AplikasiReservasiRestoran:
    def __init__(self, root): # nama fungsi __init__ adalah standar Python, sebaiknya tidak diubah
        self.root = root
        self.root.title("Reservasi Restoran")
        self.daftar_reservasi_internal = DaftarReservasi() # Mengubah nama variabel agar konsisten
        self.reservasi_selesai_list = [] # Mengubah nama variabel agar konsisten

        # Label dan Entry
        tk.Label(root, text="Nama").grid(row=0, column=0, sticky="w")
        tk.Label(root, text="No. Telepon").grid(row=1, column=0, sticky="w")
        tk.Label(root, text="Jumlah Tamu").grid(row=2, column=0, sticky="w")
        tk.Label(root, text="Tanggal").grid(row=3, column=0, sticky="w")
        tk.Label(root, text="Bulan").grid(row=4, column=0, sticky="w")
        tk.Label(root, text="Tahun").grid(row=5, column=0, sticky="w")
        tk.Label(root, text="Waktu Reservasi").grid(row=6, column=0, sticky="w")

        self.isian_nama = tk.Entry(root)
        vcmd = (root.register(self.validasi_numerik), '%P')
        self.isian_telepon = tk.Entry(root, validate="key", validatecommand=vcmd)
        self.isian_tamu = tk.Entry(root, validate="key", validatecommand=vcmd)

        self.isian_nama.grid(row=0, column=1, padx=5, pady=2)
        self.isian_telepon.grid(row=1, column=1, padx=5, pady=2)
        self.isian_tamu.grid(row=2, column=1, padx=5, pady=2)

        self.isian_hari = ttk.Combobox(root, values=[str(i) for i in range(1, 32)], state="readonly", width=17)
        self.isian_bulan = ttk.Combobox(root, values=[
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ], state="readonly", width=17)
        self.isian_tahun = ttk.Combobox(root, values=[str(i) for i in range(2024, 2031)], state="readonly", width=17)

        self.isian_hari.grid(row=3, column=1, padx=5, pady=2)
        self.isian_bulan.grid(row=4, column=1, padx=5, pady=2)
        self.isian_tahun.grid(row=5, column=1, padx=5, pady=2)

        self.isian_hari.set("Pilih tanggal")
        self.isian_bulan.set("Pilih bulan")
        self.isian_tahun.set("Pilih tahun")

        self.opsi_waktu = [f"{i:02}:00" for i in range(10, 23)]
        self.isian_waktu = ttk.Combobox(root, values=self.opsi_waktu, state="readonly", width=17) # Lebar disamakan
        self.isian_waktu.grid(row=6, column=1, padx=5, pady=2)
        self.isian_waktu.set("Pilih waktu")

        # Tombol-tombol
        tk.Button(root, text="Tambah Reservasi", command=self.proses_tambah_reservasi).grid(row=7, column=0, pady=5)
        tk.Button(root, text="Hapus Reservasi", command=self.proses_hapus_reservasi).grid(row=7, column=1, pady=5)
        tk.Button(root, text="Tampilkan Semua", command=self.tampilkan_reservasi_aktif).grid(row=8, column=0, pady=5) # Nama fungsi diubah
        tk.Button(root, text="Selesai", command=self.tandai_sebagai_selesai).grid(row=8, column=1, pady=5)

        # Listbox Reservasi Aktif
        tk.Label(root, text="Reservasi Aktif").grid(row=9, column=0, columnspan=2)
        self.listbox_reservasi_aktif = tk.Listbox(root, width=60)
        self.listbox_reservasi_aktif.grid(row=10, column=0, columnspan=2, pady=5)

        # Listbox Reservasi Selesai
        tk.Label(root, text="Reservasi Selesai").grid(row=11, column=0, columnspan=2)
        self.listbox_reservasi_selesai = tk.Listbox(root, width=60)
        self.listbox_reservasi_selesai.grid(row=12, column=0, columnspan=2, pady=5)

        self.tampilkan_reservasi_aktif() # Memanggil untuk pertama kali jika ada data awal (opsional)
        self.tampilkan_reservasi_yang_selesai() # Memanggil untuk pertama kali

    def validasi_numerik(self, nilai):
        return (nilai.isdigit() or nilai == "") and len(nilai) <= 13

    def proses_tambah_reservasi(self): # Nama fungsi diubah
        nama = self.isian_nama.get()
        telepon = self.isian_telepon.get()
        tamu = self.isian_tamu.get()
        hari = self.isian_hari.get()
        bulan = self.isian_bulan.get()
        tahun = self.isian_tahun.get()
        waktu = self.isian_waktu.get()

        if not nama or not telepon or not tamu or waktu == "Pilih waktu" or \
           hari == "Pilih tanggal" or bulan == "Pilih bulan" or tahun == "Pilih tahun":
            messagebox.showwarning("Peringatan", "Semua data harus diisi!")
            return

        tanggal_lengkap = f"{hari} {bulan} {tahun}"
        self.daftar_reservasi_internal.tambah_reservasi(nama, telepon, tamu, waktu, tanggal_lengkap)
        self.bersihkan_isian()
        self.tampilkan_reservasi_aktif()

    def proses_hapus_reservasi(self): # Nama fungsi diubah
        pilihan = self.listbox_reservasi_aktif.curselection()
        if not pilihan:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus.")
            return
        teks_terpilih = self.listbox_reservasi_aktif.get(pilihan[0])
        nama = teks_terpilih.split(" | ")[0]
        sukses = self.daftar_reservasi_internal.hapus_reservasi(nama)
        if sukses:
            self.tampilkan_reservasi_aktif()
        else:
            messagebox.showerror("Gagal", "Reservasi tidak ditemukan.")

    def tandai_sebagai_selesai(self):
        pilihan = self.listbox_reservasi_aktif.curselection()
        if not pilihan:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin diselesaikan.")
            return
        teks_terpilih = self.listbox_reservasi_aktif.get(pilihan[0])
        nama = teks_terpilih.split(" | ")[0]
        sukses = self.daftar_reservasi_internal.hapus_reservasi(nama) # Hapus dari daftar aktif
        if sukses:
            self.reservasi_selesai_list.append(teks_terpilih) # Tambah ke daftar selesai
            self.tampilkan_reservasi_aktif()
            self.tampilkan_reservasi_yang_selesai()
        else:
            messagebox.showerror("Gagal", "Reservasi tidak ditemukan di daftar aktif.")

    def tampilkan_reservasi_aktif(self): # Nama fungsi diubah
        self.listbox_reservasi_aktif.delete(0, tk.END)
        semua_reservasi = self.daftar_reservasi_internal.dapatkan_semua_reservasi()
        for res in semua_reservasi:
            self.listbox_reservasi_aktif.insert(tk.END, res)

    def tampilkan_reservasi_yang_selesai(self): # Nama fungsi diubah
        self.listbox_reservasi_selesai.delete(0, tk.END)
        for res in self.reservasi_selesai_list:
            self.listbox_reservasi_selesai.insert(tk.END, res)

    def bersihkan_isian(self): # Nama fungsi diubah
        self.isian_nama.delete(0, tk.END)
        self.isian_telepon.delete(0, tk.END)
        self.isian_tamu.delete(0, tk.END)
        self.isian_hari.set("Pilih tanggal")
        self.isian_bulan.set("Pilih bulan")
        self.isian_tahun.set("Pilih tahun")
        self.isian_waktu.set("Pilih waktu")

# Menjalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiReservasiRestoran(root)
    root.mainloop()