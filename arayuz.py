import os
from subprocess import call
from customtkinter import *
from PIL import Image, ImageTk
import tkinter as tk

# Mevcut betiğin dizinini al
def get_script_directory():
    return os.path.dirname(os.path.abspath(__file__))

# Çalışma dizinini değiştir
def change_working_directory(script_dir):
    os.chdir(script_dir)

# Yeni bir pencere aç ve verilen metni göster
def open_new_window(text):
    new_window = CTk()
    new_window.geometry("980x600")
    new_window.resizable(0, 0)

    text_frame = tk.Frame(master=new_window, bg="black")
    text_frame.pack(pady=(30, 0), padx=30, fill="both", expand=True)

    text_widget = tk.Text(master=text_frame, font=("Arial", 15), wrap="word")
    text_widget.pack(pady=10, padx=10, fill="both", expand=True)

    text_widget.insert("1.0", text)
    text_widget.configure(state='disabled')
    text_widget.see("1.0")

    new_window.mainloop()

# Metin dosyasını okuma
def open_text_file(file_name):
    with open(os.path.join("Text", file_name), "r", encoding="utf-8") as file:
        return file.read()

# Belirli bir test dosyasını çalıştır
def run_test(test_file):
    call(["python", test_file])

# Kategori seçim penceresini aç
def open_category_window():
    category_window = CTk()
    category_window.geometry("300x500")
    category_window.resizable(0, 0)

    CTkLabel(master=category_window, text="Kategori Seçiniz", font=("Arial Bold", 20)).pack(pady=(20, 30))

    categories = ["Esya", "Fiil", "Hayvan", "Meslek", "Renk", "Sayi", "Tasit", "Yiyecek", "Yon"]
    for category in categories:
        CTkButton(master=category_window, text=category, font=("Arial", 12), command=lambda c=category: run_test(f"Test/test_{c.lower()}.py")).pack(pady=5)

    category_window.mainloop()

# Cümleler penceresini aç
def open_sentences_window():
    # test_cumle.py dosyasını çalıştır
    run_test("Test/test_cumle.py")

    # subprocess kullanarak ses.py dosyasını aç
    call(["python", "ses.py"])


# Betik dizinini al ve çalışma dizinini değiştir
script_dir = get_script_directory()
change_working_directory(script_dir)

# Ana uygulama penceresi oluştur
app = CTk()
app.geometry("1200x650")  # Pencere boyutu 1200x650 olarak ayarlandı
app.resizable(0, 0)

# Karanlık mod ayarı
set_appearance_mode("dark")

# Yan panel oluştur ve butonlar ekle
sidebar_frame = CTkFrame(app, width=200)  # Sidebar genişliğini artırdık
sidebar_frame.pack(side="left", fill="y")

# Logo ekle
logo_image_path = "Foto/tu_logo.png"
logo_image = Image.open(logo_image_path).resize((180, 180))  # Resim boyutunu ayarladık
logo_image = ImageTk.PhotoImage(logo_image)

sidebar_label = tk.Label(sidebar_frame, image=logo_image)
sidebar_label.image = logo_image  # Referans tutmak için
sidebar_label.pack(pady=20)
sidebar_label.configure(bg="#282b2b")


buttons_info = {
    "İşaret Dili": "text1.txt",
    "Türk İşaret Dili": "text2.txt",
    "Proje Hakkında": "text3.txt",
    "Geliştirme Araçları": "text4.txt",
    "Proje Aşamaları": "text5.txt",
    "Kaynak ve Referanslar": "text6.txt",
    "Proje Ekibi": "text7.txt",
    "Proje Danışmanı": "text8.txt"
}

for btn_text, file_name in buttons_info.items():
    CTkButton(sidebar_frame, text=btn_text, font=("Arial", 12), command=lambda fn=file_name: open_new_window(open_text_file(fn))).pack(pady=10)

main_frame = CTkFrame(app)

