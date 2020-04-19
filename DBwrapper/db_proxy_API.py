from .Wrapper import Wrapper

class DBproxy:

    def __init__(self, config_file=None):
        self.db = Wrapper(None,config_file)



    def save_coversation(self):

