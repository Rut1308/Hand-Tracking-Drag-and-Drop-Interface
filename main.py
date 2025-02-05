import cv2
from cvzone.HandTrackingModule import HandDetector


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize Hand Detector
detector = HandDetector(detectionCon=0.5, maxHands=2)
colorR = (0, 0, 255)


class DragRect:
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = list(posCenter)
        self.size = size
        self.dragging = False

    def update(self, cursor, isDragging):
        cx, cy = self.posCenter
        w, h = self.size

        if isDragging:
            self.dragging = True
            self.posCenter = [cursor[0], cursor[1]]  # Update rectangle position
        else:
            self.dragging = False


rectList = []
for x in range(5):
    rectList.append(DragRect([x * 250 + 300, 300]))

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

            x1, y1, _ = lmList[8]
            x2, y2, _ = lmList[12]


            l, _, _ = detector.findDistance((x1, y1), (x2, y2), image)
            print(f"Finger Distance: {l}")

            cursor = lmList[8]


            for rect in rectList:
                cx, cy = rect.posCenter
                w, h = rect.size
                isInside = cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2

               
                isDragging = isInside and l < 30
                rect.update(cursor, isDragging)

    # Draw each rectangle
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(image, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, -1)


    cv2.imshow("Hand", image)
    cv2.waitKey(1)
