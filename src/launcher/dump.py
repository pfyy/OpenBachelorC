import os
import json

from adb import pull_file

DUMP_DIRPATH = "dump/"

remote_filepath_prefix = "/sdcard/Android/data/com.hypergryph.arknights/files/"

remote_local_filename_mapping = {
    "Torappu.SkinTable.json": "skin_table.json",
}


def pull_dumped_json(emulator_id):
    os.makedirs(DUMP_DIRPATH, exist_ok=True)

    for remote_filename, local_filename in remote_local_filename_mapping.items():
        remote_filepath = os.path.join(remote_filepath_prefix, remote_filename)
        local_filepath = os.path.join(DUMP_DIRPATH, local_filename)
        pull_file(
            emulator_id,
            remote_filepath,
            local_filepath,
        )

        with open(local_filepath, encoding="utf-8") as f:
            json_obj = json.load(f)

        with open(local_filepath, "w", encoding="utf-8") as f:
            json.dump(json_obj, f, ensure_ascii=False, indent=4)
