class Number:
    def __init__(self, value):
        self.value = value

    def generate_code(self):
        return [f'PUSH {self.value}']