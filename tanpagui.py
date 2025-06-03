import datetime

# Node untuk Doubly Linked List
class NodeReservasi:
    def __init__(self, nama, telepon, tamu, waktu, tanggal):
        self.nama = nama
        self.telepon = telepon
        self.tamu = tamu
        self.waktu = waktu
        self.tanggal = tanggal
        self.prev = None
        self.next = None

# Struktur Doubly Linked List
class DaftarReservasi:
    def __init__(self):
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
        return True # Indikasi sukses

    def hapus_reservasi_by_name(self, nama):
        saat_ini = self.head
        while saat_ini:
            if saat_ini.nama.lower() == nama.lower(): # Pencarian case-insensitive
                if saat_ini.prev:
                    saat_ini.prev.next = saat_ini.next
                else:
                    self.head = saat_ini.next
                if saat_ini.next:
                    saat_ini.next.prev = saat_ini.prev
                else:
                    self.tail = saat_ini.prev
                return saat_ini # Mengembalikan node yang dihapus untuk dipindahkan
            saat_ini = saat_ini.next
        return None # Tidak ditemukan

    def dapatkan_semua_reservasi(self):
        list_reservasi = []
        saat_ini = self.head
        index = 1
        while saat_ini:
            list_reservasi.append(
                f"{index}. {saat_ini.nama} | {saat_ini.telepon} | {saat_ini.tamu} tamu | {saat_ini.tanggal} {saat_ini.waktu}"
            )
            saat_ini = saat_ini.next
            index += 1
        return list_reservasi

    def dapatkan_reservasi_by_index(self, index_cari):
        saat_ini = self.head
        current_index = 1
        while saat_ini:
            if current_index == index_cari:
                return saat_ini
            saat_ini = saat_ini.next
            current_index += 1
        return None


