from states.base import State
from states.validating_data import ValidatingData
from states.events.cognitive_job_created import CognitiveJobCreated
from states.events.validation_started import ValidationStarted
from states.events.assigned_to_job import AssignedToJob

class Assigned(State):

    def on_event(self, event):
        if type(event) == AssignedToJob:
            contract = event.job_contract
            count = contract.call().activeWorkersCount()
            for item in range(count):
                worker = contract.call().activeWorkers(item)
                if worker.lower() == self.worker.eth.worker_contract.address.lower():
                    #self.worker.eth.assign_job()
                    self.change_state(ValidatingData())
                    self.worker.state.on_event(ValidationStarted(contract, event.job_contract_address))
        return self
