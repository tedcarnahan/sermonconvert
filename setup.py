from setuptools import setup, find_packages
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sermonconvert',

    version='0.0.1.dev1',

    description='Convert and upload segments of video files',
    long_description=long_description,

    url='http://tedcarnahan.com',

    author='Ted Carnahan',
    author_email='ted@tedcarnahan.com',

    license='MIT',

    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: MacOS X :: Cocoa',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Religion',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Video :: Conversion',
        'Topic :: Religion',
        'Topic :: Utilities',
        ],

    keywords='podcast sermon video conversion youtube',

    packages=find_packages(),

    install_requires=['PyQt5'],

    extras_require={
        'dev': [],
        'test': [],
        },


    )
