from Crypto.Hash import SHA3_512

latest_transaction_id = 0

class Transaction:
  def __init__(self, recepient_pk):
    self.id = Transaction.gen_id()
    self.recepient_pk = recepient_pk
  @staticmethod
  def gen_id():
    global latest_transaction_id
    id = latest_transaction_id
    latest_transaction_id += 1
    return id

class CreateCoinsTransaction(Transaction):
  def __init__(self, amount, recepient_pk):
    super().__init__(recepient_pk)
    
    self.coins = []
    for i in range(amount):
      self.coins.append(str(self.id) + '/' + str(i))
    self.hash = SHA3_512.new(str.encode(str(self.coins) + str(self.recepient_pk)))  
  def __repr__(self):
    return 'Transaction ' + str(self.id) + '\nCoin IDS: '+  str(self.coins) + '\n' + 'Transaction Hash: ' +  str(self.hash.digest()) + '\n'


class PayCoinsTransaction(Transaction):
  def __init__(self,sender_pk, sender_signature, recepient_pk, coins):
    super().__init__(recepient_pk)
    self.sender_pk = sender_pk
    self.sender_signature = sender_signature
    self.recepient_pk = recepient_pk
    self.coins = coins
    self.hash = SHA3_512.new(str.encode(str(sender_pk) + str(sender_signature)+ str(recepient_pk) + str(coins)))
  def __repr__(self):
    return 'Transaction ' + str(self.id) + '\nPaid Coins: \n' + str(self.coins) + '\n sender_pk ' + str(self.sender_pk) + '\n recepient_pk: ' + str(self.recepient_pk) + '\n'
