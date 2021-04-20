from Crypto.Signature import DSS
from Crypto.PublicKey import DSA 

class Utils:
  @staticmethod
  def sign(signer_key, message: str):
    signer = DSS.new(signer_key, 'fips-186-3')
    signature = signer.sign(message)
    return signature

  @staticmethod
  def verify(message_hash, signature, pub_key):
    verifier = DSS.new(DSA.import_key(pub_key), 'fips-186-3')
    try:
      verifier.verify(message_hash, signature)
      return True
    except ValueError:
      return False