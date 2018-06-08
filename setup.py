#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    bl-exit: Bunsenlabs exit dialog, offering various exit options
#     via both GUI and CLI
#    Copyright (C) 2012 Philip Newborough  <corenominal@corenominal.org>
#    Copyright (C) 2016 xaos52  <xaos52@gmail.com>
#    Copyright (C) 2017 damo  <damo@bunsenlabs.org>
#    Copyright (C) 2018 tknomanzr <webradley9929@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup, find_packages
import sys

if sys.version_info < (2, 7):
      raise Exception("This program only supports Python 2.7 or later")

setup(
    name='bunsen-exit',
    version='3.0.0rc1',
    install_requires=[
        "dbus-python",
        "pyxdg"
    ],
    description='A pygtk exit dialog that supports custom themes. Bunsen-exit also runs independent of systemd',
    license='GPL3',
    author='William Bradley',
    author_email='webradley9929@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'bl-exit = bunsen_exit.__main__:main',
        ]
    },
    url="https://github.com/BunsenLabs/bunsen-exit",
)

