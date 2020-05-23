__id__ = 0

# Transaction.recipient = Public Key of Recepient
# Transaction.signature = Private Key of Sender

# TODO: Prev Hash
# TODO: Pay Transaction
class Transaction:
    def __init__(self):
        self.id = self.generate_id()
        self.coins = []
    
    def generate_id(self):
        global __id__
        __id__ += 1

        return __id__
    
    def sign(self, signature):
        self.signature = signature

class CreateCoinsTransaction(Transaction):
    def __init__(self, recepient, amount):
        super().__init__()

        self.recipient = recipient
        for i in range(amount):
            self.coins.append(self.id + ';' + i)

class PayCoinsTransaction(Transaction):
    def __init__(self):
        super().__init__()

        # TODO

print(PayCoinsTransaction().id)