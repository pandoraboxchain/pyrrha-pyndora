import ipfsapi
import os

class IPFSConnector:

    def __init__(self, config):
        self.config = config
        self.api = ipfsapi.connect(self.config['server'], self.config['port'])

    def download_file(self, addr: str):
        os.chdir(self.config['data_path'])
        return self.api.get(addr)

    def upload_file(self, filename: str) -> str:
        os.chdir(self.config['data_path'])
        res = self.api.add(filename)
        return res['Hash']
