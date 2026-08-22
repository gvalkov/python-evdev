#!/usr/bin/env bash

set -o allexport
set -o nounset

CIBW_LINUX_X86_64_IMAGE="manylinux_2_34"
CIBW_LINUX_I686_IMAGE="manylinux_2_34"
CIBW_CONTAINER_ENGINE="podman"
CIBW_ARCHS_LINUX="auto64"
CIBW_BEFORE_ALL_LINUX=./scripts/cibw-before.sh
CIBW_TEST_COMMAND="python -c 'import evdev; print(evdev)'"
CIBW_ENVIRONMENT="PACKAGE_NAME=evdev-binary"

exec cibuildwheel 