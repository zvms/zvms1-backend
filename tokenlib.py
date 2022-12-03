from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadTimeSignature
import random, hashlib
import oppressor as OP
import database as DB
import sys

ERROR = 0
SUCCESS = 1
EXPIRED = 2
BAD = 3

def generateStrangeString():
    md = hashlib.md5()
    md.update(str(random.random()).encode("utf-8"))
    s = md.hexdigest()
    return s

if len(sys.argv) > 1 and sys.argv[1].lower() == 'restart':
    DB.execute('TRUNCATE log')
    SECRET_KEY = generateStrangeString()
    SALT = generateStrangeString()
    with open('tokengen.cfg', 'w') as f:
        f.write(SECRET_KEY + '\n' + SALT)
else:
    with open('tokengen.cfg') as f:
        SECRET_KEY, SALT = f
    
EXPIRES_IN = 36000000

def next():
    DB.execute('INSERT INTO log VALUES()')
    fl, r = OP.select('MAX(id)', 'log', 'true', (), ['max'])
    return r['max']

def exists(data):
    fl, r = OP.select('*', 'log', 'id=%s', (data['logid'], ), [''])
    return fl

def remove(token_data):
    DB.execute('DELETE FROM log WHERE id=%s', token_data['logid'])

def generateToken(data):
    s = TimedJSONWebSignatureSerializer(secret_key=SECRET_KEY, expires_in=EXPIRES_IN, salt=SALT)
    return s.dumps(data).decode('ascii')

def readToken(token):
    s = TimedJSONWebSignatureSerializer(secret_key=SECRET_KEY, salt=SALT)
    st = ERROR
    data = {}
    try:
        data = s.loads(token)
        st = SUCCESS
        if not exists(data):
            st = BAD
    except SignatureExpired:
        st = EXPIRED
    except BadTimeSignature:
        st = BAD
    return st, data
