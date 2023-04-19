import sys
import time

# Progress bar class
# https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console

class ProgressBar:
    def __init__(self, total, prefix='', suffix='', decimals=1, length=100, fill='#', print_end='\r'):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.decimals = decimals
        self.length = length
        self.fill = fill
        self.print_end = print_end
        self.start_time = time.time()
        self.progress = 0

    def update(self, progress):
        self.progress = progress
        percent = ("{0:." + str(self.decimals) + "f}").format(100 * (progress / float(self.total)))
        filled_length = int(self.length * progress // self.total)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)
        print(f'\r{self.prefix} |{bar}| {percent}% {self.suffix}', end=self.print_end)
        # Print New Line on Complete
        if progress == self.total:
            print()

    def increment(self):
        self.update(self.progress + 1)

    def elapsed_time(self):
        return time.time() - self.start_time

    def estimated_time(self):
        elapsed = self.elapsed_time()
        if self.progress > 0:
            estimated = elapsed * (self.total / self.progress - 1)
        else:
            estimated = 0
        return estimated

    def remaining_time(self):
        estimated = self.estimated_time()
        remaining = estimated - self.elapsed_time()
        return remaining

