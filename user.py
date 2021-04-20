from Crypto.PublicKey import DSA 
from utils import Utils
from Crypto.Hash import SHA3_512
from scrooge import Scrooge

latest_user_id = 0
class User:
  def __init__(self, scrooge: Scrooge):
    # generate private/public key pair
    self.key = DSA.generate(1024)
    self.scrooge = scrooge
    self.coins = {}
    # Only for the purpose of simulating double spending
    self.double_spending_coins = {}
    self.id = User.gen_id()

  def receive(self, coins):
    self.coins.update(coins)
  
  def pay(self, amount, recepient_pk, double_spend=False):
    consumed_coins = {}
    coins = None
    if double_spend:
      coins = self.double_spending_coins
    else:
      coins = self.coins
    # create a new dictionary with the coins to be paid in the transaction
    if amount > len(coins):
      if double_spend:
        print('User ' + str(self.id) + ' has not made enough transactions to simulate a double spend with. As user only has ' + str(len(coins)) + ' coins to double spend.' )
      else:
        print('User ' + str(self.id) +' does not have enough coins. User only has ' + str(len(coins)) + ' coins.')
    else:
      coin_ids = coins.copy().keys()
      temp_double_spend = {}
      for id in coin_ids:
        consumed_coins[id] = coins.pop(id)
        temp_double_spend[id] = consumed_coins[id]
        if len(consumed_coins) == amount:
          break
      message = SHA3_512.new(str.encode(str(consumed_coins) + str(recepient_pk)))
      signature = Utils.sign(self.key, message)
      result = self.scrooge.register_payment(self.key.publickey().export_key(),signature,recepient_pk,consumed_coins)
      if result:
        print('User ' + str(self.id) +' payment was successful. User now has ' + str(len(self.coins)) + ' coins.')
        if not double_spend:
          self.double_spending_coins = {**self.double_spending_coins, **temp_double_spend}
  def __repr__(self):
    return 'User ' + str(self.id) + '\n key: ' + str(self.key.publickey().export_key()) + '\n' + 'Coins: ' + str(len(self.coins)) + '\n'

  @staticmethod
  def gen_id():
    global latest_user_id
    id = latest_user_id
    latest_user_id += 1
    return id
