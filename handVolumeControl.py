import cv2
import time
import numpy as np
import HandtrackingModule as htm
import soundLevel as sl
import math

import threading
import queue

# Configurations
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 10)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Trackers and Utilities
pTime = 0
prevVolLevel = 0
lastVolumeUpdate = 0
volumeUpdateInterval = 0.3  # seconds
alpha = 0.3  # smoothing factor
volume_queue = queue.Queue() #Creting queeue for multithreading

# Custom modules
detector = htm.handDetector(detectionCon=0.7)
volume = sl.SoundLevel()

background_mode = True


def volume_setter_thread(volume_obj):
    while True:
        vol_level = volume_queue.get()  # Waits until a new volume is available
        if vol_level is None:
            break  # Exit signal
        volume_obj.set_volume(vol_level)
        volume_queue.task_done()

while True:
    success, img = cap.read()
    if not success:
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)


    if len(lmList) != 0:
        # Extract tip of thumb and index finger
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Drawing
        cv2.circle(img, (x1, y1), 7, (255, 0, 255), 2)
        cv2.circle(img, (x2, y2), 7, (255, 0, 255), 2)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 4, (0, 0, 0), 2)

        # Volume mapping
        lengthLine = math.hypot(x2 - x1, y2 - y1)
        print(f"The length of the line is {lengthLine}")
        clampLine = max(30, min(lengthLine, 160))
        volLevel = np.interp(clampLine, [30, 160], [0.0, 200.0])  # Use float

        # Exponential smoothing
        smoothedVolLevel = alpha * volLevel + (1 - alpha) * prevVolLevel
        prevVolLevel = smoothedVolLevel

        volume_thread = threading.Thread(target=volume_setter_thread, args=(volume,), daemon=True)
        volume_thread.start()

        # Update system volume periodically
        if time.time() - lastVolumeUpdate > volumeUpdateInterval:
            volume_queue.put(smoothedVolLevel)  # Send volume to background thread
            lastVolumeUpdate = time.time()
    else:
        pass # No hand detected, do NOT update volume or prevVolLevel


    # FPS display
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (40, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    # Display window
    if not background_mode:
        cv2.imshow('MediaPipe Volume Control', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
