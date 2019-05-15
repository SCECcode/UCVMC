install:
	mkdir -p ${prefix}/utilities
	mkdir -p ${prefix}/utilities/pycvm/
	mkdir -p ${prefix}/utilities/pycvm/pycvm
	if ! test . -ef ${prefix}/utilities; then \
		cp -R *.py ${prefix}/utilities; \
		cp -R *.sh ${prefix}/utilities; \
		chmod +x ${prefix}/utilities/*.py; \
		chmod +x ${prefix}/utilities/*.sh; \
		cp -R pycvm/*.py ${prefix}/utilities/pycvm/; \
		chmod +x ${prefix}/utilities/*.py; \
		cp -R pycvm/pycvm/*.py ${prefix}/utilities/pycvm/pycvm/; \
		chmod +x ${prefix}/utilities/pycvm/pycvm/*.py; \
	fi

clean:
	echo ""
