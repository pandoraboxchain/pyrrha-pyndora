from states.idle import Idle
from eth.connector import ETHConnector
from ipfs.connector import IPFSConnector
from config.config import CONFIGS

import threading

class Worker():

    def __init__(self):
        self.state = Idle()
        self.state.worker = self
        self.eth = ETHConnector(CONFIGS["ETH"])
        self.eth.send_alive()
        self.eth.trigger = lambda event: self.state.on_event(event)
        thread = threading.Thread(target=self.eth.run, args=())
        thread.daemon = True
        thread.start()
        thread.join()
        self.ipfs = IPFSConnector(CONFIGS["IPFS"])

if __name__ == '__main__':
    Worker()
