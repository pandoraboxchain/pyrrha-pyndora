from states.idle import Idle
from eth.connector import ETHConnector
from ipfs.connector import IPFSConnector
from config.config import CONFIGS

class Worker():

    def __init__(self):
        self.eth = ETHConnector(CONFIGS["ETH"])
        self.eth.run()
        self.ipfs = IPFSConnector(CONFIGS["IPFS"])
        self.state = Idle()

if __name__ == '__main__':
    Worker()
