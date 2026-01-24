from .config import config
from .adb import (
    get_running_emulators,
    connect_to_emulator,
    upload_standalone_script,
)


def main():
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

    host = config["host"]
    port = config["port"]
    proxy_url = f"http://{host}:{port}"

    upload_standalone_script(
        emulator_id,
        "rel/java.js",
        {"proxy_url": proxy_url},
    )
    upload_standalone_script(
        emulator_id,
        "rel/native.js",
        {"proxy_url": proxy_url},
    )
    upload_standalone_script(emulator_id, "rel/extra.js", config["extra_config"])


if __name__ == "__main__":
    main()
