class Number:
    def __init__(self, value):
        self.value = value

    def generate_code(self, scope):
        return [f'PUSH {self.value}']

    def validate_symbols(self, scope):
        return