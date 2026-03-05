set -euo pipefail

pkg install -y xz-utils

FRIDA_VERSION=17.6.2

tar -xf "frida-${FRIDA_VERSION}.tar.gz"

mkdir -p devkit/
tar -xf "frida-core-devkit-${FRIDA_VERSION}-android-arm64.tar.xz" -C devkit/

clang -shared -fPIC \
    -o _frida.so \
    -I devkit/ \
    $(python3-config --includes) \
    "frida-${FRIDA_VERSION}/frida/_frida/extension.c" \
    devkit/libfrida-core.a \
    $(python3-config --ldflags) \
    -llog

export FRIDA_EXTENSION=$(realpath _frida.so)

poetry run pip install "frida-${FRIDA_VERSION}.tar.gz"
