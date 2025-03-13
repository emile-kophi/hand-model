import cv2
import mediapipe as mp
import logging
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
logging.basicConfig(level=logging.DEBUG)

# For webcam input:
cap = cv2.VideoCapture(0)
if not cap.isOpened():
  logging.error("your cam is off")
  exit()
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.4,
    min_tracking_confidence=0.4) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      logging.info("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.flip(image, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
     for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
        hand_label = results.multi_handedness[i].classification[0].label  # 'Left' o 'Right'
        hand_score = results.multi_handedness[i].classification[0].score  # Probabilità che sia una mano
        timestamp = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
        # logging.debug(f"\n[Frame Timestamp: {timestamp} ms] Mano: {hand_label} ({hand_score:.2f})")
        # logging.info(type(results.multi_hand_landmarks))
        # logging.debug("end of frame")
        for idx, landmark in enumerate(hand_landmarks.landmark):
        #  logging.debug(f"Landmark({idx}): x={landmark.x:.4f}, y={landmark.y:.4f}, z={landmark.z:.4f}")
         print(dir(landmark))
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
      
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', image)
    # All'interno del tuo script Python
    # 'premi ESC per interompere il video'
    if cv2.waitKey(5) & 0xFF == 27:
      logging.warning("no more access for webcame")
      break
cap.release()