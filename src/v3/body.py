class Body:
  def __init__(self, body_statements):
    self.body_statements = body_statements

  def generate_code(self, scope):
    body_code = []
    for body in reversed(self.body_statements):
      body_code.append('\n\t')
      body_code.extend(body.generate_code(scope))

    body_code.append('\n\t')
    body_code.append('RET')
    
    return body_code