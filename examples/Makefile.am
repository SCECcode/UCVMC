############################################
# Special build targets
############################################
SUBDIRS = api programs/basin programs/ucvm programs/etree programs/mesh

install:
	mkdir -p ${prefix}/examples
	@for i in $(SUBDIRS); do \
		${prefix}/tests/basin/$${i}; \
	done

