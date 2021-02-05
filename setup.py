import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements


def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.req) for ir in reqs]


setuptools.setup(
    name='thorchain',
    version='0.0.1',
    description='THORChain library for Python',
    long_description=long_description,
    url='git@github.com:tirinox/thorchain.git',
    author='Maksim Koltsov',
    author_email='delevoper@tirinox.ru',
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=load_requirements("requirements.txt")
)