# Aplikasi Reservasi Restoran CLI
class AplikasiReservasiRestoranCLI:
    def __init__(self):
        self.daftar_reservasi_aktif = DaftarReservasi()
        self.reservasi_selesai_list = [] # List untuk menyimpan reservasi yang selesai (sebagai string)

    # --- PERUBAHAN: Penambahan allow_empty pada validasi numerik ---
    def validasi_numerik(self, prompt, max_len=None, allow_empty=False):
        while True:
            nilai = input(prompt)
            if allow_empty and not nilai.strip():
                return "" # Kembalikan string kosong jika diizinkan dan input kosong
            if nilai.isdigit():
                if max_len is None or len(nilai) <= max_len:
                    return nilai
                else:
                    print(f"Input tidak boleh lebih dari {max_len} digit.")
            else:
                print("Input harus berupa angka.")

    def validasi_tidak_kosong(self, prompt):
        while True:
            nilai = input(prompt)
            if nilai.strip(): # .strip() untuk menghapus spasi di awal/akhir
                return nilai
            elif nilai == "" and "(kosongkan" in prompt: # Memungkinkan input kosong untuk edit
                 return ""
            else:
                print("Input tidak boleh kosong.")
    
    def validasi_waktu(self, prompt, allow_empty=False):
        while True:
            waktu_str = input(prompt)
            if allow_empty and not waktu_str.strip():
                return "" # Kembalikan string kosong jika diizinkan dan input kosong

            try:
                if len(waktu_str) != 5 or waktu_str[2] != ':':
                    raise ValueError("Format harus HH:MM (contoh: 14:30).")

                jam, menit = map(int, waktu_str.split(':'))
                waktu_input = datetime.time(jam, menit)
                waktu_mulai = datetime.time(10, 0)
                waktu_selesai = datetime.time(21, 0)

                if waktu_mulai <= waktu_input <= waktu_selesai:
                    return waktu_str
                else:
                    print("Waktu harus di antara 10:00 dan 21:00.")
            except ValueError as e:
                print(f"Input waktu tidak valid. {e}")

    def proses_tambah_reservasi(self):
        print("\n--- Tambah Reservasi Baru ---")
        nama = self.validasi_tidak_kosong("Nama Pelanggan: ")
        telepon = self.validasi_numerik("No. Telepon (maks 13 digit): ", 13)
        tamu = self.validasi_numerik("Jumlah Tamu: ")

        print("Masukkan Tanggal Reservasi:")
        while True:
            try:
                hari = int(self.validasi_numerik("Tanggal (1-31): "))
                if 1 <= hari <= 31:
                    break
                else:
                    print("Tanggal tidak valid.")
            except ValueError:
                print("Masukkan angka untuk tanggal.")

        daftar_bulan = [
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ]
        print("Pilih Bulan:")
        for i, nama_bulan in enumerate(daftar_bulan):
            print(f"{i+1}. {nama_bulan}")
        while True:
            try:
                pilihan_bulan = int(input("Pilihan Bulan (nomor): "))
                if 1 <= pilihan_bulan <= 12:
                    bulan = daftar_bulan[pilihan_bulan-1]
                    break
                else:
                    print("Pilihan bulan tidak valid.")
            except ValueError:
                print("Masukkan nomor pilihan bulan.")

        while True:
            try:
                tahun = int(self.validasi_numerik("Tahun (contoh: 2025): "))
                if 2025 <= tahun <= 2035: # Rentang tahun yang wajar
                    break
                else:
                    print("Tahun tidak valid. Masukkan antara 2025-2035.")
            except ValueError:
                print("Masukkan angka untuk tahun.")

        tanggal_lengkap = f"{hari} {bulan} {tahun}"
        
        waktu = self.validasi_waktu("Masukkan Waktu Reservasi (HH:MM, dari 10:00 - 21:00): ")

        if self.daftar_reservasi_aktif.tambah_reservasi(nama, telepon, tamu, waktu, tanggal_lengkap):
            print(f"Reservasi untuk '{nama}' berhasil ditambahkan.")
        else:
            print(f"Gagal menambahkan reservasi untuk '{nama}'.")

    # --- PERUBAHAN: Metode ini dimodifikasi secara signifikan ---
    def proses_edit_reservasi(self):
        print("\n--- Edit Reservasi ---")
        node_untuk_diedit = self.pilih_reservasi_untuk_aksi("diedit")

        if node_untuk_diedit:
            print(f"\nMengedit data untuk: {node_untuk_diedit.nama}")
            print("Kosongkan input jika tidak ingin mengubah data tersebut.")

            # Edit Nama
            nama_baru = self.validasi_tidak_kosong(f"Nama Pelanggan [{node_untuk_diedit.nama}]: ")
            if nama_baru:
                node_untuk_diedit.nama = nama_baru

            # Edit Telepon (menggunakan allow_empty=True)
            telepon_baru = self.validasi_numerik(f"No. Telepon [{node_untuk_diedit.telepon}]: ", max_len=13, allow_empty=True)
            if telepon_baru:
                node_untuk_diedit.telepon = telepon_baru

            # Edit Jumlah Tamu (menggunakan allow_empty=True)
            tamu_baru = self.validasi_numerik(f"Jumlah Tamu [{node_untuk_diedit.tamu}]: ", allow_empty=True)
            if tamu_baru:
                node_untuk_diedit.tamu = tamu_baru
            
            # Edit Waktu
            waktu_baru = self.validasi_waktu(f"Waktu (HH:MM) [{node_untuk_diedit.waktu}]: ", allow_empty=True)
            if waktu_baru:
                node_untuk_diedit.waktu = waktu_baru
            
            # --- BAGIAN BARU: EDIT TANGGAL, BULAN, TAHUN ---
            print(f"\nTanggal saat ini: {node_untuk_diedit.tanggal}")
            pilihan_edit_tanggal = input("Apakah Anda ingin mengubah tanggal (y/n)? ").lower()
            if pilihan_edit_tanggal == 'y':
                # Pecah tanggal lama untuk ditampilkan sebagai default
                hari_lama, bulan_lama, tahun_lama = node_untuk_diedit.tanggal.split()

                # Input Hari Baru
                while True:
                    hari_str = self.validasi_numerik(f"Tanggal baru (1-31) [{hari_lama}]: ", allow_empty=True)
                    if not hari_str: # Jika kosong, gunakan yang lama
                        hari_baru = hari_lama
                        break
                    try:
                        hari_int = int(hari_str)
                        if 1 <= hari_int <= 31:
                            hari_baru = hari_str
                            break
                        else:
                            print("Tanggal tidak valid.")
                    except ValueError: # Seharusnya tidak terjadi karena validasi_numerik
                        print("Input harus angka.")
                
                # Input Bulan Baru
                daftar_bulan = [
                    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
                    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
                ]
                print(f"Bulan saat ini: {bulan_lama}")
                for i, nama_bulan in enumerate(daftar_bulan):
                    print(f"{i+1}. {nama_bulan}")
                
                while True:
                    pilihan_bulan_str = self.validasi_numerik("Pilihan Bulan baru (nomor, kosongkan jika tidak berubah): ", allow_empty=True)
                    if not pilihan_bulan_str:
                        bulan_baru = bulan_lama
                        break
                    try:
                        pilihan_bulan_int = int(pilihan_bulan_str)
                        if 1 <= pilihan_bulan_int <= 12:
                            bulan_baru = daftar_bulan[pilihan_bulan_int - 1]
                            break
                        else:
                            print("Pilihan bulan tidak valid.")
                    except ValueError:
                        print("Masukkan nomor pilihan bulan.")
                
                # Input Tahun Baru
                while True:
                    tahun_str = self.validasi_numerik(f"Tahun baru (contoh: 2025) [{tahun_lama}]: ", allow_empty=True)
                    if not tahun_str:
                        tahun_baru = tahun_lama
                        break
                    try:
                        tahun_int = int(tahun_str)
                        if 2025 <= tahun_int <= 2035:
                            tahun_baru = tahun_str
                            break
                        else:
                            print("Tahun tidak valid. Masukkan antara 2025-2035.")
                    except ValueError:
                        print("Masukkan angka untuk tahun.")
                
                # Gabungkan dan perbarui tanggal
                node_untuk_diedit.tanggal = f"{hari_baru} {bulan_baru} {tahun_baru}"

            print(f"\nReservasi untuk '{node_untuk_diedit.nama}' berhasil diperbarui.")


    def tampilkan_reservasi(self, daftar, judul):
        print(f"\n--- {judul} ---")
        if not daftar:
            print("Tidak ada reservasi.")
            return False
        for res in daftar:
            print(res)
        return True

    def pilih_reservasi_untuk_aksi(self, aksi="diproses"):
        if not self.tampilkan_reservasi(self.daftar_reservasi_aktif.dapatkan_semua_reservasi(), "Reservasi Aktif"):
            return None
        try:
            pilihan_nomor = int(input(f"Masukkan nomor reservasi yang ingin {aksi}: "))
            reservasi_node = self.daftar_reservasi_aktif.dapatkan_reservasi_by_index(pilihan_nomor)
            if reservasi_node:
                return reservasi_node
            else:
                print("Nomor reservasi tidak valid.")
                return None
        except ValueError:
            print("Input tidak valid, masukkan nomor.")
            return None

    def proses_hapus_reservasi(self):
        print("\n--- Hapus Reservasi ---")
        reservasi_node = self.pilih_reservasi_untuk_aksi("dihapus")
        if reservasi_node:
            nama_dihapus = reservasi_node.nama
            if self.daftar_reservasi_aktif.hapus_reservasi_by_name(nama_dihapus):
                print(f"Reservasi untuk '{nama_dihapus}' berhasil dihapus.")
            else:
                # Seharusnya tidak terjadi jika node ditemukan sebelumnya
                print(f"Gagal menghapus reservasi untuk '{nama_dihapus}'. Reservasi tidak ditemukan (kesalahan internal).")


    def tandai_sebagai_selesai(self):
        print("\n--- Tandai Reservasi Selesai ---")
        reservasi_node = self.pilih_reservasi_untuk_aksi("diselesaikan")
        if reservasi_node:
            data_reservasi_selesai = (
                f"{reservasi_node.nama} | {reservasi_node.telepon} | "
                f"{reservasi_node.tamu} tamu | {reservasi_node.tanggal} {reservasi_node.waktu}"
            )
            nama_selesai = reservasi_node.nama # Simpan nama sebelum dihapus
            
            node_yang_dihapus = self.daftar_reservasi_aktif.hapus_reservasi_by_name(reservasi_node.nama)
            if node_yang_dihapus:
                self.reservasi_selesai_list.append(data_reservasi_selesai)
                print(f"Reservasi untuk '{nama_selesai}' telah ditandai selesai.")
            else:
                print(f"Gagal menandai selesai. Reservasi '{nama_selesai}' tidak ditemukan di daftar aktif (kesalahan internal).")

    def jalankan(self):
        while True:
            print("\n===== Menu Reservasi Restoran =====")
            print("1. Tambah Reservasi")
            print("2. Tampilkan Reservasi Aktif")
            print("3. Edit Reservasi")
            print("4. Hapus Reservasi")
            print("5. Tandai Reservasi Selesai")
            print("6. Tampilkan Reservasi Selesai")
            print("7. Keluar")

            pilihan = input("Masukkan pilihan Anda: ")

            if pilihan == '1':
                self.proses_tambah_reservasi()
            elif pilihan == '2':
                self.tampilkan_reservasi(self.daftar_reservasi_aktif.dapatkan_semua_reservasi(), "Reservasi Aktif")
            elif pilihan == '3':
                self.proses_edit_reservasi() # Panggil fungsi edit
            elif pilihan == '4':
                self.proses_hapus_reservasi()
            elif pilihan == '5':
                self.tandai_sebagai_selesai()
            elif pilihan == '6':
                print("\n--- Daftar Reservasi Selesai ---")
                if not self.reservasi_selesai_list:
                    print("Tidak ada reservasi yang selesai.")
                else:
                    for i, res in enumerate(self.reservasi_selesai_list):
                        print(f"{i+1}. {res}")
            elif pilihan == '7':
                print("Terima kasih telah menggunakan aplikasi reservasi. Sampai jumpa!")
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

# Menjalankan aplikasi CLI
if __name__ == "__main__":
    app_cli = AplikasiReservasiRestoranCLI()
    app_cli.jalankan()