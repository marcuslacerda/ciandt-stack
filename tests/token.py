import datetime
import time
import jwt
from jwt import DecodeError, ExpiredSignature

jwt_payload = jwt.encode({
    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
}, 'secret')

time.sleep(32)

# JWT payload is now expired
# But with some leeway, it will still validate
try:
    jwt.decode(jwt_payload, 'secret')
except ExpiredSignature as e:
    print "ExpiredSignature"


print "Try again"
options = {
    'verify_exp': False,
}
token = jwt.decode(jwt_payload, 'secret', options=options)
print token
