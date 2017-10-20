# GNU Automake config

EXTRA_DIST = man*

all:

install:
	mkdir -p ${prefix}/man/man1
	if ! test . -ef ${prefix}/man/man1; then \
                cp man1/* ${prefix}/man/main1 \
        fi

clean:
