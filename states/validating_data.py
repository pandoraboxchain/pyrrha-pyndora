from base import State

class ValodatingData(State):

    def on_event(self, event):
        return self
