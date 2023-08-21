# Makefile help system

.PHONY: help
help:	## display help messages
	@python mk/pyhelp.py$(MAKEFILE_LIST)
