import json


class Parser:
    def __init__(self, fn):
        self.fn = fn
        self.text = ""
        self.parsed_text = None

    def parse(self):
        if self.fn is not None:
            with open(self.fn, 'r') as file:
                self.text = file.read()
            file.close()

        self.parsed_text = json.loads(self.text)
        return self.parsed_text
