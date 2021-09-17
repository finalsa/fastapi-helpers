import base64
import argon2


class Encoder:

    ph = None

    def __init__(self):
        self.ph = argon2.PasswordHasher(time_cost=3)
        super().__init__()

    def encode(self, word):
        base64_message = word
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64encode(base64_bytes)
        message = message_bytes.decode('ascii')
        base64_message = message
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64encode(base64_bytes)
        encode = message_bytes.decode('ascii')
        return encode

    def decode(self, word):
        base64_message = word
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        base64_message = message
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        decode = message_bytes.decode('ascii')
        return decode


encoder = Encoder()
