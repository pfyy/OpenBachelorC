import sys
import argparse

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import WordCompleter

from .adb import (
    get_running_emulators,
    connect_to_emulator,
    upload_frida_server_if_necessary,
    start_frida_server,
    start_reverse_proxy,
    clear_forward_proxy,
    start_forward_proxy,
    clear_dumped_json,
    kill_frida_server,
    kill_root_process,
)
from .config import config
from .inject import start_game
from .util import register_callback_func, invoke_callback_func
from .dump import pull_dumped_json


command_lst = [
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
    "cloner_assist",
    "allow_dup_char",
]

trainer_word_completer = WordCompleter(
    [
        "enable",
        "disable",
        *command_lst,
        "all",
    ],
    match_middle=True,
)


def setup_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no_proxy", action="store_true")
    parser.add_argument("--dump_json", action="store_true")
    args = parser.parse_args()

    if args.no_proxy:
        config["no_proxy"] = True

    if args.dump_json:
        config["enable_trainer"] = True
        config["trainer_config"]["dump_json"] = True

    if config["no_proxy"] and config["enable_trainer"]:
        print("warn: trainer is disabled when no proxy is enabled")
        config["enable_trainer"] = False


def get_emulator_id():
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

    return emulator_id


def setup_game(emulator_id):
    upload_frida_server_if_necessary(emulator_id)

    kill_root_process(emulator_id, "florida-")

    if not config["use_gadget"]:
        start_frida_server(emulator_id)

    host = config["host"]
    port = config["port"]

    if host == "127.0.0.1":
        start_reverse_proxy(emulator_id, port)

    multiplayer_port = config["multiplayer_port"]
    if multiplayer_port > 0:
        start_reverse_proxy(emulator_id, multiplayer_port)

    icebreaker_port = config["icebreaker_port"]
    if icebreaker_port > 0:
        start_reverse_proxy(emulator_id, icebreaker_port)

    frida_port = config["frida_port"]
    gadget_port = config["gadget_port"]

    clear_forward_proxy(emulator_id)
    if config["use_gadget"]:
        start_forward_proxy(emulator_id, gadget_port)
    else:
        start_forward_proxy(emulator_id, frida_port)

    game = start_game(emulator_id)

    print("info: game started")

    return game


def run_cmd(game, text):
    cmd_arr = text.split()
    cmd_flag = True

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
        if cmd == "all":
            for rel_cmd in command_lst:
                game.exec_trainer_command(f"{cmd_prefix}{rel_cmd}")
        else:
            game.exec_trainer_command(f"{cmd_prefix}{cmd}")


def setup_cli(emulator_id, game):
    register_callback_func("pull_dumped_json", lambda: pull_dumped_json(emulator_id))
    register_callback_func("clear_dumped_json", lambda: clear_dumped_json(emulator_id))

    session = PromptSession(
        history=FileHistory("trainer.txt"), completer=trainer_word_completer
    )

    while True:
        try:
            text = session.prompt("> ").strip()
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

        if not text:
            continue

        if text.startswith("?"):
            invoke_callback_func(text[1:])
            continue

        if text.startswith("!"):
            game.exec_trainer_command(text[1:])
            continue

        run_cmd(game, text)


def cleanup(emulator_id):
    kill_frida_server(emulator_id)


def main():
    try:
        setup_config()

        emulator_id = get_emulator_id()

        game = setup_game(emulator_id)

        print("----------")

        setup_cli(emulator_id, game)

    finally:
        cleanup(emulator_id)


if __name__ == "__main__":
    main()
