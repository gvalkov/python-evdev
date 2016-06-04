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
    from setuptools.command import bdist_egg, develop, build_ext
except ImportError:
    from distutils.core import setup, Extension
    from distutils.command import build, build_ext

#-----------------------------------------------------------------------------
here = abspath(dirname(__file__))

#-----------------------------------------------------------------------------
classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
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
    'version':              '0.6.1',

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
def create_ecodes(headers=None):
    if not headers:
        headers = [
            '/usr/include/linux/input.h',
            '/usr/include/linux/input-event-codes.h',
        ]

    headers = [header for header in headers if os.path.isfile(header)]
    if not headers:
        msg = '''\
        The 'linux/input.h' and 'linux/input-event-codes.h' include files
        are missing. You will have to install the kernel header files in
        order to continue:

            yum install kernel-headers-$(uname -r)
            apt-get install linux-headers-$(uname -r)
            emerge sys-kernel/linux-headers
            pacman -S kernel-headers

        In case they are installed in a non-standard location, you may use
        the '--evdev-headers' option to specify one or more colon-separated
        paths. For example:

            python setup.py build_ext \\
              --evdev-headers path/input.h:path/input-event-codes.h \\
              --include-dirs  path/ \\
              install
        '''

        sys.stderr.write(textwrap.dedent(msg))
        sys.exit(1)

    from subprocess import check_call

    print('writing ecodes.c (using %s)' % ' '.join(headers))
    cmd = '%s genecodes.py %s > ecodes.c' % (sys.executable, ' '.join(headers))
    check_call(cmd, cwd="%s/evdev" % here, shell=True)


#-----------------------------------------------------------------------------
class cmdbuild_ext(build_ext.build_ext):
    user_options = build_ext.build_ext.user_options[:]
    user_options.extend([
        ('evdev-headers=', None, 'colon-separated paths to input subsystem headers'),
    ])

    def initialize_options(self):
        self.evdev_headers = None
        # We cannot use super(cmdbuild_ext, self) here for compatibility with Py2.
        build_ext.build_ext.initialize_options(self)

    def finalize_options(self):
        if self.evdev_headers:
            self.evdev_headers = self.evdev_headers.split(':')
        build_ext.build_ext.finalize_options(self)

    def run(self):
        create_ecodes(self.evdev_headers)
        build_ext.build_ext.run(self)

#-----------------------------------------------------------------------------
kw['cmdclass']['build_ext'] = cmdbuild_ext


#-----------------------------------------------------------------------------
if __name__ == '__main__':
    setup(**kw)
