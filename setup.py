import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='aiothornode',
    version='0.0.22',
    description='THORChain node connection library for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/tirinox/aiothornode',
    author='Maksim Koltsov',
    author_email='delevoper@tirinox.ru',
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'aiohttp>=3.7.3',
        'async-timeout>=3.0.1',
        'attrs>=20.3.0',
        'chardet>=3.0.4',
        'idna>=3.1',
        'multidict>=5.1.0',
        'typing-extensions>=3.7.4.3',
        'python-dateutil>=2.8.2',
        'ujson>=4.0.2',
        'yarl>=1.6.3',
    ]
)
