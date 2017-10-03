from states.base import State
from states.events.cognitive_job_created import CognitiveJobCreated

class Idle(State):

    def on_event(self, event):
        if type(event) == CognitiveJobCreated:
            contract = event.contract
            count = contract.call().activeWorkersCount()
            for item in range(count):
                worker = contract.call().activeWorkers(item)
                    if worker == self.config['worker']:
                        self.change_state(ValodatingData(contract, event.address))
                        self.worker.state.on_event()
        return self
