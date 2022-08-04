#include "bo_heartbleed.c"
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>


void trigger_heartbleed(char *input) {
    int ret;

    /* make SSL dummy from input */
    SSL ssl_dummy;
    SSL3_RECORD rrec;
    struct ssl3_state_st s3;
    ssl_dummy.msg_callback = NULL;
    rrec.data = (unsigned char*) input;
    s3.rrec = rrec;
    ssl_dummy.s3 = &s3;

    /* call target function */
    ret = tls1_process_heartbeat(&ssl_dummy);
}


#define BUFF_SIZE 128
int main(int argc, char **argv) {

    /* read from stdin to char* */
    char buff[BUFF_SIZE];
    read(STDIN_FILENO, buff, BUFF_SIZE);

    /* wrap to SSL and call tls_hb*/
    trigger_heartbleed(buff);
    return 0;
}