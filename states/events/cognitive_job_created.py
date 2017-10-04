from states.events.event import Event

class CognitiveJobCreated(Event):

    def __init__(self, job_contract, job_contract_address):
        self.job_contract = job_contract
        self.job_contract_address = job_contract_address
