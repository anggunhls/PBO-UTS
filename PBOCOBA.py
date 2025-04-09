from tkinter import * 
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from datetime import datetime

class Produk(ABC):
    def __init__(self, nama, harga, stok):
        self.nama = nama
        self.harga = harga
        self.stok = stok

    @abstractmethod
    def hitungDiskon(self):
        pass

    def info_produk(self):
        return f"{self.nama} | Harga: Rp{self.harga:,} | Stok: {self.stok}"

class Elektronik(Produk):
    def hitungDiskon(self):
        return self.harga * 0.1

class Pakaian(Produk):
    def hitungDiskon(self):
        return self.harga * 0.2

class Makanan(Produk):
    def hitungDiskon(self):
        return self.harga * 0.05

class User:
    def __init__(self, nama, email):
        self.nama = nama
        self.email = email
        self.keranjang = []
        self.riwayat = []

class Admin(User):
    def tambah_produk(self, kategori, nama, harga, stok):
        if kategori == "elektronik":
            return Elektronik(nama, harga, stok)
        elif kategori == "pakaian":
            return Pakaian(nama, harga, stok)
        elif kategori == "makanan":
            return Makanan(nama, harga, stok)

class Pembayaran(ABC):
    @abstractmethod
    def bayar(self, jumlah):
        pass

class Gopay(Pembayaran):
    def bayar(self, jumlah):
        return f"Pembayaran Gopay sebesar Rp{jumlah:,} berhasil"

class TransferBank(Pembayaran):
    def bayar(self, jumlah):
        return f"Pembayaran Transfer Bank sebesar Rp{jumlah:,} berhasil"

class Pesanan:
    def __init__(self, user):
        self.user = user
        self.tanggal = datetime.now()
        self.items = user.keranjang.copy()
        self.total = 0
        self.status = "Diproses"

    def hitung_total(self):
        total = 0
        for item in self.items:
            produk = item['produk']
            total += (produk.harga - produk.hitungDiskon()) * item['jumlah']
        self.total = total
        return total

class EcommerceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Toko Online")
        self.current_user = None
        self.produk_list = []
        self.riwayat_pesanan = []

        self.admin = Admin("Admin Toko", "admin@tokoku.com")

        self.main_frame = Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        self.create_login_screen()

    def create_menu_bar(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        home_menu = Menu(menu_bar, tearoff=0)
        home_menu.add_command(label="Beranda", command=self.create_login_screen)
        home_menu.add_command(label="Keluar", command=self.root.quit)
        menu_bar.add_cascade(label="Menu", menu=home_menu)

        if isinstance(self.current_user, User):
            user_menu = Menu(menu_bar, tearoff=0)
            user_menu.add_command(label="Lihat Keranjang", command=self.show_keranjang)
            user_menu.add_command(label="Riwayat Pembelian", command=self.show_riwayat)
            user_menu.add_command(label="Profil Saya", command=self.show_profil)
            menu_bar.add_cascade(label="Akun Saya", menu=user_menu)

    def create_login_screen(self):
        self.clear_frame()

        Label(self.main_frame, text="Selamat Datang di Toko Online", font=('Arial', 14)).grid(row=0, column=0, pady=10)

        Button(self.main_frame, text="Login sebagai Admin", command=self.create_admin_panel, width=20).grid(row=1, column=0, pady=5)
        Button(self.main_frame, text="Login sebagai User", command=self.create_user_login, width=20).grid(row=2, column=0, pady=5)

    def create_admin_panel(self):
        self.clear_frame()

        Label(self.main_frame, text="Panel Admin", font=('Arial', 12)).grid(row=0, column=0, columnspan=2, pady=10)

        Label(self.main_frame, text="Kategori:").grid(row=1, column=0)
        self.kategori_var = StringVar()
        ttk.Combobox(self.main_frame, textvariable=self.kategori_var, values=["elektronik", "pakaian", "makanan"]).grid(row=1, column=1)

        Label(self.main_frame, text="Nama Produk:").grid(row=2, column=0)
        self.nama_produk = Entry(self.main_frame)
        self.nama_produk.grid(row=2, column=1)

        Label(self.main_frame, text="Harga:").grid(row=3, column=0)
        self.harga_produk = Entry(self.main_frame)
        self.harga_produk.grid(row=3, column=1)

        Label(self.main_frame, text="Stok:").grid(row=4, column=0)
        self.stok_produk = Entry(self.main_frame)
        self.stok_produk.grid(row=4, column=1)

        Button(self.main_frame, text="Tambah Produk", command=self.tambah_produk).grid(row=5, column=0, columnspan=2, pady=10)
        Button(self.main_frame, text="Kembali", command=self.create_login_screen).grid(row=6, column=0, columnspan=2)

    def create_user_login(self):
        self.clear_frame()

        Label(self.main_frame, text="Masukkan Nama Anda:").grid(row=0, column=0)
        self.user_name = Entry(self.main_frame)
        self.user_name.grid(row=0, column=1)

        Label(self.main_frame, text="Email:").grid(row=1, column=0)
        self.user_email = Entry(self.main_frame)
        self.user_email.grid(row=1, column=1)

        Button(self.main_frame, text="Login", command=self.login_user).grid(row=2, column=0, columnspan=2, pady=10)
        Button(self.main_frame, text="Kembali", command=self.create_login_screen).grid(row=3, column=0, columnspan=2)

    def login_user(self):
        name = self.user_name.get()
        email = self.user_email.get()
        if name and email:
            self.current_user = User(name, email)
            self.create_user_dashboard()
            self.create_menu_bar()
        else:
            messagebox.showerror("Error", "Harap isi semua field")

    def create_user_dashboard(self):
        self.clear_frame()

        Label(self.main_frame, text="Cari Produk:").grid(row=0, column=0)
        self.search_var = StringVar()
        Entry(self.main_frame, textvariable=self.search_var).grid(row=0, column=1)
        Button(self.main_frame, text="Cari", command=self.cari_produk).grid(row=0, column=2)
        Button(self.main_frame, text="Kembali", command=self.tampilkan_semua_produk).grid(row=0, column=3)

        Label(self.main_frame, text="Daftar Produk", font=('Arial', 12)).grid(row=1, column=0, columnspan=4)

        columns = ("Nama", "Harga", "Stok", "Kategori")
        self.tree = ttk.Treeview(self.main_frame, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.grid(row=2, column=0, columnspan=4, padx=5, pady=5)

        for produk in self.produk_list:
            self.tree.insert('', 'end', values=(produk.nama, f"Rp{produk.harga:,}", produk.stok, produk.__class__.__name__))

        Label(self.main_frame, text="Jumlah:").grid(row=3, column=0)
        self.jumlah_item = Entry(self.main_frame)
        self.jumlah_item.grid(row=3, column=1)

        Button(self.main_frame, text="Tambah ke Keranjang", command=self.tambah_ke_keranjang).grid(row=3, column=2)
        Button(self.main_frame, text="Lihat Detail Produk", command=self.show_detail_produk).grid(row=3, column=3)

        Button(self.main_frame, text="Lihat Keranjang", command=self.show_keranjang).grid(row=4, column=0, columnspan=4, pady=10)
        Button(self.main_frame, text="Kembali", command=self.create_login_screen).grid(row=5, column=0, columnspan=4)

    def tampilkan_semua_produk(self):
        self.tree.delete(*self.tree.get_children())
        for produk in self.produk_list:
            self.tree.insert('', 'end', values=(produk.nama, f"Rp{produk.harga:,}", produk.stok, produk.__class__.__name__))


    def show_detail_produk(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Pilih produk terlebih dahulu")
            return

        item_data = self.tree.item(selected_item)['values']
        produk = next(p for p in self.produk_list if p.nama == item_data[0])

        diskon = produk.hitungDiskon()
        harga_diskon = produk.harga - diskon

        detail_win = Toplevel(self.root)
        detail_win.title("Detail Produk")

        Label(detail_win, text=f"Nama Produk: {produk.nama}").pack()
        Label(detail_win, text=f"Harga Asli: Rp{produk.harga:,}").pack()
        Label(detail_win, text=f"Diskon: Rp{diskon:,.0f}").pack()
        Label(detail_win, text=f"Harga Setelah Diskon: Rp{harga_diskon:,.0f}").pack()
        Label(detail_win, text=f"Stok: {produk.stok}").pack()
        Label(detail_win, text=f"Kategori: {produk.__class__.__name__}").pack()

    def show_profil(self):
        profil_win = Toplevel(self.root)
        profil_win.title("Profil Pengguna")

        Label(profil_win, text=f"Nama: {self.current_user.nama}").pack(pady=5)
        Label(profil_win, text=f"Email: {self.current_user.email}").pack(pady=5)

    def show_keranjang(self):
        keranjang_window = Toplevel(self.root)
        keranjang_window.title("Keranjang Belanja")

        self.keranjang_tree = ttk.Treeview(keranjang_window, columns=("Nama", "Jumlah", "Subtotal"), show='headings')
        for col in ("Nama", "Jumlah", "Subtotal"):
            self.keranjang_tree.heading(col, text=col)
        self.keranjang_tree.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        total = 0
        for item in self.current_user.keranjang:
            produk = item['produk']
            jumlah = item['jumlah']
            subtotal = (produk.harga - produk.hitungDiskon()) * jumlah
            total += subtotal
            self.keranjang_tree.insert('', 'end', values=(produk.nama, jumlah, f"Rp{subtotal:,}"))

        Label(keranjang_window, text=f"Total: Rp{total:,}", font=('Arial', 12, 'bold')).grid(row=1, column=0, columnspan=2)

        Button(keranjang_window, text="Hapus Produk", command=self.hapus_dari_keranjang).grid(row=2, column=0, pady=5)
        Button(keranjang_window, text="Checkout", command=self.checkout_popup).grid(row=2, column=1, pady=5)

    def checkout_popup(self):
        if not self.current_user.keranjang:
            messagebox.showerror("Error", "Keranjang kosong")
            return

        checkout_win = Toplevel(self.root)
        checkout_win.title("Checkout")

        Label(checkout_win, text="Pilih Metode Pembayaran:", font=('Arial', 12)).pack(pady=10)

        self.metode_var = StringVar(value="gopay")
        Radiobutton(checkout_win, text="Gopay", variable=self.metode_var, value="gopay").pack(anchor=W)
        Radiobutton(checkout_win, text="Transfer Bank", variable=self.metode_var, value="bank").pack(anchor=W)

        Button(checkout_win, text="Bayar Sekarang", command=self.proses_checkout).pack(pady=10)

    def proses_checkout(self):
        metode_pilihan = self.metode_var.get()
        if metode_pilihan == "gopay":
            metode = Gopay()
        else:
            metode = TransferBank()

        self.proses_pembayaran(metode)

    def proses_pembayaran(self, metode):
        pesanan = Pesanan(self.current_user)
        total = pesanan.hitung_total()
        result = metode.bayar(total)
        messagebox.showinfo("Pembayaran Berhasil", result)
        self.current_user.riwayat.append(pesanan)
        self.current_user.keranjang.clear()
        self.create_user_dashboard()


    def hapus_dari_keranjang(self):
        selected_item = self.keranjang_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Pilih item yang akan dihapus")
            return

        item_data = self.keranjang_tree.item(selected_item)['values']
        nama_produk = item_data[0]
        self.current_user.keranjang = [item for item in self.current_user.keranjang if item['produk'].nama != nama_produk]
        messagebox.showinfo("Info", f"Produk '{nama_produk}' telah dihapus dari keranjang")
        self.show_keranjang()

    def proses_pembayaran(self, metode):
        pesanan = Pesanan(self.current_user)
        total = pesanan.hitung_total()
        result = metode.bayar(total)
        messagebox.showinfo("Pembayaran Berhasil", result)
        self.current_user.riwayat.append(pesanan)
        self.current_user.keranjang.clear()
        self.create_user_dashboard()

    def show_riwayat(self):
        riwayat_win = Toplevel(self.root)
        riwayat_win.title("Riwayat Pembelian")

        if hasattr(self.current_user, "riwayat") and self.current_user.riwayat:
            for idx, pesanan in enumerate(self.current_user.riwayat):
                Label(riwayat_win, text=f"{pesanan.tanggal.strftime('%d-%m-%Y %H:%M')} | Total: Rp{pesanan.total:,}").grid(row=idx, column=0)
        else:
            Label(riwayat_win, text="Belum ada riwayat pembelian.").grid(row=0, column=0)

    def tambah_produk(self):
        try:
            produk = self.admin.tambah_produk(self.kategori_var.get(), self.nama_produk.get(), int(self.harga_produk.get()), int(self.stok_produk.get()))
            self.produk_list.append(produk)
            messagebox.showinfo("Sukses", "Produk berhasil ditambahkan")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambahkan produk: {str(e)}")

    def tambah_ke_keranjang(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Pilih produk terlebih dahulu")
            return

        item_data = self.tree.item(selected_item)['values']
        produk = next(p for p in self.produk_list if p.nama == item_data[0])

        try:
            jumlah = int(self.jumlah_item.get())
            if produk.stok >= jumlah:
                self.current_user.keranjang.append({'produk': produk, 'jumlah': jumlah})
                produk.stok -= jumlah
                messagebox.showinfo("Sukses", f"{jumlah} {produk.nama} ditambahkan ke keranjang")
                self.create_user_dashboard()
            else:
                messagebox.showerror("Error", "Stok tidak mencukupi")
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus angka")

    def cari_produk(self):
        keyword = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        ditemukan = False
        for produk in self.produk_list:
            if keyword in produk.nama.lower():
                self.tree.insert('', 'end', values=(produk.nama, f"Rp{produk.harga:,}", produk.stok, produk.__class__.__name__))
                ditemukan = True
        if not ditemukan:
            messagebox.showinfo("Info", "Produk tidak ditemukan")

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = Tk()
    app = EcommerceApp(root)
    root.mainloop()