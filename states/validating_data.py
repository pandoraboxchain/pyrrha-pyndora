from states.base import State
from states.events.validation_started import ValidationStarted
from ipfs.dataset import get_dataset
from ipfs.kernel import get_kernel
from cognitive_work.cognitive_work import load

class ValodatingData(State):

    def on_event(self, event):
        if type(event) == CognitiveJobCreated:
            contract = event.contract
            kernel_ipfs = contract.call().kernel()
            dataset_ipfs = contract.call().dateset()
            dataset_data = get_dataset(self.worker.ipfs, dataset_ipfs)
            kernel_data = get_kernel(self.worker.ipfs, kernel_ipfs)
            config = self.worker.ipfs.config
            try:
                result = load(kernel_data['model'], kernel_data['weights'], dataset_data[0], config['data_path'])
            except:
                print('ValodatingData error')
        return self
