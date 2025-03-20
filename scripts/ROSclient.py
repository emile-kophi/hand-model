import roslibpy
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RosClient:
    def __init__(self, host='localhost', port=9090) :
        self.client= roslibpy.Ros(host=host,port=port)
        self.publishers= {}
        self.subscribers= {}
        self.running=False

    
    def connect(self):
        """Connect to the ROS server."""
        self.client.run()
        self.running = True
        logging.info(f'Connected: {self.client.is_connected}')

    def disconnect(self):
        """Disconnect from the ROS client and stop threads."""
        self.running = False
        for pub in self.publishers.values():
            pub.unadvertise()
        self.client.terminate()
        logging.info("Disconnected")

    def create_subscriber(self, topic_name, msg_type, callback):

        subscriber = roslibpy.Topic(self.client, topic_name, msg_type)
        subscriber.subscribe(callback)
        self.subscribers[topic_name] = subscriber
        logging.info(f"Subscribed to {topic_name}")

    def create_publisher(self, topic_name, msg_type):
        """Create a publisher if it doesn't exist"""
        if topic_name not in self.publishers:
            talker = roslibpy.Topic(self.client, topic_name, msg_type)
            talker.advertise()
            self.publishers[topic_name] = talker
            logging.info(f"Publisher created for {topic_name}")
        else:
            logging.info(f"Publisher already exists for {topic_name}")


    def publish_data(self, topic_name, message_data):
        """Publish message data"""
        if topic_name in self.publishers:
            talker = self.publishers[topic_name]
            # Verifica che talker sia di tipo roslibpy.Topic
            if isinstance(talker, roslibpy.Topic):
                talker.publish(roslibpy.Message(message_data))
                logging.info(f"Published data to {topic_name}")
                talker.publish(roslibpy.Message(message_data))
                logging.info(f"Published data to {topic_name}")
            else:
                logging.error(f"Talker is not of type roslibpy.Topic!")

        else:
            logging.error(f"Publisher for {topic_name} does not exist! Call create_publisher first.")