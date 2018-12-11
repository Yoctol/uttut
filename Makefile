.DEFAULT_GOAL := all

.PHONY: installself
installself:
	python setup.py build_ext
	pip install -e .

.PHONY: install
install:
	pip install -U pip wheel setuptools cython==0.29.1
	pip install -r requirements_dev.txt
	make installself

.PHONY: lint
lint:
	flake8

.PHONY: test
test:
	py.test --cov=uttut/ --cov-fail-under=90

.PHONY: all
all: lint test

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
