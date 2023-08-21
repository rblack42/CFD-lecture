.PHONY: nb
nb:
	cd book && \
		jupyter-lab

.PHONY: book
book:
	jb build book --all
	cp -r book/_build/html/* docs
