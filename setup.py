import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


setuptools.setup(
    name='aiothornode',
    version='0.0.2',
    description='THORChain node connection library for Python',
    long_description=long_description,
    url='git@github.com:tirinox/aiothornode.git',
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
