import hashlib
import json
import time


class Block:

  def __init__(
      self,
      index: int,
      ip_address: str,
      previous_hash: str,
      timestamp: float = None,
      signature: str = "",
      block_hash: str = None,
  ):
    self.index = index
    self.timestamp = timestamp if timestamp is not None else time.time()
    self.ip_address = ip_address
    self.previous_hash = previous_hash
    self.signature = signature
    self.hash = block_hash if block_hash else self.calculate_hash()

  def calculate_hash(self) -> str:
    block_string = json.dumps(
        {
            "index": self.index,
            "timestamp": self.timestamp,
            "ip_address": self.ip_address,
            "previous_hash": self.previous_hash,
            "signature": self.signature,
        },
        sort_keys=True,
    )
    return hashlib.sha256(block_string.encode("utf-8")).hexdigest()

  def to_dict(self) -> dict:
    return {
        "index": self.index,
        "timestamp": self.timestamp,
        "ip_address": self.ip_address,
        "previous_hash": self.previous_hash,
        "signature": self.signature,
        "hash": self.hash,
    }

  @classmethod
  def from_dict(cls, data: dict) -> "Block":
    return cls(
        index=data["index"],
        ip_address=data["ip_address"],
        previous_hash=data["previous_hash"],
        timestamp=data["timestamp"],
        signature=data.get("signature", ""),
        block_hash=data.get("hash"),
    )

  def __repr__(self):
    return (
        f"<Block #{self.index} [IP: {self.ip_address}] Hash: {self.hash[:10]}...>"
    )