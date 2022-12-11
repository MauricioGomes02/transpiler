class Body:
  def __init__(self, body_statements):
    self.body_statements = body_statements

  def generate_code(self):
    body_code = []
    for body in reversed(self.body_statements):
      body_code.extend(body.generate_code())
    
    return body_code