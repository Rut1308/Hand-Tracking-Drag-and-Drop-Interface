import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize Hand Detector
detector = HandDetector(detectionCon=0.5, maxHands=1)
colorR = (0, 0, 255)


class DragRect:
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = list(posCenter)
        self.size = size
        self.dragging = False
        self.smoothFactor = 0.2  # Adjust for smoother movement

    def update(self, cursor):
        cx, cy = self.posCenter
        self.posCenter[0] += int((cursor[0] - cx) * self.smoothFactor)
        self.posCenter[1] += int((cursor[1] - cy) * self.smoothFactor)


rectList = [DragRect([x * 250 + 300, 300]) for x in range(5)]

while True:
    success, image = cap.read()
    if not success:
        break

    image = cv2.flip(image, 1)
    hands, image = detector.findHands(image)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]

        if len(lmList) >= 12:
            cursor = lmList[8]  # Index finger tip

            for rect in rectList:
                cx, cy = rect.posCenter
                w, h = rect.size

                isInside = cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2

                if isInside:
                    rect.update(cursor)

    # Draw each rectangle
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(image, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, -1)

    cv2.imshow("Hand", image)
    cv2.waitKey(1)
