import cv2
from cvzone.HandTrackingModule import HandDetector

# Kamerayı başlat
cap = cv2.VideoCapture(0)

# El algılayıcıyı başlat
detector = HandDetector(maxHands=2)

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    
    # Elleri algıla
    hands, img = detector.findHands(img)
    
    # Algılanan eller varsa
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            
            # Algılanan her elin etrafına daha kalın bir dikdörtgen çiz
            cv2.rectangle(imgOutput, (x, y), (x + w, y + h), (0, 255, 0), 6)
    
    # Görüntüyü göster
    cv2.imshow('Image', imgOutput)
    
    # 'q' tuşuna basarak çık
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# Kaynakları serbest bırak ve pencereleri kapat
cap.release()
cv2.destroyAllWindows()
