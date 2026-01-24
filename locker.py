import os
import sys
from hashlib import sha256, sha1
import argparse
from pathlib import Path
import functools


from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

ENCRYPTED_EXT = ".encrypted"

TARGET_TS_FILEPATH_LST = [
    "src/script/java/index.ts",
    "src/script/native/index.ts",
    "src/script/util/index.ts",
    "src/script/extra/index.ts",
    "src/script/trainer/index.ts",
    "build_js_rel.cmd",
    "src/helper/helper.js",
    "src/helper/helper.py",
]

KEY_FILEPATH = "key_v1.png"

LOCKER_VERSION = 1

LOCKER_HEADER_SIZE = 1024

LEN_LOCKER_VERSION = 4

LEN_NONCE = 16


@functools.lru_cache
def get_key():
    key_filepath = Path(KEY_FILEPATH)

    if not key_filepath.is_file():
        print("err: key not found")
        exit(1)

    key_binary = key_filepath.read_bytes()

    return sha256(key_binary).digest()


def get_new_nonce():
    return get_random_bytes(LEN_NONCE)


def get_encrypted_filepath(filepath: Path):
    return filepath.with_suffix(filepath.suffix + ENCRYPTED_EXT)


def try_get_file_content(filepath: Path):
    encrypted_filepath = get_encrypted_filepath(filepath)

    if not encrypted_filepath.is_file():
        return None

    encrypted_content = encrypted_filepath.read_bytes()

    if len(encrypted_content) < LOCKER_HEADER_SIZE:
        return None

    locker_version = int.from_bytes(
        encrypted_content[:LEN_LOCKER_VERSION], byteorder="big"
    )

    if locker_version != LOCKER_VERSION:
        return None

    key = get_key()
    nonce = encrypted_content[LEN_LOCKER_VERSION : LEN_LOCKER_VERSION + LEN_NONCE]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    try:
        content = cipher.decrypt(encrypted_content[LOCKER_HEADER_SIZE:])
        return content
    except Exception:
        return None


def encrypt_file(filepath: Path):
    if not filepath.is_file():
        print(f"err: file {filepath} not found")
        return

    content = filepath.read_bytes()

    orig_content = try_get_file_content(filepath)
    if content == orig_content:
        return

    key = get_key()
    nonce = get_new_nonce()
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    payload = cipher.encrypt(content)
    header = (
        LOCKER_VERSION.to_bytes(LEN_LOCKER_VERSION, byteorder="big") + nonce
    ).ljust(LOCKER_HEADER_SIZE, b"\0")

    encrypted_filepath = get_encrypted_filepath(filepath)

    encrypted_filepath.write_bytes(header + payload)


def decrypt_file(filepath: Path):
    content = try_get_file_content(filepath)
    if content is None:
        print(f"err: failed to decrypt {filepath}")
        return

    filepath.write_bytes(content)


def do_encrypt():
    for filepath in TARGET_TS_FILEPATH_LST:
        encrypt_file(Path(filepath))


def do_decrypt():
    for filepath in TARGET_TS_FILEPATH_LST:
        decrypt_file(Path(filepath))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["encrypt", "decrypt"])
    args = parser.parse_args()

    if args.action == "encrypt":
        do_encrypt()
    elif args.action == "decrypt":
        do_decrypt()


if __name__ == "__main__":
    main()
