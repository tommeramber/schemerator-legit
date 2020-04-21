from .YamlConfigParser import YamlConfigParser


class GlobalConfig:
    def __init__(self, config_file_path):
        self.ConfigParser = YamlConfigParser()
        self.vars = self.ConfigParser.read_config_file(config_file_path)

# This is the Global configuration, its assign in main func.
global_config = None
