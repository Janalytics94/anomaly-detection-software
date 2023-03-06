FROM skoppe/afl

# get mjs
RUN git clone https://github.com/cesanta/mjs.git mjs-issues-57
WORKDIR /mjs-issues-57
RUN git checkout d6c06a6

# build and run mjs with AFL
WORKDIR /
COPY afl_build.sh afl_build.sh
COPY afl_run.sh afl_run.sh

RUN sh afl_build.sh

ENTRYPOINT ["sh", "afl_run.sh"]
