import frida

from config import config

JAVA_SCRIPT_FILEPATH = "rel/java.js"
NATIVE_SCRIPT_FILEPATH = "rel/native.js"
EXTRA_SCRIPT_FILEPATH = "rel/extra.js"
TRAINER_SCRIPT_FILEPATH = "rel/trainer.js"


def load_script(device, pid, script_filepath, script_config):
    session = device.attach(pid)

    with open(script_filepath, encoding="utf-8") as f:
        script_str = f.read()
    script = session.create_script(script_str)
    script.load()

    for k, v in script_config.items():
        script.post({"type": "conf", "k": k, "v": v})

    return script


def start_game(emulator_id):
    device = frida.get_device(emulator_id)

    pid = device.spawn("com.hypergryph.arknights")

    host = config["host"]
    port = config["port"]
    proxy_url = f"http://{host}:{port}"

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
    )

    extra_script = None
    if config["enable_extra"]:
        extra_script = load_script(
            device, pid, EXTRA_SCRIPT_FILEPATH, config["extra_config"]
        )

    trainer_script = None
    if config["enable_trainer"]:
        trainer_script = load_script(
            device, pid, TRAINER_SCRIPT_FILEPATH, config["trainer_config"]
        )

    device.resume(pid)
