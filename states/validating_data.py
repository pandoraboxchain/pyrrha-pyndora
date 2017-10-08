from states.base import State
from states.events.validation_started import ValidationStarted
from states.events.cognitive_job_created import CognitiveJobCreated
from ipfs.dataset import get_dataset
from ipfs.kernel import get_kernel
from cognitive_work.cognitive_work import load

class ValidatingData(State):

    def on_event(self, event):
        if type(event) == ValidationStarted:
            import pdb; pdb.set_trace()
            contract = event.job_contract
            #kernel_ipfs = contract.call().kernel()
            kernel_ipfs = self.worker.eth.get_kernel(contract.call().kernel())
            dataset_ipfs = self.worker.eth.get_dataset(contract.call().dataset())
            dataset_data = get_dataset(self.worker.ipfs, dataset_ipfs)
            kernel_data = get_kernel(self.worker.ipfs, kernel_ipfs)
            config = self.worker.ipfs.config
            try:
                result = load(kernel_data['model'], kernel_data['weights'], dataset_data[0], config['data_path'])
            except:
                print('ValidatingData error')
        return self
