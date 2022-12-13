class String:
    def __init__(self, value):
        self.value = value

    def generate_code(self, scope):
        return [f'{self.value}']