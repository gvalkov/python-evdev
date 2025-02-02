import os
import sys
import shutil
import textwrap
import platform
from pathlib import Path
from subprocess import run

from setuptools import setup, Extension, Command
from setuptools.command import build_ext as _build_ext


curdir = Path(__file__).resolve().parent
ecodes_c_path = curdir / "src/evdev/ecodes.c"


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
        if platform.system().lower() == "freebsd":
            files = ["dev/evdev/input.h", "dev/evdev/input-event-codes.h", "dev/evdev/uinput.h"]
        else:
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

        If you want to avoid building this package from source, then please consider
        installing the `evdev-binary` package instead. Keep in mind that it may not be
        fully compatible with, or support all the features of your current kernel.
        """

        sys.stderr.write(textwrap.dedent(msg))
        sys.exit(1)

    print("writing %s (using %s)" % (ecodes_c_path, " ".join(headers)))
    with ecodes_c_path.open("w") as fh:
        cmd = [sys.executable, "src/evdev/genecodes_c.py", "--ecodes", *headers]
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
            return False
        return True

    def generate_ecodes_py(self):
        ecodes_py = Path(self.build_lib) / "evdev/ecodes.py"
        print(f"writing {ecodes_py}")
        with ecodes_py.open("w") as fh:
            cmd = [sys.executable, "-B", "src/evdev/genecodes_py.py"]
            res = run(cmd, env={"PYTHONPATH": self.build_lib}, stdout=fh)

        if res.returncode != 0:
            print(f"failed to generate static {ecodes_py} - will use ecodes_runtime.py")
            shutil.copy("src/evdev/ecodes_runtime.py", ecodes_py)

    def run(self):
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)
        _build_ext.build_ext.run(self)
        self.generate_ecodes_py()

    sub_commands = [("build_ecodes", has_ecodes)] + _build_ext.build_ext.sub_commands


cflags = ["-std=c99", "-Wno-error=declaration-after-statement"]
setup(
    ext_modules=[
        Extension("evdev._input", sources=["src/evdev/input.c"], extra_compile_args=cflags),
        Extension("evdev._uinput", sources=["src/evdev/uinput.c"], extra_compile_args=cflags),
        Extension("evdev._ecodes", sources=["src/evdev/ecodes.c"], extra_compile_args=cflags),
    ],
    cmdclass={
        "build_ext": build_ext,
        "build_ecodes": build_ecodes,
    },
)
