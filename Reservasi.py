import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# =============================================================================
# BAGIAN 1: STRUKTUR DATA (TIDAK BERUBAH)
# =============================================================================

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
        return True

    def hapus_reservasi_by_node(self, node_to_delete):
        """Menghapus node berdasarkan objek node itu sendiri."""
        if not node_to_delete:
            return False
            
        if node_to_delete.prev:
            node_to_delete.prev.next = node_to_delete.next
        else: # Node adalah head
            self.head = node_to_delete.next

        if node_to_delete.next:
            node_to_delete.next.prev = node_to_delete.prev
        else: # Node adalah tail
            self.tail = node_to_delete.prev
            
        return True
        
    def dapatkan_node_by_id(self, item_id):
        """Mencari node berdasarkan ID unik (dalam kasus GUI, kita gunakan ID dari Treeview)."""
        saat_ini = self.head
        while saat_ini:
            if id(saat_ini) == item_id:
                return saat_ini
            saat_ini = saat_ini.next
        return None


# =============================================================================
# BAGIAN 2: APLIKASI GUI MENGGUNAKAN TKINTER
# =============================================================================

class AplikasiReservasiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Reservasi Restoran")
        self.root.geometry("1000x700")

        # Inisialisasi data
        self.daftar_reservasi_aktif = DaftarReservasi()
        self.reservasi_selesai_list = []  # List untuk menyimpan info reservasi selesai
        
        # Daftar bulan untuk dropdown
        self.daftar_bulan = [
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ]

        # --- Membuat Frame untuk Tata Letak ---
        self.frame_input = ttk.LabelFrame(root, text="Tambah Reservasi", padding=(10, 10))
        self.frame_input.pack(fill="x", padx=10, pady=5)
        
        self.frame_aksi = ttk.Frame(root, padding=(10, 10))
        self.frame_aksi.pack(fill="x", padx=10, pady=5)

        self.frame_aktif = ttk.LabelFrame(root, text="Reservasi Aktif", padding=(10, 10))
        self.frame_aktif.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.frame_selesai = ttk.LabelFrame(root, text="Reservasi Selesai", padding=(10, 10))
        self.frame_selesai.pack(fill="both", expand=True, padx=10, pady=5)

        # --- Membuat Widget untuk Input ---
        self.buat_widget_input()
        
        # --- Membuat Tombol Aksi ---
        self.buat_widget_aksi()

        # --- Membuat Tabel (TreeView) ---
        self.buat_tabel_reservasi()

        # Inisialisasi tampilan tabel
        self.perbarui_tabel_reservasi()
        
    def buat_widget_input(self):
        # Baris 1: Nama & Telepon
        ttk.Label(self.frame_input, text="Nama:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nama = ttk.Entry(self.frame_input, width=30)
        self.entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.frame_input, text="No. Telepon:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_telepon = ttk.Entry(self.frame_input, width=20)
        self.entry_telepon.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Baris 2: Tamu, Tanggal, Waktu
        ttk.Label(self.frame_input, text="Jumlah Tamu:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_tamu = ttk.Entry(self.frame_input, width=10)
        self.entry_tamu.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(self.frame_input, text="Tanggal:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.date_frame = ttk.Frame(self.frame_input)
        self.date_frame.grid(row=1, column=3, sticky="w")
        
        current_year = datetime.datetime.now().year
        self.spin_hari = ttk.Spinbox(self.date_frame, from_=1, to=31, width=4)
        self.spin_hari.pack(side="left", padx=2)
        self.combo_bulan = ttk.Combobox(self.date_frame, values=self.daftar_bulan, width=12, state="readonly")
        self.combo_bulan.pack(side="left", padx=2)
        self.spin_tahun = ttk.Spinbox(self.date_frame, from_=current_year, to=current_year + 10, width=6)
        self.spin_tahun.pack(side="left", padx=2)
        
        self.spin_hari.set(datetime.datetime.now().day)
        self.combo_bulan.current(datetime.datetime.now().month - 1)
        self.spin_tahun.set(current_year)

        ttk.Label(self.frame_input, text="Waktu (HH:MM):").grid(row=1, column=4, padx=5, pady=5, sticky="w")
        self.entry_waktu = ttk.Entry(self.frame_input, width=10)
        self.entry_waktu.grid(row=1, column=5, padx=5, pady=5, sticky="w")
        self.entry_waktu.insert(0, "10:00")
        
    def buat_widget_aksi(self):
        self.btn_tambah = ttk.Button(self.frame_aksi, text="Tambah Reservasi", command=self.tambah_reservasi)
        self.btn_tambah.pack(side="left", padx=5)

        self.btn_edit = ttk.Button(self.frame_aksi, text="Edit Terpilih", command=self.buka_jendela_edit)
        self.btn_edit.pack(side="left", padx=5)

        self.btn_hapus = ttk.Button(self.frame_aksi, text="Hapus Terpilih", command=self.hapus_reservasi)
        self.btn_hapus.pack(side="left", padx=5)
        
        self.btn_selesai = ttk.Button(self.frame_aksi, text="Tandai Selesai", command=self.tandai_selesai)
        self.btn_selesai.pack(side="left", padx=5)
        
        self.btn_clear = ttk.Button(self.frame_aksi, text="Bersihkan Input", command=self.bersihkan_input)
        self.btn_clear.pack(side="left", padx=5)

    def buat_tabel_reservasi(self):
        # Tabel Reservasi Aktif
        columns = ('nama', 'telepon', 'tamu', 'tanggal', 'waktu')
        self.tree_aktif = ttk.Treeview(self.frame_aktif, columns=columns, show='headings')
        
        self.tree_aktif.heading('nama', text='Nama Pelanggan')
        self.tree_aktif.heading('telepon', text='No. Telepon')
        self.tree_aktif.heading('tamu', text='Tamu')
        self.tree_aktif.heading('tanggal', text='Tanggal')
        self.tree_aktif.heading('waktu', text='Waktu')

        self.tree_aktif.column('nama', width=200)
        self.tree_aktif.column('telepon', width=120)
        self.tree_aktif.column('tamu', width=50, anchor="center")
        self.tree_aktif.column('tanggal', width=180)
        self.tree_aktif.column('waktu', width=80, anchor="center")
        
        # Tambah scrollbar
        scrollbar_aktif = ttk.Scrollbar(self.frame_aktif, orient="vertical", command=self.tree_aktif.yview)
        self.tree_aktif.configure(yscroll=scrollbar_aktif.set)
        scrollbar_aktif.pack(side="right", fill="y")
        self.tree_aktif.pack(fill="both", expand=True)

        # Tabel Reservasi Selesai
        self.tree_selesai = ttk.Treeview(self.frame_selesai, columns=columns, show='headings')

        self.tree_selesai.heading('nama', text='Nama Pelanggan')
        self.tree_selesai.heading('telepon', text='No. Telepon')
        self.tree_selesai.heading('tamu', text='Tamu')
        self.tree_selesai.heading('tanggal', text='Tanggal')
        self.tree_selesai.heading('waktu', text='Waktu')
        
        # Tambah scrollbar
        scrollbar_selesai = ttk.Scrollbar(self.frame_selesai, orient="vertical", command=self.tree_selesai.yview)
        self.tree_selesai.configure(yscroll=scrollbar_selesai.set)
        scrollbar_selesai.pack(side="right", fill="y")
        self.tree_selesai.pack(fill="both", expand=True)

    def perbarui_tabel_reservasi(self):
        # Hapus data lama di kedua tabel
        for item in self.tree_aktif.get_children():
            self.tree_aktif.delete(item)
        for item in self.tree_selesai.get_children():
            self.tree_selesai.delete(item)

        # Isi tabel aktif dari linked list
        current = self.daftar_reservasi_aktif.head
        while current:
            item_id = id(current) 
            values = (current.nama, current.telepon, current.tamu, current.tanggal, current.waktu)
            self.tree_aktif.insert('', 'end', iid=item_id, values=values)
            current = current.next
            
        # Isi tabel selesai dari list
        for data in self.reservasi_selesai_list:
            values = (data['nama'], data['telepon'], data['tamu'], data['tanggal'], data['waktu'])
            self.tree_selesai.insert('', 'end', values=values)

    def validasi_input(self, nama, telepon, tamu, waktu, parent_window=None):
        if not all([nama.strip(), telepon.strip(), tamu.strip(), waktu.strip()]):
            messagebox.showerror("Input Error", "Semua kolom harus diisi.", parent=parent_window)
            return False
        if not telepon.isdigit() or len(telepon) > 13:
            messagebox.showerror("Input Error", "Nomor telepon harus angka dan maksimal 13 digit.", parent=parent_window)
            return False
        if not tamu.isdigit():
            messagebox.showerror("Input Error", "Jumlah tamu harus angka.", parent=parent_window)
            return False
        try:
            jam, menit = map(int, waktu.split(':'))
            if not (10 <= jam <= 21 and 0 <= menit <= 59):
                raise ValueError()
        except ValueError:
            messagebox.showerror("Input Error", "Format waktu salah atau di luar jam operasional (10:00 - 21:00).", parent=parent_window)
            return False
        return True

    def tambah_reservasi(self):
        nama = self.entry_nama.get()
        telepon = self.entry_telepon.get()
        tamu = self.entry_tamu.get()
        waktu = self.entry_waktu.get()
        
        tanggal_lengkap = f"{self.spin_hari.get()} {self.combo_bulan.get()} {self.spin_tahun.get()}"
        
        if not self.validasi_input(nama, telepon, tamu, waktu):
            return

        self.daftar_reservasi_aktif.tambah_reservasi(nama, telepon, tamu, waktu, tanggal_lengkap)
        messagebox.showinfo("Sukses", f"Reservasi untuk '{nama}' berhasil ditambahkan.")
        self.perbarui_tabel_reservasi()
        self.bersihkan_input()
        
    def bersihkan_input(self):
        self.entry_nama.delete(0, 'end')
        self.entry_telepon.delete(0, 'end')
        self.entry_tamu.delete(0, 'end')
        self.entry_waktu.delete(0, 'end')
        self.entry_waktu.insert(0, "10:00")
        self.entry_nama.focus()

    def buka_jendela_edit(self):
        selected_item_id = self.tree_aktif.focus()
        if not selected_item_id:
            messagebox.showwarning("Peringatan", "Pilih reservasi yang ingin diedit terlebih dahulu.")
            return
        
        node_to_edit = self.daftar_reservasi_aktif.dapatkan_node_by_id(int(selected_item_id))
        if not node_to_edit:
            messagebox.showerror("Error", "Data reservasi tidak ditemukan.")
            return

        # --- PERUBAHAN DIMULAI DI SINI ---
        
        # Membuat jendela Toplevel baru untuk edit
        win_edit = tk.Toplevel(self.root)
        win_edit.title("Edit Reservasi")
        win_edit.geometry("450x300")
        win_edit.resizable(False, False)

        # Frame utama di dalam jendela edit
        main_frame = ttk.Frame(win_edit, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Widget di jendela edit
        ttk.Label(main_frame, text="Nama:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        edit_nama = ttk.Entry(main_frame, width=30)
        edit_nama.grid(row=0, column=1, padx=10, pady=5)
        edit_nama.insert(0, node_to_edit.nama)

        ttk.Label(main_frame, text="Telepon:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        edit_telepon = ttk.Entry(main_frame, width=30)
        edit_telepon.grid(row=1, column=1, padx=10, pady=5)
        edit_telepon.insert(0, node_to_edit.telepon)

        ttk.Label(main_frame, text="Tamu:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        edit_tamu = ttk.Entry(main_frame, width=30)
        edit_tamu.grid(row=2, column=1, padx=10, pady=5)
        edit_tamu.insert(0, node_to_edit.tamu)

        ttk.Label(main_frame, text="Waktu:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        edit_waktu = ttk.Entry(main_frame, width=30)
        edit_waktu.grid(row=3, column=1, padx=10, pady=5)
        edit_waktu.insert(0, node_to_edit.waktu)

        # Widget untuk mengedit tanggal
        ttk.Label(main_frame, text="Tanggal:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        edit_date_frame = ttk.Frame(main_frame)
        edit_date_frame.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        current_year = datetime.datetime.now().year
        edit_spin_hari = ttk.Spinbox(edit_date_frame, from_=1, to=31, width=4)
        edit_spin_hari.pack(side="left", padx=2)
        edit_combo_bulan = ttk.Combobox(edit_date_frame, values=self.daftar_bulan, width=12, state="readonly")
        edit_combo_bulan.pack(side="left", padx=2)
        edit_spin_tahun = ttk.Spinbox(edit_date_frame, from_=current_year, to=current_year + 10, width=6)
        edit_spin_tahun.pack(side="left", padx=2)
        
        # Parse dan atur tanggal yang ada
        try:
            hari_lama, bulan_lama, tahun_lama = node_to_edit.tanggal.split()
            edit_spin_hari.set(hari_lama)
            edit_combo_bulan.set(bulan_lama)
            edit_spin_tahun.set(tahun_lama)
        except ValueError:
            # Jika format tanggal salah, gunakan tanggal hari ini sebagai default
            edit_spin_hari.set(datetime.datetime.now().day)
            edit_combo_bulan.current(datetime.datetime.now().month - 1)
            edit_spin_tahun.set(current_year)


        # Fungsi untuk menyimpan perubahan
        def simpan_perubahan():
            nama_baru = edit_nama.get()
            telepon_baru = edit_telepon.get()
            tamu_baru = edit_tamu.get()
            waktu_baru = edit_waktu.get()
            
            # Validasi input, beri tahu messagebox agar muncul di atas jendela edit
            if not self.validasi_input(nama_baru, telepon_baru, tamu_baru, waktu_baru, parent_window=win_edit):
                return
            
            # Ambil data tanggal baru
            tanggal_baru_lengkap = f"{edit_spin_hari.get()} {edit_combo_bulan.get()} {edit_spin_tahun.get()}"
            
            # Update data pada node
            node_to_edit.nama = nama_baru
            node_to_edit.telepon = telepon_baru
            node_to_edit.tamu = tamu_baru
            node_to_edit.waktu = waktu_baru
            node_to_edit.tanggal = tanggal_baru_lengkap
            
            self.perbarui_tabel_reservasi()
            messagebox.showinfo("Sukses", "Data reservasi berhasil diperbarui.", parent=win_edit)
            win_edit.destroy()

        # Tombol Simpan
        btn_simpan = ttk.Button(main_frame, text="Simpan Perubahan", command=simpan_perubahan)
        btn_simpan.grid(row=5, column=0, columnspan=2, pady=20)
        # --- PERUBAHAN SELESAI DI SINI ---

    def hapus_reservasi(self):
        selected_item_id = self.tree_aktif.focus()
        if not selected_item_id:
            messagebox.showwarning("Peringatan", "Pilih reservasi yang ingin dihapus.")
            return

        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus reservasi ini?"):
            node_to_delete = self.daftar_reservasi_aktif.dapatkan_node_by_id(int(selected_item_id))
            if node_to_delete:
                nama_dihapus = node_to_delete.nama
                self.daftar_reservasi_aktif.hapus_reservasi_by_node(node_to_delete)
                self.perbarui_tabel_reservasi()
                messagebox.showinfo("Sukses", f"Reservasi untuk '{nama_dihapus}' telah dihapus.")
            else:
                messagebox.showerror("Error", "Gagal menghapus, data tidak ditemukan.")

    def tandai_selesai(self):
        selected_item_id = self.tree_aktif.focus()
        if not selected_item_id:
            messagebox.showwarning("Peringatan", "Pilih reservasi yang ingin ditandai selesai.")
            return

        node_to_finish = self.daftar_reservasi_aktif.dapatkan_node_by_id(int(selected_item_id))
        if node_to_finish:
            data_selesai = {
                'nama': node_to_finish.nama,
                'telepon': node_to_finish.telepon,
                'tamu': node_to_finish.tamu,
                'tanggal': node_to_finish.tanggal,
                'waktu': node_to_finish.waktu,
            }
            self.reservasi_selesai_list.append(data_selesai)
            
            self.daftar_reservasi_aktif.hapus_reservasi_by_node(node_to_finish)
            
            self.perbarui_tabel_reservasi()
            messagebox.showinfo("Sukses", f"Reservasi untuk '{data_selesai['nama']}' ditandai selesai.")
        else:
            messagebox.showerror("Error", "Gagal menandai selesai, data tidak ditemukan.")


# =============================================================================
# BAGIAN 3: MENJALANKAN APLIKASI
# =============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = AplikasiReservasiGUI(root)
    root.mainloop()