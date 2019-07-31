
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
    entry_points={
        'console_scripts': [
            'stellator=stellator.bin.stellator:main',
        ],
    },
    install_requires=(
        'systematic>=4.4.2',
    ),
    python_requires='>3.6.0',
    setup_requires=['pytest-runner'],
    tests_require=(
        'pytest',
        'pytest-runner',
        'pytest-datafiles',
    ),
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: System',
        'Topic :: System :: Systems Administration',
    ],
)
