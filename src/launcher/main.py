from adb import (
    get_running_emulators,
    connect_to_emulator,
    upload_frida_server_if_necessary,
    start_frida_server,
)


if __name__ == "__main__":
    running_emulator_id_lst = get_running_emulators()

    if not running_emulator_id_lst:
        connect_to_emulator()

    if not running_emulator_id_lst:
        print("error: emulator not found")
        exit(1)

    emulator_id = running_emulator_id_lst[0]
    print(f"info: using emulator {emulator_id}")

    upload_frida_server_if_necessary(emulator_id)

    start_frida_server(emulator_id)
