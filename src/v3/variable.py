class Variable:
    def __init__(self, template, value, is_procedure = False):
        self.template = template
        self.value = value

    def generate_code(self):
        return [f'LOAD {self.value}']
