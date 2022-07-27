

### BN_mod_sqrt() 
returns the modular square root of a such that in^2 = a (mod p). The modulus p must be a prime, otherwise an error or an incorrect "result" will be returned. The result is stored into in which can be NULL. The result will be newly allocated in that case.


## Usage Openssl Create Elliptic Curves

###  find your curve
openssl ecparam -list_curves

### generate a private key for a curve
openssl ecparam -name prime256v1 -genkey -noout -out private-key.pem

### generate corresponding public key
openssl ec -in private-key.pem -pubout -out public-key.pem

### optional: create a self-signed certificate
openssl req -new -x509 -key private-key.pem -out cert.pem -days 360

# optional: convert pem to pfx
openssl pkcs12 -export -inkey private-key.pem -in cert.pem -out cert.pfx
