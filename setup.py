import os
import codecs
from setuptools import setup, find_packages


INFO = {}

with codecs.open('README.md', mode='r', encoding='utf-8') as f:
    INFO['long_description'] = f.read()

setup(
    name='asyncio-telnet',
    version=os.environ.get('RELEASE_VERSION'),
    description='Asyncio-based Telnet library',
    long_description=INFO['long_description'],
    long_description_content_type='text/markdown',
    author='Vladimir Penzin',
    author_email='pvenv@icloud.com',
    packages=find_packages(),
    url='https://github.com/ForceFledgling/asyncio-telnet',
    platforms='any',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Framework :: AsyncIO',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Terminals :: Telnet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=(
        'telnet tty asyncio synchronous asyncronous vty vtysh fast simple'
    ),
    install_requires=[
        'asyncio',
    ],
)
