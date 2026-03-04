pkg upgrade

pkg install git
pkg install python python-pip
pkg install rust
pkg install binutils
pkg install android-tools
pkg install jq

export ANDROID_API_LEVEL=24

pip install pipx
pipx install poetry
pipx ensurepath

poetry config installer.max-workers 1

poetry install || true
poetry install --only-root
