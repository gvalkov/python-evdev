#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import textwrap

from os.path import abspath, dirname, join as pjoin
from distutils.command import build

#-----------------------------------------------------------------------------
try:
    from setuptools import setup, Extension
    from setuptools.command import bdist_egg, develop
except ImportError:
    from distutils.core import setup, Extension
    from distutils.command import build
    develop, bdist_egg = None, None

#-----------------------------------------------------------------------------
here = abspath(dirname(__file__))

#-----------------------------------------------------------------------------
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Operating System :: POSIX :: Linux',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: Implementation :: CPython',
]

#-----------------------------------------------------------------------------
cflags   = ['-std=c99', '-Wno-error=declaration-after-statement']
input_c  = Extension('evdev._input',  sources=['evdev/input.c'],  extra_compile_args=cflags)
uinput_c = Extension('evdev._uinput', sources=['evdev/uinput.c'], extra_compile_args=cflags)
ecodes_c = Extension('evdev._ecodes', sources=['evdev/ecodes.c'], extra_compile_args=cflags)

#-----------------------------------------------------------------------------
kw = {
    'name':                 'evdev',
    'version':              '0.5.0',

    'description':          'Bindings to the Linux input handling subsystem',
    'long_description':     open(pjoin(here, 'README.rst')).read(),

    'author':               'Georgi Valkov',
    'author_email':         'georgi.t.valkov@gmail.com',
    'license':              'Revised BSD License',
    'keywords':             'evdev input uinput',
    'url':                  'https://github.com/gvalkov/python-evdev',
    'classifiers':          classifiers,

    'packages':             ['evdev'],
    'ext_modules':          [input_c, uinput_c, ecodes_c],
    'include_package_data': False,
    'zip_safe':             True,
    'cmdclass':             {},
}


#-----------------------------------------------------------------------------
def create_ecodes():
    header = '/usr/include/linux/input.h'

    if not os.path.isfile(header):
        msg = '''\
        The linux/input.h header file is missing. You will have to
        install the headers for your kernel in order to continue:

            yum install kernel-headers-$(uname -r)
            apt-get install linux-headers-$(uname -r)
            pacman -S kernel-headers\n\n'''

        sys.stderr.write(textwrap.dedent(msg))
        sys.exit(1)

    from subprocess import check_call

    print('writing ecodes.c (using %s)' % header)
    cmd = '%s genecodes.py %s > ecodes.c' % (sys.executable, header)
    check_call(cmd, cwd="%s/evdev" % here, shell=True)


def cmdfactory(cmd):
    class cls(cmd):
        def run(self):
            create_ecodes()
            cmd.run(self)
    return cls

#-----------------------------------------------------------------------------
kw['cmdclass']['build'] = cmdfactory(build.build)

if develop and bdist_egg:
    kw['cmdclass']['develop']   = cmdfactory(develop.develop)
    kw['cmdclass']['bdist_egg'] = cmdfactory(bdist_egg.bdist_egg)

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    setup(**kw)
