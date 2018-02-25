#!/usr/bin/env python2

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='bunsen-exit',
    version='3.0.0',
    description='A pygtk exit dialog that supports custom themes. Bunsen-exit also runs independent of systemd',
    long_description=readme(),
    url='https://github.com/BunsenLabs/bunsen-exit',
    license='GPL 3.0',
    author='Bunsenlabs',
    author_email='webradley9929@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Environment :: X11 Applications :: GTK',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
      ],
    packages=['bunsen-exit'],
    install_requires=[
        "dbus-python",
        "pygtk",
        "pyxdg"
    ],
    entry_points={
        'console_scripts': [
            'bunsen-exit=main:main',
        ],
    },
    include_package_data=True,
    zip_safe=False
)

