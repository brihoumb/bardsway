import rsa


class BardswayRSA():
    __pub = None
    __priv = None
    __public_key = '-----BEGIN RSA PUBLIC KEY-----\nMEgCQQCRZtEi9Fktf5aq9v' +\
                   'X8WGW5XWhuueUH3CQXWL4x5nrtWYeNXvF8zl7V9RT1\nllegQomKMs/' +\
                   'mSxpcJaumGkyHeiftAgMBAAE=\n-----END RSA PUBLIC KEY-----\n'
    __private_key = '-----BEGIN RSA PRIVATE KEY-----\nMIIBPAIBAAJBAJFm0SL0' +\
                    'WS1/lqr29fxYZbldaG655QfcJBdYvjHmeu1Zh41e8XzO\nXtX1FPWW' +\
                    'V6BCiYoyz+ZLGlwlq6YaTId6J+0CAwEAAQJAQv5Qlf5nqGMFFLi9Fg' +\
                    'vU\nsteq6nmUYU65AljNKUi8TPXYdktgfvGptByH/n8HA1EvQR5OXp' +\
                    'A4RS7Udieh6P0h\nAQIjAJfOV+9nJHrtgeECJbRmNOQXsQZkVFuZvQ' +\
                    'z7ODjOmiFwMLECHwD1MynxnCuY\nhl+u2egU2WCGbKWqJrMLK5fsB/' +\
                    'yU2f0CIjIJCADXjTWbTQC99XGFco9vo6CItylN\n/frmXrySlEjLMr' +\
                    'ECHwCmJ8eSfBtmvhf0qqEED9HDBbi1Nog5V48ZWMgmLhkCIkcS\nTM' +\
                    'u1o4C/2IpLHIJHLYv9UjiwoKbpx6vta0POL1/s/B8=\n' +\
                    '-----END RSA PRIVATE KEY-----\n'

    def __init__(self):
        self.__public_key = self.__public_key.encode()
        self.__private_key = self.__private_key.encode()
        self.__pub = rsa.PublicKey.load_pkcs1(self.__public_key)
        self.__priv = rsa.PrivateKey.load_pkcs1(self.__private_key)
        pass

    def encrypt(self, message):
        return rsa.encrypt(message.encode(), self.__pub).hex()

    def decrypt(self, cypher):
        return rsa.decrypt(bytes.fromhex(cypher), self.__priv).decode()
