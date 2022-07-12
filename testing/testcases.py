# call openssl functions 
# Es gibt wrapper für openssl
# call c code/functions in python

# imports
import ctypes

# call c function
fun = ctypes.CDLL("openssl/bn_sqrt.c")

print(fun)