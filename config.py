import configparser


class Config:
    def __init__(self, param_file):
        self.config = configparser.ConfigParser()
        self.config.read(param_file)

        self.input_dir = self.config.get('input', 'input_dir')
        self.output_file = self.config.get('output', 'output_file')
        self.fps = self.config.getint('output', 'fps')
        self.start = self.config.getint('input', 'start', fallback=0)
        self.end = self.config.getint('input', 'end', fallback=None)
        self.duration = self.config.getfloat('output', 'duration', fallback=1)
        self.slow = self.config.get('output', 'slow', fallback='')

    def get_input_files(self):
        file_list = os.listdir(self.input_dir)
        file_list.sort()
        file_list = file_list[self.start:self.end]
        return file_list

