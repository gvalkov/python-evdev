import os
import sys
import textwrap
from pathlib import Path

from setuptools import setup, Extension, Command
from setuptools.command import build_ext as _build_ext
from setuptools.command import install as _install

curdir = Path(__file__).resolve().parent
ecodes_c_path = curdir / "evdev/ecodes.c"
ecodes_pyi_path = curdir / "evdev/ecodes.pyi"


def create_ecodes(headers=None):
    if not headers:
        include_paths = set()
        cpath = os.environ.get("CPATH", "").strip()
        c_inc_path = os.environ.get("C_INCLUDE_PATH", "").strip()

        if cpath:
            include_paths.update(cpath.split(":"))
        if c_inc_path:
            include_paths.update(c_inc_path.split(":"))

        include_paths.add("/usr/include")
        files = ["linux/input.h", "linux/input-event-codes.h", "linux/uinput.h"]
        headers = [os.path.join(path, file) for path in include_paths for file in files]

    headers = [header for header in headers if os.path.isfile(header)]
    if not headers:
        msg = """\
        The 'linux/input.h' and 'linux/input-event-codes.h' include files
        are missing. You will have to install the kernel header files in
        order to continue:

            dnf install kernel-headers-$(uname -r)
            apt-get install linux-headers-$(uname -r)
            emerge sys-kernel/linux-headers
            pacman -S kernel-headers

        In case they are installed in a non-standard location, you may use
        the '--evdev-headers' option to specify one or more colon-separated
        paths. For example:

            python setup.py \\
              build \\
              build_ecodes --evdev-headers path/input.h:path/input-event-codes.h \\
              build_ext --include-dirs path/ \\
              install
        """

        sys.stderr.write(textwrap.dedent(msg))
        sys.exit(1)

    from subprocess import run

    print("writing %s (using %s)" % (ecodes_c_path, " ".join(headers)))
    with ecodes_c_path.open("w") as fh:
        cmd = [sys.executable, "evdev/genecodes.py", *headers]
        run(cmd, check=True, stdout=fh)

    print("writing %s (using %s)" % (ecodes_pyi_path, " ".join(headers)))
    with ecodes_pyi_path.open("w") as fh:
        cmd = [sys.executable, "evdev/genpyi.py", *headers]
        run(cmd, check=True, stdout=fh)


class build_ecodes(Command):
    description = "generate ecodes.c"

    user_options = [
        ("evdev-headers=", None, "colon-separated paths to input subsystem headers"),
    ]

    def initialize_options(self):
        self.evdev_headers = None

    def finalize_options(self):
        if self.evdev_headers:
            self.evdev_headers = self.evdev_headers.split(":")

    def run(self):
        create_ecodes(self.evdev_headers)


class build_ext(_build_ext.build_ext):
    def has_ecodes(self):
        if ecodes_c_path.exists():
            print("ecodes.c already exists ... skipping build_ecodes")
        return not ecodes_c_path.exists()

    def run(self):
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)
        _build_ext.build_ext.run(self)

    sub_commands = [("build_ecodes", has_ecodes)] + _build_ext.build_ext.sub_commands # type: ignore
    use_stubs = True

# I've been reading through setuptools docs, but i can't for the lofe of me figure out how to bring the pyi stubs into the package "cleanly"
class install(_install.install):
    def run(self):
        print(os.listdir(os.getenv("src")))
        #_install.install.copy_file(self, "evdev/ecodes.pyi", "evdev/ecodes.pyi")
        installdir = "build/lib.linux-x86_64-cpython-311/evdev"
        Path(f"{installdir}/ecodes.pyi").write_bytes(Path("evdev/ecodes.pyi").read_bytes())
        print("CUSTOM INSTALLER")
        print(self.build_lib)
        _install.install.run(self)


cflags = ["-std=c99", "-Wno-error=declaration-after-statement"]
setup(
    #include_package_data=True,
    packages=["evdev"],
    package_dir={'evdev': 'evdev'},
    package_data={'evdev': ["*.pyi"]},
    ext_modules=[
        Extension("evdev._input", sources=["evdev/input.c"], extra_compile_args=cflags),
        Extension("evdev._uinput", sources=["evdev/uinput.c"], extra_compile_args=cflags),
        Extension("evdev._ecodes", sources=["evdev/ecodes.c"], extra_compile_args=cflags),
    ],
    cmdclass={
        "build_ext": build_ext,
        "build_ecodes": build_ecodes,
        "install": install,
    },
)
