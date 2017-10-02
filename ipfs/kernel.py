import json

from ipfs.connector import IPFSConnector

def get_kernel(connector: IPFSConnector, addr: str):
    result = connector.download_file(addr)

    with open(addr) as data_file:
        data = json.load(data_file)

    weights = data['weights']
    model = data['model']

    result = connector.download_file(weights)
    result = connector.download_file(model)

    return data
