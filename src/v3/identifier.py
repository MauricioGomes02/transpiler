class Identifier:
    def __init__(self, value, line):
        self.value = value
        self.line = line

    def generate_code(self, scope):
        return self.value
