import sys

from adb import (
    get_running_emulators,
    connect_to_emulator,
    upload_frida_server_if_necessary,
    start_frida_server,
    start_reverse_proxy,
)
from config import config
from inject import start_game


if __name__ == "__main__":
    if "--no_proxy" in sys.argv:
        config["no_proxy"] = True

    running_emulator_id_lst = get_running_emulators()

    if not running_emulator_id_lst:
        print("info: finding emulator")
        connect_to_emulator()
        running_emulator_id_lst = get_running_emulators()

        if not running_emulator_id_lst:
            print("error: emulator not found")
            exit(1)

    emulator_id = running_emulator_id_lst[0]
    print(f"info: using emulator {emulator_id}")

    upload_frida_server_if_necessary(emulator_id)

    start_frida_server(emulator_id)

    host = config["host"]
    port = config["port"]

    if host == "127.0.0.1":
        start_reverse_proxy(emulator_id, port)

    start_game(emulator_id)

    print("info: game started")

    print()
    print("----------")
    print()

    input("Press Enter to Exit:\n")
