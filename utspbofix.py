from tkinter import * 
from tkinter import ttk, messagebox
from tkinter import font
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
    def __init__(self, username, password, email, alamat, role):
        self.username = username
        self.password = password
        self.email = email
        self.alamat = alamat
        self.role = role
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
    
class QRIS(Pembayaran):
    def bayar(self, jumlah):
        return f"""Pembayaran QRIS sebesar Rp{jumlah:,} berhasil
Scan kode QR berikut:
████████████████
████████████████
████ ▄▄▄▄▄ ██ ▄▄
████ █   █ █▄▄█
████ █▄▄▄█ ████
████▄▄▄▄▄▄▄█▄▄▄
████████████████"""

class COD(Pembayaran):
    def bayar(self, jumlah):
        return f"""Pembayaran COD (Cash on Delivery) sebesar Rp{jumlah:,} berhasil
Silakan siapkan uang tunai saat paket datang"""

class Dana(Pembayaran):
    def bayar(self, jumlah):
        return f"Pembayaran Dana sebesar Rp{jumlah:,} berhasil"

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
        self.root.geometry("800x500")  
        self.root.eval('tk::PlaceWindow . center') 
        self.root.resizable(True, True)  

        self.users = []
        self.current_user = None
        self.produk_list = []
        self.riwayat_pesanan = []
        self.theme = "default"

        self.themes = {
            "default": {"bg": "#F5F5F5", "fg": "#000000"},
            "dark": {"bg": "#2E2E2E", "fg": "#FFFFFF"},
            "blue": {"bg": "#E3F2FD", "fg": "#0D47A1"},
            "green": {"bg": "#E8F5E9", "fg": "#1B5E20"},
            "pink": {"bg": "#FCE4EC", "fg": "#880E4F"}
        }

        self.main_frame = Frame(root, width=800, height=500)
        self.main_frame.pack(padx=10, pady=10)
        self.main_frame.pack_propagate(False)  

        self.create_menu_bar()
        self.create_homepage()
        self.apply_theme()

    def create_menu_bar(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        home_menu = Menu(menu_bar, tearoff=0)
        home_menu.add_command(label="Beranda", command=self.create_homepage)
        home_menu.add_command(label="Keluar", command=self.root.quit)
        menu_bar.add_cascade(label="Menu", menu=home_menu)

        if isinstance(self.current_user, User):
            user_menu = Menu(menu_bar, tearoff=0)
            user_menu.add_command(label="Lihat Keranjang", command=self.show_keranjang)
            user_menu.add_command(label="Riwayat Pembelian", command=self.show_riwayat)
            user_menu.add_command(label="Profil Saya", command=self.show_profil)
            menu_bar.add_cascade(label="Akun Saya", menu=user_menu)

        theme_menu = Menu(menu_bar, tearoff=0)
        for name in self.themes:
            theme_menu.add_command(label=f"Tema: {name.capitalize()}", command=lambda n=name: self.set_theme(n))
        menu_bar.add_cascade(label="Tema", menu=theme_menu)

    def set_theme(self, theme_name):
        self.theme = theme_name
        self.apply_theme()
        
#arya
    def apply_theme(self):
        theme_colors = self.themes.get(self.theme, self.themes["default"])
        bg_color = theme_colors["bg"]
        fg_color = theme_colors["fg"]

        self.root.configure(bg=bg_color)
        self.main_frame.configure(bg=bg_color)

        for widget in self.main_frame.winfo_children():
            try:
                if isinstance(widget, Entry):
                    widget.configure(bg="FFFDD0", fg=fg_color, insertbackground=fg_color)
                elif isinstance(widget, Button):
                    widget.configure(bg="FFFDD0", fg=fg_color)
                elif isinstance(widget, (Label, Frame)):
                    widget.configure(bg=bg_color, fg=fg_color)
            except:
                pass

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                background=bg_color,
                foreground=fg_color,
                rowheight=25,
                fieldbackground=bg_color,
                bordercolor=bg_color)
        style.configure("Treeview.Heading",
                background=bg_color,
                foreground=fg_color)
        style.map("Treeview", 
            background=[('selected', '#6A9FB5')],
            foreground=[('selected', fg_color)])

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def create_homepage(self):
        self.clear_frame()
        self.root.geometry("800x500") 
        self.main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)  

        Label(self.main_frame, text="Selamat Datang\ndi Toko Online!", font=("Helvetica", 16, "bold")).pack(pady=(50, 50))
        Button(self.main_frame, text="Sign Up", width=25, command=self.create_register).pack(pady=5)
        Button(self.main_frame, text="Login", width=25, command=self.create_login).pack(pady=5)
        self.apply_theme()

    def create_register(self):
        self.clear_frame()
        self.root.geometry("300x410")

        Label(self.main_frame, text="Sign Up", font=("Helvetica", 14, "bold")).pack(pady=(10, 25))

        Label(self.main_frame, text="Username:").pack(anchor="w", padx=20, pady=2)
        username = Entry(self.main_frame)
        username.pack(padx=20, fill="x")

        Label(self.main_frame, text="Password:").pack(anchor="w", padx=20, pady=2)
        password = Entry(self.main_frame, show="*")
        password.pack(padx=20, fill="x")

        Label(self.main_frame, text="Email:").pack(anchor="w", padx=20, pady=2)
        email = Entry(self.main_frame)
        email.pack(padx=20, fill="x")

        Label(self.main_frame, text="Alamat:").pack(anchor="w", padx=20, pady=2)
        alamat = Entry(self.main_frame)
        alamat.pack(padx=20, fill="x")

        Label(self.main_frame, text="Role:").pack(anchor="w", padx=20, pady=2)
        role = StringVar()
        ttk.Combobox(self.main_frame, textvariable=role, values=["admin", "customer"]).pack(padx=20, fill="x")

        btn_frame = Frame(self.main_frame)
        btn_frame.pack(pady=(40, 30), padx=40, fill="x")

        Button(btn_frame, text="Sign Up", command=lambda: self.register_user(username.get(), password.get(), email.get(), alamat.get(), role.get())).pack(side="right")
        Button(btn_frame, text="Kembali", command=self.create_homepage).pack(side="left")
        self.apply_theme()

    def register_user(self, username, password, email, alamat, role):
        if username and password and email and alamat:
            if role == "admin":
                self.users.append(Admin(username, password, email, alamat, role))
            else:
                self.users.append(User(username, password, email, alamat, role))

            messagebox.showinfo("Sukses", "Registrasi berhasil! Silakan login.")
            self.create_login()
        else:
            messagebox.showerror("Error", "Semua field wajib diisi!")

    def create_login(self):
        self.clear_frame()
        self.root.geometry("300x350")

        Label(self.main_frame, text="Login", font=("Helvetica", 14, "bold")).pack(pady=(40, 25))

        Label(self.main_frame, text="Username:").pack(anchor="w", padx=20, pady=2)
        username = Entry(self.main_frame)
        username.pack(padx=20, fill="x")

        Label(self.main_frame, text="Password:").pack(anchor="w", padx=20, pady=2)
        password = Entry(self.main_frame, show="*")
        password.pack(padx=20, fill="x")

        btn_frame = Frame(self.main_frame)
        btn_frame.pack(pady=(40, 30), padx=20, fill="x")

        Button(btn_frame, text="Kembali", width=10, command=self.create_homepage).pack(side="left")
        Button(btn_frame, text="Login", width=10, command=lambda: self.login_user(username.get(), password.get())).pack(side="right")
        self.apply_theme()

    def login_user(self, username, password):
        user = next((u for u in self.users if u.username == username and u.password == password), None)
        if user:
            self.current_user = user
            if user.role == "admin":
                self.create_admin_panel()
            else:
                self.create_user_dashboard()
                self.create_menu_bar()
        else:
            messagebox.showerror("Error", "Akun tidak ditemukan, belum sign up?")
            self.create_homepage()
