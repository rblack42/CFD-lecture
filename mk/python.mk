.PHONY: pyinit
pyinit:  ## configure python project
	@test ./.python-version || \
		cp ~/_sys/PYPROJ/python-version .python-version

	@test ./.envrc || \
		cp ~/_sys/PYPROJ/envrc .envrc

.PHONY: pyprep
pyprep: ## install pip tools
	pip install -U pip
	pip install wheel
	pip install pip-tools

.PHONY: pyreqs
pyreqs:  ## update project requirements
	pip-compile --resolver=backtracking
	pip install -r requirements.txt

.PHONY: test
test: ## Run unit tests
	python -m pytest

.PHONY: changes
changes:	## create CHANGES file from git logs
	git log --oneline --pretty=format:"* %ad: %s" --date=short > CHANGES

.PHONY: pydev
pydev:		## Install package in development mode
	python -m pip install --editable .

.PHONY:	run
run:	## simple run of application (no parameters)
	python -m ${APPNAME}
