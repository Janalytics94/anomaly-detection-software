#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct ssl_method_st SSL_METHOD;
typedef struct ssl_cipher_st SSL_CIPHER;
typedef struct ssl_st SSL;
typedef struct ssl_ctx_st SSL_CTX;
typedef struct buf_mem_st BUF_MEM;
typedef struct ssl_session_st SSL_SESSION;

struct ssl_session_st {
  int ssl_version; /* what ssl version session info is
                    * being kept in here? */

  /* only really used in SSLv2 */
  unsigned int key_arg_length;
  unsigned char key_arg[8];
  int master_key_length;
  unsigned char master_key[48];
  /* session_id - valid? */
  unsigned int session_id_length;
  unsigned char session_id[32];
  /* this is used to determine whether the session is being reused in
   * the appropriate context. It is up to the application to set this,
   * via SSL_new */
  unsigned int sid_ctx_length;
  unsigned char sid_ctx[32];
  char *psk_identity_hint;
  char *psk_identity;
  /* Used to indicate that session resumption is not allowed.
   * Applications can also set this bit for a new session via
   * not_resumable_session_cb to disable session caching and tickets. */
  int not_resumable;

  /* The cert is the certificate used to establish this connection */
  struct sess_cert_st /* SESS_CERT */ *sess_cert;
  /* when app_verify_callback accepts a session where the peer's certificate
   * is not ok, we must remember the error for session reuse: */
  long verify_result; /* only for servers */

  int references;
  long timeout;
  long time;

  unsigned int compress_meth; /* Need to lookup the method */

  const SSL_CIPHER *cipher;
  unsigned long cipher_id; /* when ASN.1 loaded, this
                            * needs to be used to load
                            * the 'cipher' structure */

  /* These are used to make removal of session-ids more
   * efficient and to implement a maximum cache size. */
  struct ssl_session_st *prev, *next;
};

struct buf_mem_st {
  size_t length; /* current number of bytes */
  char *data;
  size_t max; /* size of buffer */
  unsigned long flags;
};

struct ssl_ctx_st {
  const SSL_METHOD *method;
  unsigned long session_cache_size;
  struct ssl_session_st *session_cache_head;
  struct ssl_session_st *session_cache_tail;

  /* This can have one of 2 values, ored together,
   * SSL_SESS_CACHE_CLIENT,
   * SSL_SESS_CACHE_SERVER,
   * Default is SSL_SESSION_CACHE_SERVER, which means only
   * SSL_accept which cache SSL_SESSIONS. */
  int session_cache_mode;

  /* If timeout is not 0, it is the default timeout value set
   * when SSL_new() is called.  This has been put in to make
   * life easier to set things up */
  long session_timeout;

  struct {
    int sess_connect;             /* SSL new conn - started */
    int sess_connect_renegotiate; /* SSL reneg - requested */
    int sess_connect_good;        /* SSL new conne/reneg - finished */
    int sess_accept;              /* SSL new accept - started */
    int sess_accept_renegotiate;  /* SSL reneg - requested */
    int sess_accept_good;         /* SSL accept/reneg - finished */
    int sess_miss;                /* session lookup misses  */
    int sess_timeout;             /* reuse attempt on timeouted session */
    int sess_cache_full;          /* session removed due to full cache */
    int sess_hit;                 /* session reuse actually done */
    int sess_cb_hit;              /* session-id that was not
                                   * in the cache was
                                   * passed back via the callback.  This
                                   * indicates that the application is
                                   * supplying session-id's from other
                                   * processes - spooky :-) */
  } stats;

  int references;

  void *app_verify_arg;
  /* before OpenSSL 0.9.7, 'app_verify_arg' was ignored
   * ('app_verify_callback' was called with just one argument) */

  /* Default password callback user data. */
  void *default_passwd_callback_userdata;

  /* cookie generate callback */
  int (*app_gen_cookie_cb)(SSL *ssl, unsigned char *cookie,
                           unsigned int *cookie_len);

