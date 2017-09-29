from states.idle import Idle

class Worker():

    def __init__(self):
        self.state = Idle()

if __name__ == '__main__':
    Worker()
