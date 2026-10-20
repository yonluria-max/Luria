import base64
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


class CryptoManager:

  def __init__(self, private_key=None, public_key=None):
    if private_key and public_key:
      self.private_key = private_key
      self.public_key = public_key
    else:
      self.private_key, self.public_key = self.generate_key_pair()

  @staticmethod
  def generate_key_pair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

  def sign_data(self, data: str) -> str:
    signature = self.private_key.sign(
        data.encode("utf-8"),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return base64.b64encode(signature).decode("utf-8")

  @staticmethod
  def verify_signature(
      data: str, signature_b64: str, public_key_pem: str
  ) -> bool:
    try:
      public_key = serialization.load_pem_public_key(
          public_key_pem.encode("utf-8")
      )
      signature = base64.b64decode(signature_b64.encode("utf-8"))
      public_key.verify(
          signature,
          data.encode("utf-8"),
          padding.PSS(
              mgf=padding.MGF1(hashes.SHA256()),
              salt_length=padding.PSS.MAX_LENGTH,
          ),
          hashes.SHA256(),
      )
      return True
    except (InvalidSignature, Exception):
      return False

  def get_public_key_pem(self) -> str:
    pem = self.public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pem.decode("utf-8")