#anggun
    def create_admin_panel(self):
        self.clear_frame()
        self.root.geometry("300x350")

        Label(self.main_frame, text="Panel Admin", font=("Helvetica", 16, "bold")).pack(pady=(40, 10))

        form = Frame(self.main_frame)
        form.pack(pady=10)

        Label(form, text="Kategori:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.kategori_var = StringVar()
        ttk.Combobox(form, textvariable=self.kategori_var, values=["elektronik", "pakaian", "makanan"], width=20).grid(row=0, column=1, padx=5)

        Label(form, text="Nama Produk:").grid(row=1, column=0, sticky=W, padx=5, pady=5)
        self.nama_produk = Entry(form)
        self.nama_produk.grid(row=1, column=1, padx=5)

        Label(form, text="Harga:").grid(row=2, column=0, sticky=W, padx=5, pady=5)
        self.harga_produk = Entry(form)
        self.harga_produk.grid(row=2, column=1, padx=5)

        Label(form, text="Stok:").grid(row=3, column=0, sticky=W, padx=5, pady=5)
        self.stok_produk = Entry(form)
        self.stok_produk.grid(row=3, column=1, padx=5)

        Button(self.main_frame, text="Tambah Produk", command=self.tambah_produk).pack(pady=10)
        Button(self.main_frame, text="Kembali", command=self.create_homepage).pack()
        self.apply_theme()

    def create_user_dashboard(self):
        self.clear_frame()
        self.apply_theme()
        self.root.geometry("800x500")

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
        Label(self.main_frame, text="Filter Kategori:").grid(row=5, column=0, pady=(10, 0))
        self.filter_kategori = StringVar()
        ttk.Combobox(self.main_frame, textvariable=self.filter_kategori, values=["semua", "elektronik", "pakaian", "makanan"]).grid(row=5, column=1, pady=(10, 0))

        Label(self.main_frame, text="Sortir Berdasarkan:").grid(row=6, column=0)
        self.sort_by = StringVar()
        ttk.Combobox(self.main_frame, textvariable=self.sort_by, values=["harga_terendah", "harga_tertinggi", "stok_terbanyak", "stok_tersedikit"]).grid(row=6, column=1)

        Button(self.main_frame, text="Terapkan Filter", command=self.terapkan_filter).grid(row=6, column=2, padx=10,pady=(5,10))
        Button(self.main_frame, text="Kembali", command=self.create_homepage).grid(row=5, column=0, columnspan=4)
        self.apply_theme()

    def terapkan_filter(self):
        kategori = self.filter_kategori.get()
        sort = self.sort_by.get()

        produk_terfilter = self.produk_list

        if kategori and kategori != "semua":
            produk_terfilter = [p for p in produk_terfilter if p.__class__.__name__.lower() == kategori.lower()]

        if sort == "harga_terendah":
            produk_terfilter.sort(key=lambda x: x.harga)
        elif sort == "harga_tertinggi":
            produk_terfilter.sort(key=lambda x: x.harga, reverse=True)
        elif sort == "stok_terbanyak":
            produk_terfilter.sort(key=lambda x: x.stok, reverse=True)
        elif sort == "stok_tersedikit":
            produk_terfilter.sort(key=lambda x: x.stok)

        self.tree.delete(*self.tree.get_children())
        for produk in produk_terfilter:
            self.tree.insert('', 'end', values=(produk.nama, f"Rp{produk.harga:,}", produk.stok, produk.__class__.__name__))

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

        Label(profil_win, text=f"Usename: {self.current_user.username}").pack(pady=5)
        Label(profil_win, text=f"Password: {self.current_user.password}").pack(pady=5)
        Label(profil_win, text=f"Email: {self.current_user.email}").pack(pady=5)
        Label(profil_win, text=f"Alamat: {self.current_user.alamat}").pack(pady=5)

    def show_keranjang(self):
        keranjang_window = Toplevel(self.root)
        keranjang_window.title("Keranjang Belanja")

        self.keranjang_tree = ttk.Treeview(keranjang_window, columns=("Nama", "Harga satuan", "Jumlah", "Subtotal"), show='headings')
        for col in ("Nama","Harga satuan", "Jumlah", "Subtotal"):
            self.keranjang_tree.heading(col, text=col)
        self.keranjang_tree.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        total = 0
        for item in self.current_user.keranjang:
            produk = item['produk']
            jumlah = item['jumlah']
            harga_diskon = produk.harga - produk.hitungDiskon()
            subtotal = harga_diskon * jumlah
            total += subtotal
            self.keranjang_tree.insert('', 'end', values=(
               produk.nama,
               f"Rp{harga_diskon:,}",
               jumlah,
               f"Rp{subtotal:,}"))

        Label(keranjang_window, text=f"Total: Rp{total:,}", font=('Arial', 12, 'bold')).grid(row=1, column=0, columnspan=2)

        Button(keranjang_window, text="Hapus Produk", command=self.hapus_dari_keranjang).grid(row=2, column=0, pady=5)
        Button(keranjang_window, text="Checkout", command=self.checkout_popup).grid(row=2, column=1, pady=5)
        self.apply_theme()
#erica
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
        Radiobutton(checkout_win, text="QRIS", variable=self.metode_var, value="qris").pack(anchor=W)
        Radiobutton(checkout_win, text="COD", variable=self.metode_var, value="cod").pack(anchor=W)
        Radiobutton(checkout_win, text="Dana", variable=self.metode_var, value="dana").pack(anchor=W)
        Button(checkout_win, text="Bayar Sekarang", command=self.proses_checkout).pack(pady=10)

    def proses_checkout(self):
        metode_pilihan = self.metode_var.get()
        if metode_pilihan == "gopay":
            metode = Gopay()
        elif metode_pilihan == "bank":
            metode = TransferBank()
        elif metode_pilihan == "qris":
            metode = QRIS()
        elif metode_pilihan == "cod":
            metode = COD()
        elif metode_pilihan == "dana":
            metode = Dana()
        else:
            messagebox.showerror("Error", "Metode pembayaran tidak valid")
            return

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
            produk = self.current_user.tambah_produk(self.kategori_var.get(), self.nama_produk.get(), int(self.harga_produk.get()), int(self.stok_produk.get()))
            self.produk_list.append(produk)
            messagebox.showinfo("Sukses", "Produk berhasil ditambahkan")
            self.create_admin_panel()
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