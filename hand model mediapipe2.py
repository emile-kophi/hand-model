import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
from mediapipe.tasks.python.vision.hand_landmarker import HandLandmarkerResult

model_path = r'C:\UNIFI\LM Bio UniFi\II ANNO\PRIMO SEMESTRE\ANALISI DI IMMAGINI E RADIOMICA\TESINA\hand model\hand_landmarker.task'

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

def draw_landmarks(image, landmarks):
    height, width, _ = image.shape
    for landmark in landmarks:
        x = int(landmark.x * width)
        y = int(landmark.y * height)
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
    connections = [(0, 1), (1, 2), (2, 3), (3, 4),
                   (0, 5), (5, 6), (6, 7), (7, 8),
                   (0, 9), (9, 10), (10, 11), (11, 12),
                   (0, 13), (13, 14), (14, 15), (15, 16),
                   (0, 17), (17, 18), (18, 19), (19, 20)]
    for start, end in connections:
        x1, y1 = int(landmarks[start].x * width), int(landmarks[start].y * height)
        x2, y2 = int(landmarks[end].x * width), int(landmarks[end].y * height)
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global frame
    if result.hand_landmarks:
        for i, landmarks in enumerate(result.hand_landmarks):
            handedness = result.handedness[i][0].category_name # Ottieni la mano (destra o sinistra)
            print(f"Frame Timestamp: {timestamp_ms}, Mano: {handedness}") # stampa la mano rilevata.
            draw_landmarks(current_frame, landmarks)

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

cap = cv2.VideoCapture(0)
with HandLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        current_frame = frame.copy()
        

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        timestamp = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
        landmarker.detect_async(mp_image, timestamp)

        show_frame= cv2.flip(frame, 1)
        cv2.imshow("Hand Tracking", show_frame)

        if cv2.waitKey(5) & 0xFF == 27:
            print("no access for webcam")
            break
   
cap.release()
cv2.destroyAllWindows()