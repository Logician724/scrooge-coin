from transaction import Transaction
from transaction import CreateCoinsTransaction
from transaction import PayCoinsTransaction
from Crypto.PublicKey import DSA
from Crypto.Hash import SHA3_512
from block import Block
from utils import Utils

class Scrooge:
  def __init__(self):
    self.key = DSA.generate(2048)
    self.blocks = {}
    self.users = {}
    self.latest_block = Block()

  def create_coins(self, amount: int, recepient_pk: str):
    transaction = CreateCoinsTransaction(amount, recepient_pk)
    coins = {}
    for coin in transaction.coins:
      coins[coin] = transaction.hash.digest()
    self.users[recepient_pk].receive(coins)
    self.add_transaction(transaction)

  def register_payment(self, sender_pk, sender_signature, recepient_pk, coins):
    if sender_pk == recepient_pk:
      print('User ' + str(self.users[str(sender_pk)].id) + ' is trying to pay coins to himself. Scrooge rejecting')
      return
    if Utils.verify(SHA3_512.new(str.encode(str(coins) + str(recepient_pk))),sender_signature,sender_pk):
      for coin in coins.items():
        if not self.is_coin_valid(coin, str(sender_pk)):
          print('Detected Double Spending or coin does not belong to user')
          return False
      transaction = PayCoinsTransaction(str(sender_pk), sender_signature, recepient_pk, coins)
      new_coins = {}
      for id in coins.keys():
        new_coins[id]= transaction.hash.digest()
      self.users.get(recepient_pk).receive(new_coins)
      print('Transaction ' + str(transaction.id) + ' is getting added to the chain')
      self.add_transaction(transaction)
      return True
    else:
      print('Scrooge could not verify the transaction. Invalid signature')
      return False



  def add_transaction(self, transaction: Transaction):
    self.latest_block.add_transaction(transaction)
    print('Updated Blocks \n' + str(self.latest_block))
    if len(self.latest_block.transactions) == 10:
      self.latest_block.signature = Utils.sign(self.key,self.latest_block.hash)
      self.blocks[self.latest_block.hash.digest()] = self.latest_block
      self.latest_block = Block(self.latest_block.hash.digest())
      print('A new Block has been added to the chain. Chain Length = ' + str(len(self.blocks)))
      print(self.blocks)
  def is_coin_valid(self, coin, sender_pk):
    transaction = self.find_transaction(coin[1])
    # Make sure transaction belongs to user and no double spending happened
    if transaction.recepient_pk == sender_pk and not self.is_double_spending(coin, sender_pk):
      return True
    else:
      return False

  def is_double_spending(self, coin, sender_pk):
    # Go through all transactions in the block chain till we reach the transaction used for payment.
    current_block = self.latest_block

    while current_block is not None:
      # In case you find a transaction that was used for payment with this coin by the same payer 
      # after the transaction in question was made,  then this is a double spend!
      for transaction in current_block.transactions.values():
        
        if  transaction.hash.digest() != coin[1]:
          if (
            isinstance(transaction, PayCoinsTransaction) and
            transaction.sender_pk == sender_pk and
            coin in transaction.coins.items()):
            return True
        else:
          return False
      current_block = self.blocks.get(current_block.prev_block_hash)
    return False

  def find_transaction(self, transaction_hash):
    target_transaction = None
    current_block = self.latest_block
    while target_transaction is None:
      candidate_transaction = current_block.transactions.get(transaction_hash)
      if candidate_transaction is not None:
        target_transaction = candidate_transaction
      else:
        current_block = self.blocks.get(current_block.prev_block_hash)
        if current_block == None:
          raise Exception('Could not find transaction')
    return target_transaction
