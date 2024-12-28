import frida

from config import config

JAVA_SCRIPT_FILEPATH = "tmp/java.js"
NATIVE_SCRIPT_FILEPATH = "tmp/native.js"


def load_script(session, script_filepath):
    with open(script_filepath, encoding="utf-8") as f:
        script_str = f.read()
    script = session.create_script(script_str)
    script.load()

    host = config["host"]
    port = config["port"]
    proxy_url = f"http://{host}:{port}"

    script.post({"type": "conf", "k": "proxy_url", "v": proxy_url})
    script.post({"type": "conf", "k": "no_proxy", "v": config["no_proxy"]})

    return script


def start_game(emulator_id):
    device = frida.get_device(emulator_id)

    pid = device.spawn("com.hypergryph.arknights")

    java_session = device.attach(pid)
    native_session = device.attach(pid)

    java_script = load_script(java_session, JAVA_SCRIPT_FILEPATH)
    native_script = load_script(native_session, NATIVE_SCRIPT_FILEPATH)

    device.resume(pid)
