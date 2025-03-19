import roslibpy
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



class ROSclient:
    def __init__(self, host='localhost', port=9090):
        self.client= roslibpy.Ros(host=host,port=port)
        self.publishers= {}
        self.subscribers= {}
        self.running=False

        # logger configuration
        self.logger = logging.getLogger(__name__) 
        self.logger.setLevel(logging.DEBUG) 

        # log manager configuration
        manager = logging.StreamHandler()
        manager.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        manager.setFormatter(formatter)

        # Add manager to the logger
        self.logger.addHandler(manager)

    def connect(self):
        """Connect to the ROS server."""
        self.client.run()
        self.running = True
        self.logger.info(f'Connected: {self.client.is_connected}')

    def disconnect(self):
        """Disconnect from the ROS client and stop threads."""
        self.running = False
        for pub in self.publishers.values():
            pub.unadvertise()
        self.client.terminate()
        self.logger.info("Disconnected")

    def create_subscriber(self, topic_name, msg_type, callback):

        subscriber = roslibpy.Topic(self.client, topic_name, msg_type)
        subscriber.subscribe(callback)
        self.subscribers[topic_name] = subscriber
        self.logger.info(f"Subscribed to {topic_name}")

    def create_publisher(self, topic_name, msg_type):
        """Create a publisher if it doesn't exist"""
        if topic_name not in self.publishers:
            talker = roslibpy.Topic(self.client, topic_name, msg_type)
            talker.advertise()
            self.publishers[topic_name] = talker
            self.logger.info(f"Publisher created for {topic_name}")
        else:
            self.logger.info(f"Publisher already exists for {topic_name}")

    def publish_data(self, topic_name, message_data):
        """Publish message data"""
        if topic_name in self.publishers:
            talker = self.publishers[topic_name]
            talker.publish(roslibpy.Message(message_data))
            self.logger.info(f"Published data to {topic_name}")
        else:
            self.logger.error(f"Publisher for {topic_name} does not exist! Call create_publisher first.")


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
                    "secs": int(message['timestamp']),
                    "nsecs": int((message['timestamp'] % 1) * 1e9)
                }
            },
            "hand": message['hand'],
            "score": message['score'],
            "landmarks": hand_landmarks_list
        })
        ros_client.publish_data("/hand_landmarks", all_landmarks_msg)

    except Exception as e:
        logging.error(f"Error processing message: {e}")

#  ROSclient and topic launch
if __name__ == "__main__":
    ros_client = ROSclient()
    ros_client.connect()
    ros_client.create_subscriber('/hand_landmarks', 'custom_msgs/All_landmarks', hand_landmarks_callback)

    try:
        ros_client.client.run_forever()
    except KeyboardInterrupt:
        logging.warning("Shutting down...")
        ros_client.disconnect()