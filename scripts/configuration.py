import logging
import roslibpy

class RosParam:
    '''parameters of base configuration on ROS'''

    # configuration of logger
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)


    # ROS parameters
    ROS_TOPIC='/hand_landmarks'
    ROS_TOPIC_TYPE='custom_msgs/All_landmarks'

config= RosParam()


# CALLBACK to recived landmark data
def hand_landmarks_callback(message):
    try:
        config.logger.info(" message recived")

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
        config.logger.error(f"Error processing message: {e}")


