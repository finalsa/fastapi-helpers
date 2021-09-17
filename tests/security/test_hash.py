from unittest import TestCase
from fastapi_utils import Encoder


class SecurityTest(TestCase):

    def test_hash(self,):
        encoded = Encoder.encode("hola")
        decoded = Encoder.decode(encoded)
        self.assertEqual("hola", decoded, "Encoder base64 failed.")
    
    def test_pass_hash(self,):
        _hash = Encoder.ph.hash("hola")

        self.assertTrue(Encoder.ph.verify(_hash, "hola"))