  /* verify cookie callback */
  int (*app_verify_cookie_cb)(SSL *ssl, unsigned char *cookie,
                              unsigned int cookie_len);

  /* Default values used when no per-SSL value is defined follow */

  void (*info_callback)(const SSL *ssl, int type,
                        int val); /* used if SSL's info_callback is NULL */

  /* Default values to use in SSL structures follow (these are copied by
   * SSL_new) */

  unsigned long options;
  unsigned long mode;
  long max_cert_list;

  struct cert_st /* CERT */ *cert;
  int read_ahead;

  /* callback that allows applications to peek at protocol messages */
  void (*msg_callback)(int write_p, int version, int content_type,
                       const void *buf, size_t len, SSL *ssl, void *arg);
  void *msg_callback_arg;

  int verify_mode;
  unsigned int sid_ctx_length;
  unsigned char sid_ctx[32];

  int quiet_shutdown;

  /* Maximum amount of data to send in one fragment.
   * actual record size can be more than this due to
   * padding and MAC overheads.
   */
  unsigned int max_send_fragment;

  /* For a server, this contains a callback function by which the set of
   * advertised protocols can be provided. */
  int (*next_protos_advertised_cb)(SSL *s, const unsigned char **buf,
                                   unsigned int *len, void *arg);
  void *next_protos_advertised_cb_arg;
  /* For a client, this contains a callback function that selects the
   * next protocol from the list provided by the server. */
  int (*next_proto_select_cb)(SSL *s, unsigned char **out,
                              unsigned char *outlen, const unsigned char *in,
                              unsigned int inlen, void *arg);
  void *next_proto_select_cb_arg;
};

struct ssl_cipher_st {
  int valid;
  const char *name; /* text name */
  unsigned long id; /* id, 4 bytes, first is version */

  /* changed in 0.9.9: these four used to be portions of a single value
   * 'algorithms' */
  unsigned long algorithm_mkey; /* key exchange algorithm */
  unsigned long algorithm_auth; /* server authentication */
  unsigned long algorithm_enc;  /* symmetric encryption */
  unsigned long algorithm_mac;  /* symmetric authentication */
  unsigned long algorithm_ssl;  /* (major) protocol version */

  unsigned long algo_strength; /* strength and export flags */
  unsigned long algorithm2;    /* Extra flags */
  int strength_bits;           /* Number of bits really used */
  int alg_bits;                /* Number of bits for algorithm */
};

struct ssl_method_st {
  int version;
  int (*ssl_new)(SSL *s);
  void (*ssl_clear)(SSL *s);
  void (*ssl_free)(SSL *s);
  int (*ssl_accept)(SSL *s);
  int (*ssl_connect)(SSL *s);
  int (*ssl_read)(SSL *s, void *buf, int len);
  int (*ssl_peek)(SSL *s, void *buf, int len);
  int (*ssl_write)(SSL *s, const void *buf, int len);
  int (*ssl_shutdown)(SSL *s);
  int (*ssl_renegotiate)(SSL *s);
  int (*ssl_renegotiate_check)(SSL *s);
  long (*ssl_get_message)(SSL *s, int st1, int stn, int mt, long max, int *ok);
  int (*ssl_read_bytes)(SSL *s, int type, unsigned char *buf, int len,
                        int peek);
  int (*ssl_write_bytes)(SSL *s, int type, const void *buf_, int len);
  int (*ssl_dispatch_alert)(SSL *s);
  long (*ssl_ctrl)(SSL *s, int cmd, long larg, void *parg);
  long (*ssl_ctx_ctrl)(SSL_CTX *ctx, int cmd, long larg, void *parg);
  const SSL_CIPHER *(*get_cipher_by_char)(const unsigned char *ptr);
  int (*put_cipher_by_char)(const SSL_CIPHER *cipher, unsigned char *ptr);
  int (*ssl_pending)(const SSL *s);
  int (*num_ciphers)(void);
  const SSL_CIPHER *(*get_cipher)(unsigned ncipher);
  const struct ssl_method_st *(*get_ssl_method)(int version);
  long (*get_timeout)(void);
  struct ssl3_enc_method *ssl3_enc; /* Extra SSLv3/TLS stuff */
  int (*ssl_version)(void);
  long (*ssl_callback_ctrl)(SSL *s, int cb_id, void (*fp)(void));
  long (*ssl_ctx_callback_ctrl)(SSL_CTX *s, int cb_id, void (*fp)(void));
};

