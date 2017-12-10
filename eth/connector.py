import json
from os import path
from web3 import Web3, HTTPProvider
from states.events.cognitive_job_created import CognitiveJobCreated
from contract.statuses import statuses, get_status_by_number


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
        address = event['args']['cognitiveJob']
        print('Got new cognitive job contract %s' % address)
        abi = self.read_abi("CognitiveJob")
        contract = self.web3.eth.contract(address=address, abi=abi)
        event = CognitiveJobCreated(contract, address)
        self.trigger(event)

    def read_abi(self, file: str) -> str:
        here = path.abspath(path.dirname(__file__))
        file = "%s.json" % file
        with open(path.join(here, self.config['abi'], file), encoding='utf-8') as f:
            artifact = json.load(f)
        return artifact['abi']

    def get_kernel(self, kernel):
        abi = self.read_abi("Kernel")
        contract = self.web3.eth.contract(address=kernel, abi=abi)
        return contract.call().ipfsAddress()

    def get_dataset(self, dataset):
        abi = self.read_abi("Dataset")
        contract = self.web3.eth.contract(address=dataset, abi=abi)
        return contract.call().ipfsAddress()

    def assign_job(self):
        self.get_account()
        self.worker_contract.transact({'from':self.config['worker']}).acceptAssignment()

    def accept_valid_data(self):
        self.get_account()
        self.worker_contract.transact({'from':self.config['worker']}).acceptValidData()

    def provide_results(self, result):
        self.get_account()
        self.worker_contract.transact({'from':self.config['worker']}).provideResults(result)

    def get_account(self):
        ac = self.web3.eth.account.privateKeyToAccount(self.config['private_key'])
        return ac

    def send_alive(self):
        abi = self.read_abi("WorkerNode")
        self.pandora_contract.call().workerNodes
        count = self.pandora_contract.call().workerNodesCount()
        self.worker_contract = None
        for item in range(0, count):
            worker_addr = self.pandora_contract.call().workerNodes(item)
            worker_contract = self.web3.eth.contract(address=worker_addr, abi=abi)
            if worker_addr.lower()==self.config['worker'].lower():
                self.worker_contract = worker_contract

        self.get_account()
        if get_status_by_number(self.worker_contract.call().currentState()) == "offline":
            self.worker_contract.transact({'from':self.config['account']}).alive()

#var myContract = contractAbi.at(contractAddress);
#// suppose you want to call a function named myFunction of myContract
#var getData = myContract.myFunction.getData(function parameters);
#//finally paas this data parameter to send Transaction
#web3.eth.sendTransaction({to:Contractaddress, from:Accountaddress, data: getData});
