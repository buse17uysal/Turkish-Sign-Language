import speech_recognition as sr
import cv2
import customtkinter as ctk
import mediapipe as mp

# Konuşmayı metne dönüştürmek için tanıyıcıyı başlat
r = sr.Recognizer()

def speech_to_text_turkish():
    """Türkçe metin dönüştürme işlemi yapar."""
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
            return text.lower()

    except sr.RequestError as e:
        output_label.configure(text="İstek işlenemedi; {0}".format(e))  # Hata mesajını göster (Türkçe)
        root.update()
        return None
    except sr.UnknownValueError:
        output_label.configure(text="Bilinmeyen hata oluştu")  # Genel hata mesajını göster (Türkçe)
        root.update()
        return None

def on_key_press(event):
    """Tuşa basma olayını işlemek için fonksiyon"""
    if event.char == 'q':
        root.quit()

# CustomTkinter GUI penceresini oluştur
root = ctk.CTk()
root.title("Konuşma Tanıma")

# Çıktı için etiket oluştur
output_label = ctk.CTkLabel(root, text="")
output_label.pack(pady=20)

# Tuşa basma olayını bağla
root.bind("<KeyPress>", on_key_press)

# MediaPipe ve OpenCV kullanarak el algılama işlemini başlat
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    user_text = speech_to_text_turkish()
    if user_text:
        print("Kullanıcı dedi ki:", user_text)  # Tanınan metni ekrana yazdır

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
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Görüntüyü göster
    cv2.imshow("El Algılama", frame)

    # Tuş basma olaylarını kontrol et
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    root.update_idletasks()
    root.update()

cap.release()
cv2.destroyAllWindows()
