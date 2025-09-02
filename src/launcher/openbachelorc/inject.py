import os
import time
import subprocess
import json

import frida
import requests

from .const import PACKAGE_NAME
from .config import config
from .adb import start_gadget

SCRIPT_DIRPATH = "rel1666/"

JAVA_SCRIPT_FILEPATH = os.path.join(SCRIPT_DIRPATH, "java.js")
NATIVE_SCRIPT_FILEPATH = os.path.join(SCRIPT_DIRPATH, "native.js")
EXTRA_SCRIPT_FILEPATH = os.path.join(SCRIPT_DIRPATH, "extra.js")
TRAINER_SCRIPT_FILEPATH = os.path.join(SCRIPT_DIRPATH, "trainer.js")


def test_remote_port():
    try:
        requests.get(
            "http://127.0.0.1:27042",
            proxies={"http": "", "https": ""},
            timeout=5,
        )
        return True
    except Exception:
        return False


def handle_script_message(script_filepath, message, data):
    print(f"message [{os.path.basename(script_filepath)}]:", message)


def load_script(device, pid, script_filepath, script_config, is_emulated_realm=False):
    if is_emulated_realm:
        session = device.attach(pid, realm="emulated")
    else:
        session = device.attach(pid)

    with open(script_filepath, encoding="utf-8") as f:
        script_str = f.read()
    script = session.create_script(script_str)
    script.on(
        "message",
        lambda message, data: handle_script_message(script_filepath, message, data),
    )
    script.load()

    for k, v in script_config.items():
        script.post({"type": "conf", "k": k, "v": v})

    return script


class Game:
    def __init__(
        self, device, pid, java_script, native_script, extra_script, trainer_script
    ):
        self.device = device
        self.pid = pid
        self.java_script = java_script
        self.native_script = native_script
        self.extra_script = extra_script
        self.trainer_script = trainer_script

    def exec_trainer_command(self, trainer_command_name):
        if self.trainer_script is not None:
            self.trainer_script.post(
                {"type": "conf", "k": "invoke", "v": trainer_command_name}
            )
        else:
            print("err: trainer is disabled")


def start_game(emulator_id):
    device = frida.get_remote_device()

    if config["use_gadget"]:
        pid = "Gadget"

        start_gadget(emulator_id)

        for i in range(100):
            if test_remote_port():
                break
            else:
                time.sleep(0.1)

    else:
        pid = device.spawn(PACKAGE_NAME)

    host = config["host"]
    port = config["port"]
    proxy_url = f"http://{host}:{port}"

    is_emulated_realm = config["use_emulated_realm"]

    java_script = load_script(
        device,
        pid,
        JAVA_SCRIPT_FILEPATH,
        {"proxy_url": proxy_url, "no_proxy": config["no_proxy"]},
    )
    native_script = load_script(
        device,
        pid,
        NATIVE_SCRIPT_FILEPATH,
        {"proxy_url": proxy_url, "no_proxy": config["no_proxy"]},
        is_emulated_realm=is_emulated_realm,
    )

    extra_script = None
    if config["enable_extra"]:
        extra_script = load_script(
            device,
            pid,
            EXTRA_SCRIPT_FILEPATH,
            config["extra_config"],
            is_emulated_realm=is_emulated_realm,
        )

    trainer_script = None
    if config["enable_trainer"]:
        trainer_script = load_script(
            device,
            pid,
            TRAINER_SCRIPT_FILEPATH,
            config["trainer_config"],
            is_emulated_realm=is_emulated_realm,
        )

    device.resume(pid)

    game = Game(device, pid, java_script, native_script, extra_script, trainer_script)

    return game
