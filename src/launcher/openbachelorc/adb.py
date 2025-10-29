import subprocess
import os
import lzma
import platform
import json

from .const import PACKAGE_NAME
from .config import config

if platform.system() == "Windows":
    ADB_FILEPATH = "platform-tools/adb.exe"
else:
    ADB_FILEPATH = "adb"

MAX_NUM_MUMU_EMU = 4
MAX_NUM_LD_EMU = 4

ARCH_TO_FRIDA_SERVER_XZ_FILEPATH = {
    "arm64-v8a": "frida-server/frida-server-17.4.2-android-arm64.xz",
    "x86_64": "frida-server/frida-server-17.4.2-android-x86_64.xz",
}

ANDROID_FRIDA_SERVER_FILEPATH = "/data/local/tmp/florida-17.4.2"

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
        emulator_id_lst.append(f"127.0.0.1:{16384 + 32 * i}")

    # LD
    for i in range(MAX_NUM_LD_EMU):
        emulator_id_lst.append(f"127.0.0.1:{5555 + 2 * i}")

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

    frida_server_binary = frida_server_binary.replace(
        b"frida-agent-<arch>.so", b"florida-123-<arch>.so"
    )

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


def run_root_cmd(emulator_id, root_cmd, kwargs=None):
    tmp_lst = []

    if config["use_su"]:
        tmp_lst = ["su", "-c"]

    if kwargs is None:
        kwargs = {}

    proc = subprocess.run(
        [
            ADB_FILEPATH,
            "-s",
            emulator_id,
            "shell",
            *tmp_lst,
            root_cmd,
        ],
        **kwargs,
    )

    return proc


def check_root(emulator_id):
    check_root_cmd = "id -u"

    proc = run_root_cmd(
        emulator_id,
        check_root_cmd,
        kwargs={
            "capture_output": True,
            "text": True,
        },
    )

    if proc.stdout.strip() == "0":
        return True

    return False


def start_frida_server(emulator_id):
    root_emulator(emulator_id)

    root_flag = check_root(emulator_id)

    if not root_flag:
        print("warn: root check failed, skipping frida server startup")
        return

    print("info: root check passed")

    frida_port = config["frida_port"]

    # flag "-C" avoids blocking
    start_frida_server_cmd = (
        f"'{ANDROID_FRIDA_SERVER_FILEPATH}' -l 127.0.0.1:{frida_port} -D -C"
    )

    proc = run_root_cmd(emulator_id, start_frida_server_cmd)

    print("info: frida server started")


def start_reverse_proxy(emulator_id, port):
    proc = subprocess.run(
        [ADB_FILEPATH, "-s", emulator_id, "reverse", f"tcp:{port}", f"tcp:{port}"],
    )
    print("info: adb reverse proxy started")


def clear_forward_proxy(emulator_id):
    proc = subprocess.run(
        [
            ADB_FILEPATH,
            "-s",
            emulator_id,
            "forward",
            "--remove-all",
        ],
    )
    print("info: adb forward proxy cleared")


def start_forward_proxy(emulator_id, remote_port, local_port=27042):
    proc = subprocess.run(
        [
            ADB_FILEPATH,
            "-s",
            emulator_id,
            "forward",
            f"tcp:{local_port}",
            f"tcp:{remote_port}",
        ],
    )
    print("info: adb forward proxy started")


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
            f"/sdcard/Android/data/{PACKAGE_NAME}/files/*.json",
            f"/sdcard/Android/data/{PACKAGE_NAME}/files/*.cs",
        ],
    )


def start_gadget(emulator_id):
    proc = subprocess.run(
        [
            ADB_FILEPATH,
            "-s",
            emulator_id,
            "shell",
            f"monkey -p {PACKAGE_NAME} -c android.intent.category.LAUNCHER 1",
        ],
    )


def upload_standalone_script(emulator_id, script_filepath, script_conf):
    script_filename = os.path.basename(script_filepath)
    script_conf_filename = os.path.splitext(script_filename)[0] + ".config"

    tmp_script_conf_filepath = os.path.join(TMP_DIRPATH, script_conf_filename)

    os.makedirs(TMP_DIRPATH, exist_ok=True)
    with open(tmp_script_conf_filepath, "w") as f:
        json.dump({"parameters": script_conf}, f, indent=4)

    proc = subprocess.run(
        [ADB_FILEPATH, "-s", emulator_id, "shell", "mkdir -p /sdcard/openbachelor"],
    )

    proc = subprocess.run(
        [
            ADB_FILEPATH,
            "-s",
            emulator_id,
            "push",
            script_filepath,
            f"/sdcard/openbachelor/{script_filename}",
        ],
    )

    proc = subprocess.run(
        [
            ADB_FILEPATH,
            "-s",
            emulator_id,
            "push",
            tmp_script_conf_filepath,
            f"/sdcard/openbachelor/{script_conf_filename}",
        ],
    )


def kill_root_process(emulator_id, process_name):
    kill_root_process_cmd = f"pkill -f '{process_name}'"

    print(f"info: killing {process_name}")
    proc = run_root_cmd(emulator_id, kill_root_process_cmd)


def kill_frida_server(emulator_id):
    process_name = os.path.basename(ANDROID_FRIDA_SERVER_FILEPATH)

    kill_root_process(emulator_id, process_name)
