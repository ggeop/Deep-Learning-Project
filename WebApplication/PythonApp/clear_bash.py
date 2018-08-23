import os

class clear_bash(object):
    def __init__(self):
        self.clean()

    def clean(self):
        os.system('cls' if os.name == 'nt' else 'clear')
