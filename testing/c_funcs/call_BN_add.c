
# include <stdio.h>
# include <stdlib.h>
# include <openssl/bn.h>
# include <openssl/crypto.h>


// Testing the different functions e.g.BN_ADD, BN_SQRRT MOD, call in python ! und dann laufen lassen ?
int main()
{
    const char a[] = "12345";
    const char b[] = "12345";

    BIGNUM *bn1 = NULL;
    BN_dec2bn(&bn1, a);

    BIGNUM *bn2 = NULL;
    BN_dec2bn(&bn2, b);

    BIGNUM *bn3 = BN_new();
    BN_add(bn3, bn1, bn2);

    char *n3 = BN_bn2dec(bn3);
    printf("%s\n%s\n%s\n", a, b, n3);
    OPENSSL_free(n3); // don't forget to free this.
    
    BN_free(bn1);
    BN_free(bn2);
    BN_free(bn3);

    return 0;
}



