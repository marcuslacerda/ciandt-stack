import datetime
import time
import jwt
from jwt import ExpiredSignature
import unittest

class TokenTestCase(unittest.TestCase):

    def test_encode_token(self):
        """Token test: test expire feature."""
        jwt_payload = jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
        }, 'secret')

        time.sleep(12)
        # JWT payload is now expired
        # But with some leeway, it will still validate
        try:
            jwt.decode(jwt_payload, 'secret')
            self.fail(msg='Token must be expired')
        except ExpiredSignature:
            print "Expected ExpiredSignature Error"

        options = {'verify_exp': False}
        token = jwt.decode(jwt_payload, 'secret', options=options)
        self.assertIsNotNone(token)
