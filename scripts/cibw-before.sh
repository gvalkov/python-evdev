#!/usr/bin/env bash


if [ -n "$PACKAGE_NAME" ]; then
    sed -i -re 's,^(name = ")evdev("),\1'${PACKAGE_NAME}'\2,' pyproject.toml
fi