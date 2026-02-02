from pathlib import Path
import shutil
import lzma
from tkinter.filedialog import askopenfilename

import lief


FRIDA_VERSION = "17.6.2"
FRIDA_GADGET_XZ_FILEPATH = (
    f"frida-gadget/frida-gadget-{FRIDA_VERSION}-windows-x86_64.dll.xz"
)

FRIDA_GADGET_FILENAME = f"florida-{FRIDA_VERSION}.dll"


def main():
    ak_filepath = askopenfilename(filetypes=[("Arknights", "Arknights.exe")])
    if not ak_filepath:
        print("err: Arknights.exe not given")
        exit(1)

    ak_filepath = Path(ak_filepath)

    victim_dll_filepath = ak_filepath.parent / "hgsdk.dll"
    if not victim_dll_filepath.is_file():
        print("err: victim dll not found")
        exit(1)

    victim_dll_bak_filepath = victim_dll_filepath.with_name(
        victim_dll_filepath.name + ".bak"
    )
    if not victim_dll_bak_filepath.is_file():
        shutil.copy(victim_dll_filepath, victim_dll_bak_filepath)

    frida_dll_filepath = ak_filepath.parent / FRIDA_GADGET_FILENAME
    with lzma.open(FRIDA_GADGET_XZ_FILEPATH) as f:
        frida_dll_filepath.write_bytes(f.read())

    # ----------

    victim_dll = lief.PE.parse(victim_dll_bak_filepath)

    frida_import = victim_dll.add_import(FRIDA_GADGET_FILENAME)
    frida_import.add_entry("_frida_application_query_options_deserialize")

    lief_config = lief.PE.Builder.config_t()
    lief_config.imports = True

    # what is your fucking default, lief?
    lief_config.tls = False

    victim_dll.write(victim_dll_filepath, config=lief_config)


if __name__ == "__main__":
    main()
