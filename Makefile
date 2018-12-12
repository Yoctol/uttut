.DEFAULT_GOAL := all

.PHONY: installself
installself:
	python setup.py build_ext
	pip install -e .

.PHONY: install
install:
	pipenv install

.PHONY: install-dev
install-dev:
	pipenv install --dev

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
	make install
	make -C docs

.PHONY: distribute
distribute:
	make clean
	python setup.py sdist

.PHONY: rebuild
rebuild:
	make clean
	rm -f `find uttut -name *.c`
	rm -f `find uttut -name *.cpp`
