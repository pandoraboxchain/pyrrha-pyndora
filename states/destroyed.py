from base import State

class Destroyed(State):

    def on_event(self, event):
        return self
