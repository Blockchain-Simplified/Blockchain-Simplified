from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64


def genrateKeys(private_key_path, public_key_path):
    private_key = RSA.generate(1024)
    public_key = private_key.publickey()
    private_pem = private_key.exportKey().decode()
    public_pem = public_key.exportKey().decode()
    with open(private_key_path, 'w') as pr:
        pr.write(private_pem)
    with open(public_key_path, 'w') as pu:
        pu.write(public_pem)


def decryptData(private_key_path, ciperText):
    cp = base64.decodebytes(ciperText.encode())
    pr_key = RSA.importKey(open(private_key_path, 'r').read())
    de = PKCS1_OAEP.new(key=pr_key)
    return str(de.decrypt(cp).decode())

def encryptData(public_key_path, message):
    pb_key = RSA.importKey(open(public_key_path).read())
    cipher = PKCS1_OAEP.new(key=pb_key)
    return base64.b64encode(cipher.encrypt(str(message).encode())).decode()


def saveKeyinFile(name, actual_key_in_str):
    with open(name, 'w') as pr:
        pr.write(actual_key_in_str)
    

# ss = open('public.pem').read()
# saveKeyinFile('test.pem', ss)

# genrateKeys('private.pem', 'public.pem')
# cipher = encryptData('test.pem', 'hello')
# print("Cipher Text", cipher)
# print("Normal Text", decryptData('private.pem', cipher))