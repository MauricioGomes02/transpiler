import common

class RelationalOperation:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def generate_code(self):
        left_code = self.left.generate_code()
        right_code = self.right.generate_code()

        # relational_operation_code = [f'\n{common.create_label()}']
        relational_operation_code = []
        relational_operation_code.append('\n\t')
        relational_operation_code.extend(left_code)
        relational_operation_code.append('\n\t')
        relational_operation_code.extend(right_code)
        relational_operation_code.append('\n\t')
        relational_operation_code.append(self.operator)

        return relational_operation_code