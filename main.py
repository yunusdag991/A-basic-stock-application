import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import pandas as pd
import os
import sqlite3


def find_file():
    filename = filedialog.askopenfilename(
        initialdir="/",
        title="Dosya Seç",
        filetypes=(("csv files", "*.csv"),("All Files", "*.*"))
    )
    
    label_file["text"] = filename

    label_file.place(x=15, y=10)

    show_file()

    conn = sqlite3.connect('filename')
    cur = conn.cursor()

    conn.commit()
    conn.close()
    
    return None

def create():
    def save_file():
        path = entry_filename.get()
        if not path.endswith(".csv"):
            path += ".csv"
        filepath = os.path.join(os.getcwd(), path)
        with open(filepath, 'w') as file:
            file.write('Product Name,Product Code,Product Number\n')
        label_file["text"] = filepath
        tk.messagebox.showinfo("Bilgi", f"{path} başarıyla oluşturuldu.")
        top.destroy()
        show_file()

    top = tk.Toplevel(pencere)
    top.title("Dosya Oluştur")
    top.geometry("300x150")

    label_filename = tk.Label(top, text="Dosya Adı:")
    label_filename.pack(pady=10)
    entry_filename = tk.Entry(top, width=25)
    entry_filename.pack(pady=5)

    button_save = tk.Button(top, text="Kaydet", command=save_file)
    button_save.pack(pady=10)


def show_file():
    global path
    path = label_file["text"]
    try:
        name = r"{}".format(path)
        if name[-4:] == ".csv":
            global df
            df = pd.read_csv(name)
        else:
            df = pd.read_excel(name)
    except ValueError:
        tk.messagebox.showerror("Information", "Geçersiz dosya girişi")
    except FileNotFoundError:
        tk.messagebox.showerror("Information", f"Dosya bulunamadı {name}")

    #önceden yazılmış dosyaları sil
    table.delete(*table.get_children())

    table["column"] =list(df.columns)
    table["show"] = "headings"

    for column  in table["column"]:
        table.heading(column , text=column)

    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        table.insert("","end",values=row)

    return None

def kontrol():
    if label_file["text"] == "Hiçbir Dosya Seçili Değil":
        tk.messagebox.showwarning("Uyarı", "Hiçbir dosya seçili değil.")
        return -1
    

def bul():
    if kontrol() == -1:
        return

    def search_product():
        code = entry_code.get()
        result = df[df["Product Code"] == code]
        if not result.empty:
            result_str = result.to_string(index=False)
            tk.messagebox.showinfo("Sonuç", f"Ürün bulundu:\n{result_str}")
        else:
            tk.messagebox.showinfo("Sonuç", "Ürün bulunamadı.")
        top.destroy()

    top = tk.Toplevel(pencere)
    top.title("Ürün Bul")
    top.geometry("300x150")

    label_code = tk.Label(top, text="Ürün kodu giriniz:")
    label_code.pack(pady=10)
    entry_code = tk.Entry(top, width=25)
    entry_code.pack(pady=5)

    button_search = tk.Button(top, text="Ara", command=search_product)
    button_search.pack(pady=10)


def ekle():
    if kontrol() == -1:
        return

    def kaydet():
        product_name = entry_name.get()
        product_code = entry_code.get()
        product_number = entry_num.get()

        global df
        code = entry_code.get()
        result = df[df["Product Code"] == code]

        if not result.empty:
            tk.messagebox.showinfo("Bilgi", "Ürün zaten var.")
            return
         # Başlıkları yalnızca dosya ilk oluşturulduğunda yaz
        if not os.path.exists(path):
            with open(path, 'w') as file:
                file.write('Product Name,Product Code,Product Number\n')
        # Verileri dosyaya ekle
        with open(path, 'a') as file:
            file.write(f'{product_name},{product_code},{product_number}\n')
        
        tk.messagebox.showinfo("Bilgi", "Ürün başarıyla eklendi.")
        show_file()

    top = tk.Toplevel(pencere)
    top.title("Ürün Ekle")
    top.geometry("300x300")

    label_name = tk.Label(top, text="Ürün Adı Giriniz:")
    label_name.pack(pady=10)
    entry_name = tk.Entry(top, width=25)
    entry_name.pack(pady=5)

    label_code = tk.Label(top, text="Ürün Kodu Giriniz:")
    label_code.pack(pady=10)
    entry_code = tk.Entry(top, width=25)
    entry_code.pack(pady=5)

    label_num = tk.Label(top, text="Ürün Sayısı Giriniz:")
    label_num.pack(pady=10)
    entry_num = tk.Entry(top, width=25)
    entry_num.pack(pady=5)

    buton_save = tk.Button(top,text="Kaydet", command=  kaydet)
    buton_save.pack(pady=10)

