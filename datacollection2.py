import cv2
import mediapipe as mp
import os

# Mediapipe kütüphanesini yükler
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Elleri algılamak için bir Hands modeli oluşturur
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# Kamera açılır
cap = cv2.VideoCapture(0)

# Fotoğrafların kaydedileceği klasörü belirler
output_folder = "captured_photos"
os.makedirs(output_folder, exist_ok=True)

# Fotoğraf sayacı
photo_counter = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Görüntüyü RGB'ye dönüştürür
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Görüntüyü el işareti modeline verir
    results = hands.process(frame_rgb)

    # Eğer el algılandıysa
    if results.multi_hand_landmarks:
        # Her el için işaretçilerin konumlarını çizer
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Elin üstünde metin ekler
            if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x < hand_landmarks.landmark[
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x:
                hand_side = "Sol El"
            else:
                hand_side = "Sag El"

            text_size = cv2.getTextSize(hand_side, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            cv2.putText(frame, hand_side, (int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1] - text_size[0] / 2),
                                            int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame.shape[0] - 50)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Bir tuşa basıldığında fotoğrafı kaydeder
        if cv2.waitKey(1) & 0xFF == ord('c'):
            photo_counter += 1
            photo_name = f"photo_{photo_counter}.jpg"
            photo_path = os.path.join(output_folder, photo_name)
            cv2.imwrite(photo_path, frame)
            print(f"Photo captured: {photo_name}")

    # Görüntüyü gösterir
    cv2.imshow('Hand Tracking', frame)

    # 'q' tuşuna basıldığında çıkış yapar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırakır ve pencereleri kapatır
cap.release()
cv2.destroyAllWindows()