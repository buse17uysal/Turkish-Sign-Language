import speech_recognition as sr
import cv2
import customtkinter as ctk
import mediapipe as mp
from PIL import Image, ImageTk, ImageDraw, ImageFont
import threading
import numpy as np

# Konuşmayı metne dönüştürmek için tanıyıcıyı başlat
r = sr.Recognizer()

# Global değişkenler
cap = None
hands = None
user_text = ""
mp_hands = None

def speech_to_text_turkish():
    """Türkçe metin dönüştürme işlemi yapar."""
    global user_text
    try:
        # Giriş için mikrofonu kullan
        with sr.Microphone() as source:
            output_label.configure(text="Sesinizi kaydediyorum...")  # Kaydedildiğini kullanıcıya bildir (Türkçe)
            root.update()

            # Ortam gürültüsünü düzeltmek için ayarla
            r.adjust_for_ambient_noise(source, duration=0.2)

            # Kullanıcı girişini dinle
            audio = r.listen(source)

            # Türkçe modeliyle Google Konuşma Tanıma kullanarak konuşmayı tanı
            text = r.recognize_google(audio, language='tr-TR')
            output_label.configure(text="Dinledim: " + text)  # Tanınan metni ekranda göster (Türkçe)
            root.update()
            user_text = text.lower()

    except sr.RequestError as e:
        output_label.configure(text="İstek işlenemedi; {0}".format(e))  # Hata mesajını göster (Türkçe)
        root.update()
        user_text = None
    except sr.UnknownValueError:
        output_label.configure(text="Bilinmeyen hata oluştu")  # Genel hata mesajını göster (Türkçe)
        root.update()
        user_text = None

def on_key_press(event):
    """Tuşa basma olayını işlemek için fonksiyon"""
    if event.char == 'q':
        root.quit()

def reset_camera_and_speech():
    global cap, hands, user_text
    cap.release()
    user_text = ""
    output_label.configure(text="")
    initialize_camera()
    threading.Thread(target=main_loop).start()
    threading.Thread(target=speech_to_text_turkish).start()

def initialize_camera():
    global cap, hands, mp_hands
    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    return cap.isOpened()

def main_loop():
    global user_text
    while cap.isOpened():
        # Kameradan görüntü al
        ret, frame = cap.read()
        if not ret:
            break
        
        # Görüntüyü ters çevir (aynalama)
        frame = cv2.flip(frame, 1)
        
        # Renk uzayını BGR'den RGB'ye çevir
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # El algılama işlemi yap
        result = hands.process(rgb_frame)
        
        # Tespit edilen elleri çiz
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(rgb_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # Tanınan metni görüntüye yazdır
        if user_text:
            # Pillow ile yazı yazma
            pil_image = Image.fromarray(rgb_frame)
            draw = ImageDraw.Draw(pil_image)
            # Burada Türkçe karakterleri destekleyen bir font dosyası seçmelisiniz
            font = ImageFont.truetype("arial.ttf", 32)
            draw.text((10, 10), user_text, font=font, fill=(0, 255, 0))

            # Pillow görüntüsünü tekrar OpenCV formatına çevir
            rgb_frame = np.array(pil_image)
        
        # OpenCV görüntüsünü tkinter'da göster
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)

        root.update_idletasks()
        root.update()

    cap.release()
    cv2.destroyAllWindows()

# CustomTkinter GUI penceresini oluştur
root = ctk.CTk()
root.title("Konuşma Tanıma ve El Algılama")

# Çıktı için etiket oluştur
output_label = ctk.CTkLabel(root, text="")
output_label.pack(pady=20)

# Kamera görüntüsü için bir etiket oluştur
camera_label = ctk.CTkLabel(root)
camera_label.pack(pady=20)

# Reset butonunu oluştur
reset_button = ctk.CTkButton(root, text="Reset", command=reset_camera_and_speech)
reset_button.pack(pady=20)

# Tuşa basma olayını bağla
root.bind("<KeyPress>", on_key_press)

# MediaPipe ve OpenCV kullanarak el algılama işlemini başlat
mp_drawing = mp.solutions.drawing_utils

if initialize_camera():
    threading.Thread(target=main_loop).start()
    threading.Thread(target=speech_to_text_turkish).start()
else:
    output_label.configure(text="Kamera açılamadı!")

root.mainloop()
