# call openssl functions 
# Es gibt wrapper für openssl
# call c code/functions in python

# imports
import ctypes

# call c function
fun = ctypes.CDLL("c_func.so")

print(fun.square(10))