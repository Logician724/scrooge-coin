class Block:
  def __init__(self):
    self.transactions = {}
    self.hash = hash(str(self.transactions))

  def add_transaction(self, transaction):
    if len(self.transactions) < 10:    
      self.transactions.add(transaction)
      self.hash = hash(str(self.transactions))
    else:
      raise Exception('This block is full')