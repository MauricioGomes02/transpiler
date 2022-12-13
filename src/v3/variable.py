import json


class Variable:
    def __init__(self, template, value):
        self.template = template
        self.value = value

    def generate_code(self, scope):
        symbol = scope.get_symbol(self.value)
        local_scope = scope.get_parent()
        while symbol is None and local_scope is not None:
            symbol = local_scope.get_symbol(self.value)
            local_scope = local_scope.get_parent()

        return [f'LOAD {symbol.name}']

    def validate_symbols(self, scope):
        symbol = scope.get_symbol(self.value)
        local_scope = scope.get_parent()
        while symbol is None and local_scope is not None:
            symbol = local_scope.get_symbol(self.value)
            local_scope = local_scope.get_parent()

        if symbol is None:
            raise Exception('Undefined')