set -euo pipefail

pkg install xz-utils

tar -xf frida-17.6.2.tar.gz

mkdir -p devkit/
tar -xf frida-core-devkit-17.6.2-android-arm64.tar.xz -C devkit/

clang -shared -fPIC \
    -o _frida.so \
    -I devkit/ \
    $(python3-config --includes) \
    frida-17.6.2/frida/_frida/extension.c \
    devkit/libfrida-core.a \
    $(python3-config --ldflags) \
    -llog

export FRIDA_EXTENSION=$(realpath _frida.so)

poetry run pip install frida-17.6.2.tar.gz
