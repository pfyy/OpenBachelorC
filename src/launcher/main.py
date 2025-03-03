import sys

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import WordCompleter

from adb import (
    get_running_emulators,
    connect_to_emulator,
    upload_frida_server_if_necessary,
    start_frida_server,
    start_reverse_proxy,
)
from config import config
from inject import start_game

trainer_word_completer = WordCompleter(
    [
        "enable:zero_cost",
        "disable:zero_cost",
        "enable:zero_deploy_cnt",
        "disable:zero_deploy_cnt",
        "enable:deploy_everywhere",
        "disable:deploy_everywhere",
        "enable:zero_cooldown",
        "disable:zero_cooldown",
        "enable:unlimited_token",
        "disable:unlimited_token",
        "enable:no_sp",
        "disable:no_sp",
        "enable:withdraw_everything",
        "disable:withdraw_everything",
        "enable:heal_everyone",
        "disable:heal_everyone",
        "enable:unlimited_ammo",
        "disable:unlimited_ammo",
        "enable:eat_enemy",
        "disable:eat_enemy",
        "enable:global_range",
        "disable:global_range",
        "enable:anti_air",
        "disable:anti_air",
        "enable:true_aoe",
        "disable:true_aoe",
    ]
)

if __name__ == "__main__":
    if "--no_proxy" in sys.argv:
        config["no_proxy"] = True

    if config["no_proxy"] and config["enable_trainer"]:
        print("warn: trainer is disabled when no proxy is enabled")
        config["enable_trainer"] = False

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

    game = start_game(emulator_id)

    print("info: game started")

    print("----------")

    session = PromptSession(
        history=FileHistory("trainer.txt"), completer=trainer_word_completer
    )

    while True:
        try:
            text = session.prompt("> ")
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

        for cmd in text.split():
            game.exec_trainer_command(cmd)
