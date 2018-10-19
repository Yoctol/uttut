.DEFAULT_GOAL := all

.PHONY: installself
installself:
	python setup.py build_ext
	pip install -e .

.PHONY: install
install:
	pip install -U pip wheel setuptools cython
	pip install -r requirements_dev.txt
	make installself

.PHONY: lint
lint:
	flake8

.PHONY: test
test:
	python -m unittest

.PHONY: all
all: test lint


.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find uttut -name *.so`
	rm -rf .cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	python setup.py clean

.PHONY: dev-test
dev-test:
	make clean
	make installself
	make lint
	make test

.PHONY: docs
docs:
	make installself
	make -C docs

.PHONY: distribute
distribute:
	make clean
	python setup.py sdist
