from setuptools import setup, find_packages, Extension
from pathlib import Path


try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

# a good way to structure python package with Cython
# https://stackoverflow.com/questions/4505747/how-should-i-structure-a-python-package-that-contains-cython-code
try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

cmdclass = {}
ext_modules = []

if use_cython:
    ext_modules += [
        Extension('uttut.elements', ['uttut/elements.pyx']),
        Extension('uttut.expand_by_entities', ['uttut/expand_by_entities.pyx']),
        Extension('uttut.normalize_datum', ['uttut/normalize_datum.pyx']),
        Extension('uttut.tokenize_datum', ['uttut/tokenize_datum.pyx']),
    ]
    cmdclass.update({'build_ext': build_ext})
else:
    ext_modules += [
        Extension('uttut.elements', ['uttut/elements.c']),
        Extension('uttut.expand_by_entities', ['uttut/expand_by_entities.c']),
        Extension('uttut.normalize_datum', ['uttut/normalize_datum.c']),
        Extension('uttut.tokenize_datum', ['uttut/tokenize_datum.c']),
    ]


readme = Path(__file__).parent.joinpath('README.md')
if readme.exists():
    with readme.open() as f:
        long_description = f.read()
        try:
            from pypandoc import convert_text
            long_description = convert_text(
                long_description, 'rst', format='md')
        except ImportError:
            print("warning: pypandoc module not found, could not convert Markdown to RST")
else:
    long_description = '-'


setup(
    name="uttut",
    version='0.5.1',
    description="Yoctol Utterance processing utilities",
    license="MIT",
    author="cph",
    url='https://github.com/Yoctol/uttut',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.14.1',
    ],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Development Status :: 3 - Alpha",
    ],
    cmdclass=cmdclass,
    ext_modules=ext_modules,
    python_requires='>=3.5',
)
