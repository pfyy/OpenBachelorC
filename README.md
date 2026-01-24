# OpenBachelorC

OpenBachelor Client. For PvZ Online.

This project is a game launcher only. If you are looking for a game server, please look at OpenBachelor Server.

Discord: [https://discord.gg/W4yPMpBv8F](https://discord.gg/W4yPMpBv8F)


## Supported Environment

A rooted arm64 android phone.

A jailed arm64 android phone (with OpenBachelorG).

Mac (Apple silicon) with AVD (Android Studio) (recommended: arm64, Android 15, Google APIs Image).

> FYI: For AVD users, do not use Google Play Store image, which is not readily rooted.

## How-To

### 0. Start Server

1. Use a game server, preferably OpenBachelor Server.

### 1. Setup Client

1. Install Python 3.12 and add `python.exe` to path.

2. Run `setup.cmd`.

3. Open your emulator/phone's settings, enable its root permission and adb connection.

4. Run `load_config_[YOUR_DEVICE].cmd`. For example, if you are using a jailed phone (no root permission), run `load_config_jailed_phone.cmd`.

### 2. Run Client

1. Run `main.cmd`.

