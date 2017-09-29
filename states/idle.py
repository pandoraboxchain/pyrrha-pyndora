from states.base import State

class Idle(State):

    def on_event(self, event):
        return self