#define SSL2_CHALLENGE_LENGTH 16
/*#define SSL2_CHALLENGE_LENGTH	32 */
#define SSL2_MIN_CHALLENGE_LENGTH 16
#define SSL2_MAX_CHALLENGE_LENGTH 32
#define SSL2_CONNECTION_ID_LENGTH 16
#define SSL2_MAX_CONNECTION_ID_LENGTH 16
#define SSL2_SSL_SESSION_ID_LENGTH 16
#define SSL2_MAX_CERT_CHALLENGE_LENGTH 32
#define SSL2_MIN_CERT_CHALLENGE_LENGTH 16
#define SSL2_MAX_KEY_MATERIAL_LENGTH 24

typedef struct ssl2_state_st {
  int three_byte_header;
  int clear_text;    /* clear text */
  int escape;        /* not used in SSLv2 */
  int ssl2_rollback; /* used if SSLv23 rolled back to SSLv2 */

  /* non-blocking io info, used to make sure the same
   * args were passwd */
  unsigned int wnum; /* number of bytes sent so far */
  int wpend_tot;
  const unsigned char *wpend_buf;

  int wpend_off; /* offset to data to write */
  int wpend_len; /* number of bytes passwd to write */
  int wpend_ret; /* number of bytes to return to caller */

  /* buffer raw data */
  int rbuf_left;
  int rbuf_offs;
  unsigned char *rbuf;
  unsigned char *wbuf;

  unsigned char *write_ptr; /* used to point to the start due to
                             * 2/3 byte header. */

  unsigned int padding;
  unsigned int rlength; /* passed to ssl2_enc */
  int ract_data_length; /* Set when things are encrypted. */
  unsigned int wlength; /* passed to ssl2_enc */
  int wact_data_length; /* Set when things are decrypted. */
  unsigned char *ract_data;
  unsigned char *wact_data;
  unsigned char *mac_data;

  unsigned char *read_key;
  unsigned char *write_key;

  /* Stuff specifically to do with this SSL session */
  unsigned int challenge_length;
  unsigned char challenge[SSL2_MAX_CHALLENGE_LENGTH];
  unsigned int conn_id_length;
  unsigned char conn_id[SSL2_MAX_CONNECTION_ID_LENGTH];
  unsigned int key_material_length;
  unsigned char key_material[SSL2_MAX_KEY_MATERIAL_LENGTH * 2];

  unsigned long read_sequence;
  unsigned long write_sequence;

  struct {
    unsigned int conn_id_length;
    unsigned int cert_type;
    unsigned int cert_length;
    unsigned int csl;
    unsigned int clear;
    unsigned int enc;
    unsigned char ccl[SSL2_MAX_CERT_CHALLENGE_LENGTH];
    unsigned int cipher_spec_length;
    unsigned int session_id_length;
    unsigned int clen;
    unsigned int rlen;
  } tmp;
} SSL2_STATE;

#define SSL3_RANDOM_SIZE 32
#define EVP_MAX_MD_SIZE 64 /* longest known is SHA512 */
#define EVP_MAX_KEY_LENGTH 64
#define EVP_MAX_IV_LENGTH 16
#define EVP_MAX_BLOCK_LENGTH 32

typedef struct ssl3_buffer_st {
  unsigned char *buf; /* at least SSL3_RT_MAX_PACKET_SIZE bytes,
                       * see ssl3_setup_buffers() */
  size_t len;         /* buffer size */
  int offset;         /* where to 'copy from' */
  int left;           /* how many bytes left */
} SSL3_BUFFER;

