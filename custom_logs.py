import logging
import sys

class Log:
    def __init__(self, filename):
        self.filename = filename

    def log(self, message: str):
        with open(self.filename, 'a') as file:
            file.write(message)
