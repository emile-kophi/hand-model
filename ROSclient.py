import roslibpy
import logging


class ROSclient:
    def __init__(self, host='localhost', port=9090):
        self.client= roslibpy.Ros(host=host,port=port)
        self.publishers= {}
        self.suscribers= {}
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