typedef struct ssl3_record_st {
  /*r */ int type;             /* type of record */
  /*rw*/ unsigned int length;  /* How many bytes available */
  /*r */ unsigned int off;     /* read/write offset into 'buf' */
  /*rw*/ unsigned char *data;  /* pointer to the record data */
  /*rw*/ unsigned char *input; /* where the decode bytes are */
  /*r */ unsigned char *comp;  /* only used with decompression - malloc()ed */
  /*r */ unsigned long epoch;  /* epoch number, needed by DTLS1 */
  /*r */ unsigned char seq_num[8]; /* sequence number, needed by DTLS1 */
} SSL3_RECORD;

typedef struct ssl3_state_st {
  long flags;
  int delay_buf_pop_ret;

  unsigned char read_sequence[8];
  int read_mac_secret_size;
  unsigned char read_mac_secret[EVP_MAX_MD_SIZE];
  unsigned char write_sequence[8];
  int write_mac_secret_size;
  unsigned char write_mac_secret[EVP_MAX_MD_SIZE];

  unsigned char server_random[SSL3_RANDOM_SIZE];
  unsigned char client_random[SSL3_RANDOM_SIZE];

  /* flags for countermeasure against known-IV weakness */
  int need_empty_fragments;
  int empty_fragment_done;

  /* The value of 'extra' when the buffers were initialized */
  int init_extra;

  SSL3_BUFFER rbuf; /* read IO goes into here */
  SSL3_BUFFER wbuf; /* write IO goes into here */

  SSL3_RECORD rrec; /* each decoded record goes in here */
  SSL3_RECORD wrec; /* goes out from here */

  /* storage for Alert/Handshake protocol data received but not
   * yet processed by ssl3_read_bytes: */
  unsigned char alert_fragment[2];
  unsigned int alert_fragment_len;
  unsigned char handshake_fragment[4];
  unsigned int handshake_fragment_len;

  /* partial write - check the numbers match */
  unsigned int wnum; /* number of bytes sent so far */
  int wpend_tot;     /* number bytes written */
  int wpend_type;
  int wpend_ret; /* number of bytes submitted */
  const unsigned char *wpend_buf;

  /* this is set whenerver we see a change_cipher_spec message
   * come in when we are not looking for one */
  int change_cipher_spec;

  int warn_alert;
  int fatal_alert;
  /* we allow one fatal and one warning alert to be outstanding,
   * send close alert via the warning alert */
  int alert_dispatch;
  unsigned char send_alert[2];

  /* This flag is set when we should renegotiate ASAP, basically when
   * there is no more data in the read or write buffers */
  int renegotiate;
  int total_renegotiations;
  int num_renegotiations;

  int in_read_app_data;

  /* Opaque PRF input as used for the current handshake.
   * These fields are used only if TLSEXT_TYPE_opaque_prf_input is defined
   * (otherwise, they are merely present to improve binary compatibility) */
  void *client_opaque_prf_input;
  size_t client_opaque_prf_input_len;
  void *server_opaque_prf_input;
  size_t server_opaque_prf_input_len;

  struct {
    /* actually only needs to be 16+20 */
    unsigned char cert_verify_md[EVP_MAX_MD_SIZE * 2];

    /* actually only need to be 16+20 for SSLv3 and 12 for TLS */
    unsigned char finish_md[EVP_MAX_MD_SIZE * 2];
    int finish_md_len;
    unsigned char peer_finish_md[EVP_MAX_MD_SIZE * 2];
    int peer_finish_md_len;

    unsigned long message_size;
    int message_type;

    /* used to hold the new cipher we are going to use */
    const SSL_CIPHER *new_cipher;

    /* used when SSL_ST_FLUSH_DATA is entered */
    int next_state;

    int reuse_message;

    /* used for certificate requests */
    int cert_req;
    int ctype_num;
    char ctype[9];
    int use_rsa_tmp;

    int key_block_length;
    unsigned char *key_block;

    int new_mac_pkey_type;
    int new_mac_secret_size;
    char *new_compression;
    int cert_request;
  } tmp;

  /* Connection binding to prevent renegotiation attacks */
  unsigned char previous_client_finished[EVP_MAX_MD_SIZE];
  unsigned char previous_client_finished_len;
  unsigned char previous_server_finished[EVP_MAX_MD_SIZE];
  unsigned char previous_server_finished_len;
  int send_connection_binding; /* TODOEKR */

} SSL3_STATE;

