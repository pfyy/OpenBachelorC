from pathlib import Path
import sys
import shutil

from pc_const import AK_EXE_FILEPATH_TXT_FILEPATH, VICTIM_DLL_FILENAME


def main():
    ak_filepath = Path(Path(AK_EXE_FILEPATH_TXT_FILEPATH).read_text(encoding="utf-8"))

    victim_dll_filepath = ak_filepath.parent / VICTIM_DLL_FILENAME
    victim_dll_bak_filepath = victim_dll_filepath.with_name(
        victim_dll_filepath.name + ".bak"
    )

    if not victim_dll_bak_filepath.is_file():
        print("err: victim dll bak not found")
        sys.exit(1)

    shutil.copy2(victim_dll_bak_filepath, victim_dll_filepath)

    Path(AK_EXE_FILEPATH_TXT_FILEPATH).unlink()


if __name__ == "__main__":
    main()
