import time
from block import Block


class Blockchain:

  def __init__(self):
    self.chain = []
    self.create_genesis_block()

  def create_genesis_block(self):
    genesis_block = Block(
        index=0,
        ip_address="0.0.0.0",
        previous_hash="0" * 64,
        timestamp=0.0,
        signature="GENESIS",
    )
    self.chain.append(genesis_block)

  def get_latest_block(self) -> Block:
    return self.chain[-1]

  def add_block(self, new_block: Block) -> bool:
    if not self.is_valid_new_block(new_block, self.get_latest_block()):
      return False
    self.chain.append(new_block)
    return True

  def create_and_add_block(self, ip_address: str, signature: str = "") -> Block:
    latest_block = self.get_latest_block()
    new_block = Block(
        index=latest_block.index + 1,
        ip_address=ip_address,
        previous_hash=latest_block.hash,
        signature=signature,
    )
    if self.add_block(new_block):
      return new_block
    return None

  def is_valid_new_block(self, new_block: Block, previous_block: Block) -> bool:
    if previous_block.index + 1 != new_block.index:
      return False
    if previous_block.hash != new_block.previous_hash:
      return False
    if new_block.calculate_hash() != new_block.hash:
      return False
    return True

  def is_chain_valid(self) -> bool:
    for i in range(1, len(self.chain)):
      current_block = self.chain[i]
      previous_block = self.chain[i - 1]
      if not self.is_valid_new_block(current_block, previous_block):
        return False
    return True

  def get_all_blacklisted_ips(self) -> list:
    blacklisted_ips = []
    for block in self.chain[1:]:
      if block.ip_address and block.ip_address not in blacklisted_ips:
        blacklisted_ips.append(block.ip_address)
    return blacklisted_ips