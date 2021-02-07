import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


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
    install_requires=parse_requirements("requirements.txt")
)
