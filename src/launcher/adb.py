import subprocess

ADB_FILEPATH = "platform-tools/adb.exe"

MAX_NUM_MUMU_EMU = 4
MAX_NUM_LD_EMU = 4


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
        emulator_id_lst.append(f"127.0.0.1:{16384+32*i}")

    # LD
    for i in range(MAX_NUM_LD_EMU):
        emulator_id_lst.append(f"127.0.0.1:{5555+2*i}")

    # try connecting
    proc_lst = []
    for emulator_id in emulator_id_lst:
        proc = subprocess.Popen([ADB_FILEPATH, "connect", emulator_id])
        proc_lst.append(proc)

    for proc in proc_lst:
        proc.wait()
