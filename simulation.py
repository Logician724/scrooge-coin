from scrooge import Scrooge
from user import User
import random
import sys
import keyboard
sys.stdout = open('out.txt', 'w')

print('Initializing Scrooge')
scrooge = Scrooge()
for i in range(0, 10):
  print('Creating User ' + str(i))
  new_user = User(scrooge)
  scrooge.users[str(new_user.key.publickey().export_key())]=new_user
for user_key in scrooge.users.keys():
  scrooge.create_coins(10, user_key)
users = list(scrooge.users.items())

print('=============================================\n')
print('Printing users')
print('=============================================\n')
for user in scrooge.users.values():
  print(user)
print('=============================================\n')
print('Simulating transactions. Some of these transactions are double spending at random.')
print('This simulation does not end. You can terminate by pressing on space')
print('=============================================\n')
while True:
  try:
    if keyboard.is_pressed('space'):
      print('You pressed on space! Terminating')
      sys.exit()
    sender = random.choice(users)
    recepient = random.choice(users)
    # Sender Pays a Random Amound between 1 and 10
    amount = random.randint(1,10)
    print('User ' + str(sender[1].id)+ ' is sending ' + str(amount) + ' coins to user ' + str(recepient[1].id))
    sender[1].pay(amount,recepient[0], double_spend=bool(random.getrandbits(1)))
  except Exception as e: print(e)

print('=============================================\n')
print('Simulation is over.')
print('=============================================\n')
