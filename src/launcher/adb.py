import subprocess
import os
import lzma

from config import config

ADB_FILEPATH = "platform-tools/adb.exe"

MAX_NUM_MUMU_EMU = 4
MAX_NUM_LD_EMU = 4

ARCH_TO_FRIDA_SERVER_XZ_FILEPATH = {
    "x86_64": "frida-server/frida-server-16.5.9-android-x86_64.xz",
    "arm64-v8a": "frida-server/frida-server-16.5.9-android-arm64.xz",
    "x86": "frida-server/frida-server-16.5.9-android-x86.xz",
    "armeabi-v7a": "frida-server/frida-server-16.5.9-android-arm.xz",
    "armeabi": "frida-server/frida-server-16.5.9-android-arm.xz",
}

ANDROID_FRIDA_SERVER_FILEPATH = "/data/local/tmp/frida-server-16.5.9"

TMP_DIRPATH = "tmp/"


def get_running_emulators():
    proc = subprocess.run([ADB_FILEPATH, "devices"], capture_output=True, text=True)

    running_emulator_id_lst = []

    for line in proc.stdout.splitlines()[1:]:
        line = line.strip()
        if line:
            line_split = line.split()
            if line_split[-1] != "offline":
                running_emulator_id_lst.append(line_split[0])

    return running_emulator_id_lst


def connect_to_emulator():
    emulator_id_lst = []

    # MUMU
    for i in range(MAX_NUM_MUMU_EMU):
        emulator_id_lst.append(f"127.0.0.1:{16384+32*i}")

    # LD
    for i in range(MAX_NUM_LD_EMU):
        emulator_id_lst.append(f"127.0.0.1:{5555+2*i}")

    # try connecting
    proc_lst = []
    for emulator_id in emulator_id_lst:
        proc = subprocess.Popen([ADB_FILEPATH, "connect", emulator_id])
        proc_lst.append(proc)

    for proc in proc_lst:
        proc.wait()


def get_emulator_arch(emulator_id):
    proc = subprocess.run(
        [ADB_FILEPATH, "-s", emulator_id, "shell", "getprop ro.product.cpu.abi"],
        capture_output=True,
        text=True,
    )

    return proc.stdout.strip()


def upload_frida_server_if_necessary(emulator_id):
    proc = subprocess.run(
        [
            ADB_FILEPATH,
            "-s",
            emulator_id,
            "shell",
            f"test -f '{ANDROID_FRIDA_SERVER_FILEPATH}' || echo 1",
        ],
        capture_output=True,
        text=True,
    )

    if not proc.stdout.strip():
        print("info: frida server found")
        return

    print("info: frida server not found")

    os.makedirs(TMP_DIRPATH, exist_ok=True)

    emulator_arch = get_emulator_arch(emulator_id)
    print(f"info: emulator arch {emulator_arch}")
    frida_server_xz_filepath = ARCH_TO_FRIDA_SERVER_XZ_FILEPATH[emulator_arch]

    frida_server_filepath = os.path.join(TMP_DIRPATH, "frida-server")

    with lzma.open(frida_server_xz_filepath) as f:
        frida_server_binary = f.read()
    with open(frida_server_filepath, "wb") as f:
        f.write(frida_server_binary)

    proc = subprocess.run(
        [
            ADB_FILEPATH,
            "-s",
            emulator_id,
            "push",
            frida_server_filepath,
            ANDROID_FRIDA_SERVER_FILEPATH,
        ],
    )

    proc = subprocess.run(
        [
            ADB_FILEPATH,
            "-s",
            emulator_id,
            "shell",
            f"chmod a+x '{ANDROID_FRIDA_SERVER_FILEPATH}'",
        ],
    )

    print("info: frida server uploaded")


def root_emulator(emulator_id):
    print("info: root emulator")
    proc = subprocess.run(
        [
            ADB_FILEPATH,
            "-s",
            emulator_id,
            "root",
        ],
    )

    proc = subprocess.run(
        [
            ADB_FILEPATH,
            "-s",
            emulator_id,
            "wait-for-device",
        ],
    )
    print("info: emulator rooted")


def start_frida_server(emulator_id):
    root_emulator(emulator_id)

    start_frida_server_cmd = f"'{ANDROID_FRIDA_SERVER_FILEPATH}' -D -C"

    if config["use_su"]:
        start_frida_server_cmd = f"su -c {start_frida_server_cmd}"

    # flag "-C" avoids blocking
    proc = subprocess.run(
        [
            ADB_FILEPATH,
            "-s",
            emulator_id,
            "shell",
            start_frida_server_cmd,
        ],
    )

    print("info: frida server started")


def start_reverse_proxy(emulator_id, port):
    proc = subprocess.run(
        [ADB_FILEPATH, "-s", emulator_id, "reverse", f"tcp:{port}", f"tcp:{port}"],
    )
    print("info: adb reverse proxy started")


def pull_file(emulator_id, remote_filepath, local_filepath):
    proc = subprocess.run(
        [ADB_FILEPATH, "-s", emulator_id, "pull", remote_filepath, local_filepath],
    )
    print(f"info: pulled remote {remote_filepath} to local {local_filepath}")


def clear_dumped_json(emulator_id):
    proc = subprocess.run(
        [
            ADB_FILEPATH,
            "-s",
            emulator_id,
            "shell",
            "rm",
            "/sdcard/Android/data/com.hypergryph.arknights/files/*.json",
            "/sdcard/Android/data/com.hypergryph.arknights/files/*.cs",
        ],
    )