# Ana başlık etiketi
CTkLabel(master=app, text="Dilsiz Çevirmeni", font=("Arial Bold", 20), justify="left").pack(anchor="w", pady=(10, 0), padx=(20, 0))

# İstatistik çerçeveleri
stats_frame = CTkFrame(master=app, fg_color="transparent")
stats_frame.pack(padx=(20, 0), pady=(10, 0), anchor="nw")

quizzes_taken_frame = CTkFrame(master=stats_frame, fg_color="#70179A", width=132, height=70, corner_radius=8)
quizzes_taken_frame.pack_propagate(0)
quizzes_taken_frame.pack(anchor="w", side="left", padx=(0, 20))

alpha_button = CTkButton(master=quizzes_taken_frame, text="Alfabe", font=("Arial Bold", 10), text_color="#F3D9FF", command=lambda: run_test("Test/test_alfabe.py"), fg_color="#70179A")
alpha_button.pack(anchor="nw")
CTkLabel(master=quizzes_taken_frame, text="29", justify="left", font=("Arial Bold", 25), text_color="#F3D9FF").pack(anchor="nw", padx=(14, 0))

correct_qs_frame = CTkFrame(master=stats_frame, fg_color="#146C63", width=132, height=70, corner_radius=8)
correct_qs_frame.pack_propagate(0)
correct_qs_frame.pack(anchor="w", side="left", padx=(0, 20))

kelimeler_button = CTkButton(master=correct_qs_frame, text="Kelimeler", font=("Arial Bold", 10), text_color="#D5FFFB", command=open_category_window, fg_color="#146C63")
kelimeler_button.pack(anchor="nw")
CTkLabel(master=correct_qs_frame, text="100", justify="left", font=("Arial Bold", 25), text_color="#D5FFFB").pack(anchor="nw", padx=(14, 0))

highest_score_frame = CTkFrame(master=stats_frame, fg_color="#9A1717", width=132, height=70, corner_radius=8)
highest_score_frame.pack_propagate(0)
highest_score_frame.pack(anchor="w", side="left", padx=(0, 20))

cümleler_button = CTkButton(master=highest_score_frame, text="Cümleler", font=("Arial Bold", 10), text_color="#FFCFCF", command=open_sentences_window, fg_color="#9A1717")
cümleler_button.pack(anchor="nw")
CTkLabel(master=highest_score_frame, text="Sesli Komut", justify="left", font=("Arial Bold", 20), text_color="#FFCFCF").pack(anchor="nw", padx=(14, 0))

# Başlık etiketi
CTkLabel(master=app, text="Dijital erişilebilirlik herkesin hakkı! Eşit şartlarda doğmasak da, eşit şartlarda yaşayabiliriz.", font=("Arial Bold", 20), justify="left").pack(anchor="nw", side="top", padx=(20, 0), pady=(10, 0))

# Quiz çerçeveleri
quizzes_frame = CTkFrame(master=app, fg_color="transparent")
quizzes_frame.pack(pady=(10, 0), padx=(20, 0), anchor="nw")

# Görsellerin listesi (resimlerin tıklanabilirliğini kaldırdık)
images = ["Foto/foto1.png", "Foto/foto2.png", "Foto/foto3.png", "Foto/foto4.jpg", "Foto/foto5.png", "Foto/foto6.png"]

# Görselleri 2x3 formatında düzenle
for i in range(0, len(images), 3):
    row_frame = CTkFrame(master=quizzes_frame, fg_color="transparent")
    row_frame.pack(anchor="nw", pady=(0, 10))

    for image_name in images[i:i+3]:
        img_data = Image.open(image_name).resize((300, 200))  # Resized to fit better in 2x3 layout
        img = CTkImage(light_image=img_data, dark_image=img_data, size=(300, 200))
        label = CTkLabel(master=row_frame, text="", image=img, corner_radius=8)
        label.pack(side="left", padx=(0, 20))

# Ana uygulama döngüsü
app.mainloop()