def sil():
    if kontrol() == -1:
        return
    
    def delete_product():
        code = entry_code.get()
        global df
        result = df[df["Product Code"] == code]
        if not result.empty:
            result_str = result.to_string(index=False)
            df = df[df["Product Code"] != code]
            df.to_csv(path, index=False)
            show_file()
            tk.messagebox.showinfo("Sonuç", f"Bu ürün silindi:\n{result_str}")
        else:
            tk.messagebox.showinfo("Sonuç", "Ürün bulunamadı.")
        top.destroy()

    top = tk.Toplevel(pencere)
    top.title("Ürün Sil")
    top.geometry("300x150")

    label_code = tk.Label(top, text="Ürün kodu giriniz:")
    label_code.pack(pady=10)
    entry_code = tk.Entry(top, width=25)
    entry_code.pack(pady=5)

    button_search = tk.Button(top, text="Ara", command=delete_product)
    button_search.pack(pady=10)


def guncelle():
    if kontrol() == -1:
        return
    
    def update_product():
        product_name = entry_name.get()
        product_code = entry_code.get()
        product_number = entry_num.get()
        global df
        if product_code not in df["Product Code"].values:
            tk.messagebox.showinfo("Bilgi", "Ürün bulunamadı.")
            return
        # güncelle
        df.loc[df["Product Code"] == product_code, ["Product Name", "Product Number"]] = [product_name, product_number]
        df.to_csv(path, index=False)
        tk.messagebox.showinfo("Bilgi", "Ürün başarıyla güncellendi.")
        show_file()
        top.destroy()

    top = tk.Toplevel(pencere)
    top.title("Ürün Güncelle")
    top.geometry("300x300")

    label_name = tk.Label(top, text="Ürün Adı Giriniz:")
    label_name.pack(pady=10)
    entry_name = tk.Entry(top, width=25)
    entry_name.pack(pady=5)

    label_code = tk.Label(top, text="Ürün Kodu Giriniz:")
    label_code.pack(pady=10)
    entry_code = tk.Entry(top, width=25)
    entry_code.pack(pady=5)

    label_num = tk.Label(top, text="Ürün Sayısı Giriniz:")
    label_num.pack(pady=10)
    entry_num = tk.Entry(top, width=25)
    entry_num.pack(pady=5)

    buton_save = tk.Button(top, text="Güncelle", command=update_product)
    buton_save.pack(pady=10)

pencere = tk.Tk()
pencere.geometry("750x750")
pencere.pack_propagate(0)
pencere.resizable(0,0)

üst_cerceve = tk.LabelFrame(pencere, text = "Malzemeler")
üst_cerceve.place(height=650,width=750)

alt_cerceve1 = tk.LabelFrame(pencere, text="Dosya İşlemleri")
alt_cerceve1.place(y=650,height=100,width=375)
alt_cerceve2 = tk.LabelFrame(pencere, text="Eşya Ekle veya Bul")
alt_cerceve2.place(x=375,y=650,height=100,width=375)

buton1_sol = tk.Button(alt_cerceve1,width=7,height=1,text="Dosya Ara", command= find_file)
buton1_sol.place(x= 55,y=40)

buton2_sol = tk.Button(alt_cerceve1,width=7,height=1,text="Oluştur", command= create)
buton2_sol.place(x= 175,y = 40)

label_file = ttk.Label(alt_cerceve1,text="Hiçbir Dosya Seçili Değil")
label_file.place(x=75, y=10)

buton1_sag = tk.Button(alt_cerceve2,width=7,height=1,text="Ekle", command=  ekle)
buton1_sag.place(x = 100, y=5)

buton2_sag = tk.Button(alt_cerceve2,width=7,height=1,text="Bul", command= bul)
buton2_sag.place(x = 200, y= 5)

buton3_sag = tk.Button(alt_cerceve2,width=7,height=1,text="Sil", command= sil)
buton3_sag.place(x = 100, y= 45)

buton4_sag = tk.Button(alt_cerceve2, width=7, height=1, text="Güncelle", command=guncelle)
buton4_sag.place(x=200, y=45)

table = ttk.Treeview(üst_cerceve)
table.place(relheight=1, relwidth=1)

kaydirx= tk.Scrollbar(üst_cerceve, orient="vertical", command=table.xview)
kaydiry= tk.Scrollbar(üst_cerceve, orient="horizontal", command=table.yview)
table.configure(xscrollcommand=kaydirx, yscrollcommand=kaydiry)
kaydirx.pack(side="bottom",fill="x")
kaydiry.pack(side="right",fill="y")


pencere.mainloop()

