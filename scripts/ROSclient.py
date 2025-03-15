import roslibpy
import logging


class ROSclient:
    def __init__(self, host='localhost', port=9090):
        self.client= roslibpy.Ros(host=host,port=port)
        self.publishers= {}
        self.subscribers= {}
        self.publishing_threads = {}
        self.running=False

        # logger configuration
        self.logger = logging.getLogger(__name__) 
        self.logger.setLevel(logging.DEBUG) 

        # log manager configuration
        manager = logging.StreamHandler()
        manager.setLevel(logging.DEBUG)
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
        for thread in self.publishing_threads.values():
            thread.join()  # Wait for threads to finish
        for pub in self.publishers.values():
            pub.unadvertise()
        self.client.close()
        self.logger.info("Disconnected")

    def create_subscriber(self, topic_name, msg_type, callback):

        subscriber = roslibpy.Topic(self.client, topic_name, msg_type, queue_size=10)
        subscriber.subscribe(callback)
        self.subscribers[topic_name] = subscriber
        self.logger.info(f"Subscribed to {topic_name}")


    def create_publisher(self, topic_name, msg_type, message_data):

        talker = roslibpy.Topic(self.client, topic_name, msg_type)

        talker.publish(roslibpy.Message(message_data))
        self.logger.info(f"Published message to {topic_name}")
        talker.unadvertise()

    # def use_service(self, service_name, service_type):

    #     service = roslibpy.Service(self.client, service_name, service_type)
    #     request = roslibpy.ServiceRequest()
    #     result = service.call(request)
    #     self.logger.info(f"Service {type(result)} called")
        
    #     return result['']
