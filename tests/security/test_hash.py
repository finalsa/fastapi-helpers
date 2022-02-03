from unittest import TestCase
from fastapi_helpers import Encoder





def test_hash():
    encoded = Encoder.encode("hola")
    decoded = Encoder.decode(encoded)
    assert "hola" == decoded
    
def test_pass_hash():
    _hash = Encoder.ph.hash("hola")
    assert Encoder.ph.verify(_hash, "hola")
