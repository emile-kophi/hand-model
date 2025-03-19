import cv2
import mediapipe as mp
import logging
from ROSclient import ROSclient
import roslibpy
from ROSclient import hand_landmarks_callback
import time



mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

logging.basicConfig(level=logging.INFO)

# Initialize ROS connection
ros_client_pub = ROSclient()
ros_client_sub = ROSclient()
ros_client_pub.connect()
ros_client_sub.connect()
ros_client_pub.create_publisher('/hand_landmarks', 'custom_msgs/All_landmarks')  # Add publisher for ROS
ros_client_sub.create_subscriber('/hand_landmarks', 'custom_msgs/All_landmarks', hand_landmarks_callback)

# Webcam input:
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture(cv2.CAP_DSHOW)  # Usa il driver di Windows DirectShow

if not cap.isOpened():
    logging.error("Your camera is off")
    exit()

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6) as hands:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue  # If the frame is empty, skip to the next iteration

        # To improve performance, mark the image as not writable to pass by reference
        image.flags.writeable = False
        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                hand_label = results.multi_handedness[i].classification[0].label  # 'Left' or 'Right'
                hand_score = results.multi_handedness[i].classification[0].score  # Probability of hand identification
                timestamp = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)
                # Creazione manuale di un Header come dizionario
                header = {
                'stamp': {'secs': int(time.time()), 'nsecs': 0},  # Timestamp in secondi e nanosecondi
                'frame_id': 'hand_frame'  # Definisci il frame_id
                }


                # Save landmark coordinates in a dictionary
                landmarks = []
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    landmarks.append({
                        "id": idx,
                        "x": landmark.x,
                        "y": landmark.y,
                        "z": landmark.z
                    })

                # Create the message for ROS
                message_data = roslibpy.Message({
                    "header": header,
                    "hand": hand_label,
                    "score": hand_score,
                    "landmarks": landmarks
                })

                # Draw the landmarks on the hands
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

            # publish data
            ros_client_pub.publish_data('/hand_landmarks', message_data)



        # Display the image
        cv2.imshow('MediaPipe Hands', image)

        # Press ESC to stop the video
        if cv2.waitKey(5) & 0xFF == 27:
            logging.warning("No more access for webcam")
            break

cap.release()
ros_client_pub.disconnect()
ros_client_sub.disconnect()