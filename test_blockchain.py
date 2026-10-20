from block import Block
from blockchain import Blockchain


def run_tests():
  bc = Blockchain()

  # 1. הוספת בלוקים תקינים
  bc.create_and_add_block(ip_address="192.168.1.50")
  bc.create_and_add_block(ip_address="10.0.0.1")

  print("Chain length:", len(bc.chain))
  print("Is chain valid?", bc.is_chain_valid())
  print("Blacklisted IPs:", bc.get_all_blacklisted_ips())

  # 2. ניסיון זיוף - שינוי IP בבלוק קיים
  bc.chain[1].ip_address = "99.99.99.99"
  print("Is chain valid after tampering?", bc.is_chain_valid())


if __name__ == "__main__":
  run_tests()