struct ssl_st {
  /* protocol version
   * (one of SSL2_VERSION, SSL3_VERSION, TLS1_VERSION, DTLS1_VERSION)
   */
  int version;
  int type; /* SSL_ST_CONNECT or SSL_ST_ACCEPT */

  const SSL_METHOD *method; /* SSLv3 */

  /* There are 2 BIO's even though they are normally both the
   * same.  This is so data can be read and written to different
   * handlers */

  char *rbio; /* used by SSL_read */
  char *wbio; /* used by SSL_write */
  char *bbio;
  /* This holds a variable that indicates what we were doing
   * when a 0 or -1 is returned.  This is needed for
   * non-blocking IO so we know what request needs re-doing when
   * in SSL_accept or SSL_connect */
  int rwstate;

  /* true when we are actually in SSL_accept() or SSL_connect() */
  int in_handshake;
  int (*handshake_func)(SSL *);

  /* Imagine that here's a boolean member "init" that is
   * switched as soon as SSL_set_{accept/connect}_state
   * is called for the first time, so that "state" and
   * "handshake_func" are properly initialized.  But as
   * handshake_func is == 0 until then, we use this
   * test instead of an "init" member.
   */

  int server; /* are we the server side? - mostly used by SSL_clear*/

  int new_session;    /* Generate a new session or reuse an old one.
                       * NB: For servers, the 'new' session may actually be a
                       * previously    cached session or even the previous session
                       * unless    SSL_OP_NO_SESSION_RESUMPTION_ON_RENEGOTIATION is
                       * set */
  int quiet_shutdown; /* don't send shutdown packets */
  int shutdown;       /* we have shut things down, 0x01 sent, 0x02
                       * for received */
  int state;          /* where we are */
  int rstate;         /* where we are when reading */

  BUF_MEM *init_buf; /* buffer used during init */
  void *init_msg;    /* pointer to handshake message body, set by
                        ssl3_get_message() */
  int init_num;      /* amount read/written */
  int init_off;      /* amount read/written */

  /* used internally to point at a raw packet */
  unsigned char *packet;
  unsigned int packet_length;

  struct ssl2_state_st *s2; /* SSLv2 variables */
  struct ssl3_state_st *s3; /* SSLv3 variables */
  // struct dtls1_state_st *d1; /* DTLSv1 variables */

  int read_ahead; /* Read as many input bytes as possible
                   * (for non-blocking reads) */

  /* callback that allows applications to peek at protocol messages */
  void (*msg_callback)(int write_p, int version, int content_type,
                       const void *buf, size_t len, SSL *ssl, void *arg);
  void *msg_callback_arg;

  int hit; /* reusing a previous session */

  int purpose; /* Purpose setting */
  int trust;   /* Trust setting */

  /* These are the ones being used, the ones in SSL_SESSION are
   * the ones to be 'copied' into these ones */
  int mac_flags;
  char *expand;

  char *compress;

  /* session info */

  /* client cert? */
  /* This is used to hold the server certificate used */
  struct cert_st /* CERT */ *cert;

  /* the session_id_context is used to ensure sessions are only reused
   * in the appropriate context */
  unsigned int sid_ctx_length;
  unsigned char sid_ctx[32];

  /* This can also be in the session once a session is established */
  SSL_SESSION *session;

