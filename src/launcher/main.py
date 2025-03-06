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
        "enable",
        "disable",
        "zero_cost",
        "zero_deploy_cnt",
        "deploy_everywhere",
        "zero_cooldown",
        "unlimited_token",
        "no_sp",
        "withdraw_everything",
        "heal_everyone",
        "unlimited_ammo",
        "eat_enemy",
        "global_range",
        "anti_air",
        "true_aoe",
        "no_ban_card",
    ],
    match_middle=True,
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

        if text.startswith("!"):
            game.exec_trainer_command(text[1:])
            continue

        cmd_arr = text.split()
        cmd_flag = True

        if not cmd_arr:
            continue

        if cmd_arr[0] == "enable":
            cmd_arr = cmd_arr[1:]
        elif cmd_arr[0] == "disable":
            cmd_arr = cmd_arr[1:]
            cmd_flag = False

        if cmd_flag:
            cmd_prefix = "enable:"
        else:
            cmd_prefix = "disable:"

        for cmd in cmd_arr:
            game.exec_trainer_command(f"{cmd_prefix}{cmd}")
