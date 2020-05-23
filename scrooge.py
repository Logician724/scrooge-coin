from block import Block
from user import User
from transaction import Transaction
from transaction import CreateCoinsTransaction
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
class scrooge:
  def __init___(self):
    self.blocks={}
    self.user = User()
    self.add_block()

  def create_coins(self, amount, recepient):
    # TODO: Verify receiver public key
    transaction = CreateCoinsTransaction(amount, recepient)
    self.sign(transaction)
    try:
      self.latest_block.add(transaction)
    except:
      self.add_block(transaction)
  def add_block(self):
    block = Block()
    self.blocks.add(block)
    self.latest_block= block
  def add_block(self, transaction):
    block = Block()
    block.add_transaction(transaction)
    self.blocks.add(block)
  def sign(self, transaction: Transaction):
    signature = self.user.private_key.sign(hash(str(transaction.id) + str(transaction.coins)),
    padding.PSS(
      mgf=padding.MGF1(hashes.SHA256()),
      salt_length=padding.PSS.MAX_LENGTH)
    )
    transaction.sign(signature)