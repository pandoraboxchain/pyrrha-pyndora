from states.base import State
from states.events.computing_started import ComputingStarted
from states.events.cognitive_job_created import CognitiveJobCreated
from ipfs.dataset import get_dataset
from ipfs.kernel import get_kernel
from cognitive_work.cognitive_work import load

class ValidatingData(State):

    def on_event(self, event):
        if type(event) == ComputingStarted:
            contract = event.job_contract
            kernel_ipfs = self.worker.eth.get_kernel(contract.call().kernel())
            dataset_ipfs = self.worker.eth.get_dataset(contract.call().dataset())
            dataset_data = get_dataset(self.worker.ipfs, dataset_ipfs)
            kernel_data = get_kernel(self.worker.ipfs, kernel_ipfs)
            config = self.worker.ipfs.config
            try:
                result = load_and_run(kernel_data['model'], kernel_data['weights'], dataset_data[0], config['data_path'])
                self.worker.eth.provide_results(result)
            except:
                print('Error')
        return self
