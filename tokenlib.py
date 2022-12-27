import sys
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadTimeSignature
import random, hashlib

ERROR = 0
SUCCESS = 1
EXPIRED = 2
BAD = 3

def generateStrangeString():
    md = hashlib.md5()
    md.update(str(random.random()).encode("utf-8"))
    s = md.hexdigest()
    return s

if 'restart' in sys.argv:
    SECRET_KEY = generateStrangeString()
    SALT = generateStrangeString()
    with open('tokengen.cfg', 'w') as f:
        f.write(SECRET_KEY + '\n' + SALT)
else:
    with open('tokengen.cfg') as f:
        SECRET_KEY, \
        SALT = map(lambda s: s[:-1], f)
EXPIRES_IN = 36000000

def generateToken(data):
    global SECRET_KEY, SALT, EXPIRES_IN
    s = TimedJSONWebSignatureSerializer(secret_key=SECRET_KEY, expires_in=EXPIRES_IN, salt=SALT)
    return s.dumps(data).decode('ascii')

def readToken(token):
    global SECRET_KEY, SALT, EXPIRES_IN
    global ERROR, SUCCESS, EXPIRED, BAD
    s = TimedJSONWebSignatureSerializer(secret_key=SECRET_KEY, salt=SALT)
    st = ERROR
    data = {}
    try:
        data = s.loads(token)
        st = SUCCESS
    except SignatureExpired:
        st = EXPIRED
    except BadTimeSignature:
        st = BAD
    return st, data
