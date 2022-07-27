# call openssl functions 
# Es gibt wrapper für openssl
# call c code/functions in python
# command co create shared files : cc -fPIC -shared -o bn_sqrt.so openssl/bn_sqrt.c
# imports
from ctypes import * 
from OpenSSL import SSL, crypto
import pem
import glob

#so_file = "/Users/janavihs/projects/anomaly-detection-software/testing/my_functions.so"
# call c function
#fun = CDLL(so_file)
#print(fun.square(10))

# get certificate
cert = "anomaly-detection-software/testing/certs/cert.pem"



with open(cert, 'rb') as f:
   certs = pem.parse(f.read())
   print(crypto.FILETYPE_PEM(certs))

print(certs)
crypto.get_elliptic_curves()


root_certs = SSL._CERTIFICATE_PATH_LOCATIONS

for certs in glob.glob("/etc/ssl/certs/*.pem"):
    print(certs)