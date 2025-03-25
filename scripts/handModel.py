
''''In this code, we use the Hand Landmark Model by MediaPipe (Google) and add lines for communication via ROS
model: https://mediapipe.readthedocs.io/en/latest/solutions/hands.html#hand-landmark-model'''


import cv2
import mediapipe as mp
import time
from RosClient import RosClient
import roslibpy
from configuration import hand_landmarks_callback
from configuration import config as cfg
from configuration import tracking as tcg





class HandDetector:
    """manage the hand detection by MediaPipe."""
    
    def __init__(self, min_detection_confidence=tcg.detection_confidence, min_tracking_confidence=tcg.tracking_confidence):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.hands = self.mp_hands.Hands(
            model_complexity=tcg.complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def detect_hands(self, image):
        """image elaboration """

        image.flags.writeable = False
        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return results, image

    def draw_landmarks(self, image, hand_landmarks):
        """Draw landmarks on image deteceted"""
        
        for hand in hand_landmarks:
            self.mp_drawing.draw_landmarks(
                image,
                hand,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style()
            )
        return image


class HandTrackerApp:
    """management of tracking process and send data to ROS."""
    
    def __init__(self):
        self.detector = HandDetector()
        self.ros_client = RosClient()
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            cfg.logger.error("Errore: la fotocamera non è accessibile.")
            exit()

    def start(self):

        """start hand's tracking and comunication via ROS."""
        self.ros_client.connect()
        self.ros_client.create_publisher(cfg.ROS_TOPIC, cfg.ROS_TOPIC_TYPE)
        self.ros_client.create_subscriber(cfg.ROS_TOPIC, cfg.ROS_TOPIC_TYPE, hand_landmarks_callback)

        try:
            with self.detector.hands as hands:
                while self.cap.isOpened():
                    success, image = self.cap.read()
                    if not success:
                        continue  # Skip empty frame

                    results, image = self.detector.detect_hands(image)

                    if results.multi_hand_landmarks:
                        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
                            hand_label = results.multi_handedness[i].classification[0].label
                            hand_score = results.multi_handedness[i].classification[0].score

                            landmarks = [{"id": idx, "x": lm.x, "y": lm.y, "z": lm.z} 
                                         for idx, lm in enumerate(hand_landmarks.landmark)]

                            # Create header ROS
                            header = {
                                'stamp': {'secs': int(time.time()), 'nsecs': 0},
                                'frame_id': 'hand_frame'
                            }

                            # Create ROS message
                            message_data = roslibpy.Message({
                                "header": header,
                                "hand": hand_label,
                                "score": hand_score,
                                "landmarks": landmarks
                            })

                            # data publication via ROS
                            self.ros_client.publish_data(cfg.ROS_TOPIC, message_data)

                            # draw landmarks
                            image = self.detector.draw_landmarks(image, [hand_landmarks])

                    cv2.imshow('MediaPipe Hands', image)

                    # ESC per uscire
                    if cv2.waitKey(5) & 0xFF == 27:
                        cfg.logger.warning("Chiusura del programma.")
                        break
        except Exception as e:
            cfg.logger.error(f"Errore durante l'esecuzione: {e}")
        finally:
            self.cap.release()
            self.ros_client.disconnect()
            cv2.destroyAllWindows()


# start the program
if __name__ == "__main__":
    app = HandTrackerApp()
    app.start()