  /* Used in SSL2 and SSL3 */
  int verify_mode; /* 0 don't care about verify failure.
                    * 1 fail if verify fails */

  void (*info_callback)(const SSL *ssl, int type,
                        int val); /* optional informational callback */

  int error;      /* error bytes to be written */
  int error_code; /* actual code */

  unsigned int (*psk_client_callback)(SSL *ssl, const char *hint,
                                      char *identity,
                                      unsigned int max_identity_len,
                                      unsigned char *psk,
                                      unsigned int max_psk_len);
  unsigned int (*psk_server_callback)(SSL *ssl, const char *identity,
                                      unsigned char *psk,
                                      unsigned int max_psk_len);

  SSL_CTX *ctx;
  /* set this flag to 1 and a sleep(1) is put into all SSL_read()
   * and SSL_write() calls, good for nbio debuging :-) */
  int debug;

  /* extra application data */
  long verify_result;

  int references;
  unsigned long options; /* protocol behaviour */
  unsigned long mode;    /* API behaviour */
  long max_cert_list;
  int first_packet;
  int client_version; /* what was passed, used for
                       * SSLv3/TLS rollback check */
  unsigned int max_send_fragment;
  /* TLS extension debug callback */
  void (*tlsext_debug_cb)(SSL *s, int client_server, int type,
                          unsigned char *data, int len, void *arg);
  void *tlsext_debug_arg;
  char *tlsext_hostname;
  int servername_done; /* no further mod of servername
                          0 : call the servername extension callback.
                          1 : prepare 2, allow last ack just after in server
                          callback. 2 : don't call servername callback, no ack
                          in server hello
                       */
  /* certificate status request info */
  /* Status type or -1 if no status type */
  int tlsext_status_type;
  /* Expect OCSP CertificateStatus message */
  int tlsext_status_expected;
  /* OCSP status request only */
  /* OCSP response received or to be sent */
  unsigned char *tlsext_ocsp_resp;
  int tlsext_ocsp_resplen;

  /* RFC4507 session ticket expected to be received or sent */
  int tlsext_ticket_expected;
  /* draft-rescorla-tls-opaque-prf-input-00.txt information to be used for
   * handshakes */
  void *tlsext_opaque_prf_input;
  size_t tlsext_opaque_prf_input_len;

  void *tls_session_secret_cb_arg;

  SSL_CTX *initial_ctx; /* initial ctx, used to store sessions */

  /* Next protocol negotiation. For the client, this is the protocol that
   * we sent in NextProtocol and is set when handling ServerHello
   * extensions.
   *
   * For a server, this is the client's selected_protocol from
   * NextProtocol and is set when handling the NextProtocol message,
   * before the Finished message. */
  unsigned char *next_proto_negotiated;
  unsigned char next_proto_negotiated_len;

  unsigned int
      tlsext_heartbeat; /* Is use of the Heartbeat extension negotiated?
                           0: disabled
                           1: enabled
                           2: enabled, but not allowed to send Requests
                         */
  unsigned int
      tlsext_hb_pending;      /* Indicates if a HeartbeatRequest is in flight */
  unsigned int tlsext_hb_seq; /* HeartbeatRequest sequence number */

  int renegotiate; /* 1 if we are renegotiating.
                    * 2 if we are a server and are inside a handshake
                    * (i.e. not just sending a HelloRequest) */
};

#define TLS1_RT_HEARTBEAT 24
#define TLS1_HB_REQUEST 1
#define TLS1_HB_RESPONSE 2
#define n2s(c, s)                                                              \
  ((s = (((unsigned int)(c[0])) << 8) | (((unsigned int)(c[1])))), c += 2)
#define s2n(s, c)                                                              \
  ((c[0] = (unsigned char)(((s) >> 8) & 0xff),                                 \
    c[1] = (unsigned char)(((s)) & 0xff)),                                     \
   c += 2)

int tls1_process_heartbeat(SSL *s);