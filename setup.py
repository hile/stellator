
import glob
from setuptools import setup, find_packages
from stellator import __version__

setup(
    name='stellator',
    keywords='vmware fusion control scripts',
    description='Scripts to manage vmware fusion headless virtual machines',
    author='Ilkka Tuohela',
    author_email='hile@iki.fi',
    url='https://github.com/hile/stellator/',
    version=__version__,
    license='PSF',
    packages=find_packages(),
    install_requires=(
        'systematic>=4.4.2',
    ),
    python_requires='>3.6.0',
    entry_points={
        'console_scripts': [
            'stellator=stellator.bin.stellator:main',
        ],
    },
)
