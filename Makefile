1.DEFAULT_GOAL := all

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

.PHONY: typecheck
typecheck:
	mypy --config-file=.mypy uttut

.PHONY: test
test:
	pytest --cov-report=term-missing --cov=uttut/ --cov-fail-under=80

.PHONY: test-linetrace
test-linetrace:
	make clean
	make clean-c
	LINE_TRACE=1 python setup.py build_ext --force --inplace --define CYTHON_TRACE
	make test

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

.PHONY: clean-c
clean-c:
	rm -f `find uttut -name *.c`
	rm -f `find uttut -name *.cpp`

.PHONY: docs
docs:
	make install
	make -C docs

.PHONY: distribute
distribute:
	make clean
	python setup.py sdist

