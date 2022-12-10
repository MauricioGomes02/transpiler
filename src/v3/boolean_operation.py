import common

class BooleanOperation:
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def generate_code(self):
        left_expression = self.left.generate_code()
        right_expression = self.right.generate_code()
        
        boolean_operation_code = []        
        boolean_operation_code.extend(left_expression)
        boolean_operation_code.append('\n\t')
        boolean_operation_code.extend(right_expression)
        boolean_operation_code.append('\n\t')
        boolean_operation_code.append('STORE tmp_value')
        boolean_operation_code.append('\n\t')
        boolean_operation_code.append('CMP LOAD tmp_value')
        boolean_operation_code.append('\n\t')

        false_label = common.create_label()
        true_label = common.create_label()

        if self.operator == '==':
            boolean_operation_code.append(f'JZ {true_label}')
            boolean_operation_code.append('\n\t')
            boolean_operation_code.append(f'JP {false_label}')                        
        elif self.operator == '>':
            boolean_operation_code.append(f'JMORE {true_label}')
            boolean_operation_code.append('\n\t')
            boolean_operation_code.append(f'JP {false_label}')
        elif self.operator == '<':
            boolean_operation_code.append(f'JLESS {true_label}')
            boolean_operation_code.append('\n\t')
            boolean_operation_code.append(f'JP {false_label}')
        elif self.operator == '>=':
            boolean_operation_code.append(f'JLESS {false_label}')
            boolean_operation_code.append('\n\t')
            boolean_operation_code.append(f'JP {true_label}')
        elif self.operator == '<=':
            boolean_operation_code.append(f'JMORE {false_label}')
            boolean_operation_code.append('\n\t')
            boolean_operation_code.append(f'JP {true_label}')

        boolean_operation_code.append('\n')
        boolean_operation_code.append(true_label)
        boolean_operation_code.append('\n\t')
        boolean_operation_code.append('PUSH 1')
        boolean_operation_code.append('\n')
        boolean_operation_code.append(false_label)
        boolean_operation_code.append('\n\t')
        boolean_operation_code.append('PUSH 0')
        boolean_operation_code.append(f'\n{common.create_label()}')

        return boolean_operation_code