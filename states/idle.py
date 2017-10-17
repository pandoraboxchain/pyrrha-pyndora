from states.base import State
from states.validating_data import ValidatingData
from states.assigned import Assigned
from states.events.cognitive_job_created import CognitiveJobCreated
from states.events.assigned_to_job import AssignedToJob
from states.events.validation_started import ValidationStarted

class Idle(State):

    def on_event(self, event):
        if type(event) == CognitiveJobCreated:
            contract = event.job_contract
            count = contract.call().activeWorkersCount()
            for item in range(count):
                worker = contract.call().activeWorkers(item)
                if worker.lower() == self.worker.eth.worker_contract.address.lower():
                    self.change_state(Assigned())
                    self.worker.state.on_event(AssignedToJob(contract, event.job_contract_address))
        return self
