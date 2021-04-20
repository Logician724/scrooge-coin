from Crypto.Hash import SHA3_512

latest_block_id = 0

class Block:
  
  def __init__(self, prev_block_hash = None):
    self.transactions = {}
    self.prev_block_hash = prev_block_hash
    self.signature = ''
    self.update_hash()
    self.id = Block.gen_id()
  
  @staticmethod
  def gen_id():
    global latest_block_id
    id = latest_block_id
    latest_block_id += 1
    return id
  
  def __repr__(self):
    transactions = self.transactions.values()
    transactions_str = ''
    for transaction in transactions:
      transactions_str += str(transaction)
    return 'ID: '+ str(self.id) + '\n' + 'Transactions: ' + str(len(transactions)) +'\n' + transactions_str  + '\n' + 'Previous Block: ' +  str(self.prev_block_hash) + '\n' + 'Signature: ' + str(self.signature) + '\n'
  
  def add_transaction(self, transaction):
    if len(self.transactions) < 10:    
      self.transactions[transaction.hash.digest()] =  transaction
      self.update_hash()
    else:
      raise Exception('This block is full')
  def __repr__(self):
    return 'Block ' + str(self.id) + ' \n' + 'Transactions: ' + str(self.transactions) + ' \n' + 'Prev Block Hash: ' + str(self.prev_block_hash) + '\n'

  def update_hash(self):
    self.hash = SHA3_512.new(str.encode(str(self.transactions)+ str(self.prev_block_hash)))
