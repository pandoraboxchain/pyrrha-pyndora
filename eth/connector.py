import json
from os import path
from web3 import Web3, HTTPProvider

class ETHConnector():

    def __init__(self, config):
        self.config = config
        #self.delegate = delegate

        print('Connecting to Ethereum node on %s:%d...' % (self.config['server'], self.config['port']))
        self.web3 = Web3(HTTPProvider(endpoint_uri="%s:%d" % (self.config['server'], self.config['port'])))
        print('Ethereum node connected successfully')

        print('Loading ABIs...')
        abi = self.read_abi("Pandora")
        self.pandora_abi = self.read_abi("Pandora")
        #self.kernel_abi = self.read_abi("KernelContract")
        #self.dataset_abi = self.read_abi("DatasetContract")
        print('ABIs loaded successfully')

        #print('Getting root contract %s...' % self.config.contract)
        self.pandora_contract = self.web3.eth.contract(address=self.config['contract'], abi=self.pandora_abi)
        self.event_filter = self.pandora_contract.on('CognitiveJobCreated')
        #print('Root contract instantiated')

    def run(self):
        print('Event start')
        self.event_filter.start()
        print('Event watch')
        self.event_filter.watch(self.on_cognitive_job_created)
        print('Event join')
        self.event_filter.join()
        print('Event done')

    def on_cognitive_job_created(self, event: dict):
        address = event['args']['contractAddress']
        print('Got new cognitive job contract %s' % address)

    def read_abi(self, file: str) -> str:
        here = path.abspath(path.dirname(__file__))
        file = "%s.json" % file
        with open(path.join(here, self.config['abi'], file), encoding='utf-8') as f:
            artifact = json.load(f)
        return artifact['abi']
