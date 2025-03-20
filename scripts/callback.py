import logging
from RosClient import RosClient
import roslibpy


# CALLBACK to recived landmark data
def hand_landmarks_callback(message):
    try:
        logging.info(" message recived")

        #Create dei custom message HandLandmark
        hand_landmarks_list = [
            roslibpy.Message({
                "id": lm["id"],
                "x": lm["x"],
                "y": lm["y"],
                "z": lm["z"]
            })
            for lm in message["landmarks"]
        ]
        # Create custom message All_landmarks []
        all_landmarks_msg = roslibpy.Message({
            "header": {
                "stamp": {
                    "secs": message['header']['stamp']['secs'],
                    "nsecs": message['header']['stamp']['nsecs']
                }
            },
            "hand": message['hand'],
            "score": message['score'],
            "landmarks": hand_landmarks_list
        })
        return(all_landmarks_msg)
    except Exception as e:
        logging.error(f"Error processing message: {e}")