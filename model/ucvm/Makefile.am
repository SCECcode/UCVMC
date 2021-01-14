# GNU Automake config

EXTRA_DIST = ucvm* model*

all:

install:
	mkdir -p ${prefix}/model/ucvm
	if ! test . -ef ${prefix}/model/ucvm; then \
                cp -L ucvm* ${prefix}/model/ucvm; \
        fi

clean:
