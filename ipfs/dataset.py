import json

from ipfs.connector import IPFSConnector

def get_dataset(connector: IPFSConnector, addr: str):
    result = connector.download_file(addr)

    with open(addr) as data_file:
        data = json.load(data_file)

    batches = data['batches']
    for item in batches:
        result = connector.download_file(item)

    print(data)
