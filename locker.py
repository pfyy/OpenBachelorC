import os
import sys
from hashlib import sha256, sha1


from Crypto.Cipher import AES

TARGET_TS_FILEPATH_LST = [
    "src/script/java/index.ts",
    "src/script/native/index.ts",
    "src/script/util/index.ts",
]

KEY_FILEPATH = "key.png"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("error: no command given")
        exit(1)

    if not os.path.isfile(KEY_FILEPATH):
        print("error: key not found")
        exit(1)

    with open(KEY_FILEPATH, "rb") as f:
        key_binary = f.read()
    key_hash = sha256(key_binary)

    key = key_hash.digest()
    nonce = sha1(key_binary).digest()[:16]

    if sys.argv[1] == "encrypt":
        for target_ts_filepath in TARGET_TS_FILEPATH_LST:
            target_ts_encrypted_filepath = target_ts_filepath + ".encrypted"
            with open(target_ts_filepath, "rb") as f:
                ts_binary = f.read()
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            ts_binary_encrypted = cipher.encrypt(ts_binary)
            with open(target_ts_encrypted_filepath, "wb") as f:
                f.write(ts_binary_encrypted)
    elif sys.argv[1] == "decrypt":
        for target_ts_filepath in TARGET_TS_FILEPATH_LST:
            target_ts_encrypted_filepath = target_ts_filepath + ".encrypted"
            with open(target_ts_encrypted_filepath, "rb") as f:
                ts_binary_encrypted = f.read()
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            ts_binary = cipher.decrypt(ts_binary_encrypted)
            with open(target_ts_filepath, "wb") as f:
                f.write(ts_binary)
    else:
        print("error: unknown command")
        exit(1)
