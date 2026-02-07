$ErrorActionPreference = "Stop"
pyinstaller src\win_binary\main.py
Copy-Item -Path "conf", "frida-gadget", "frida-server", "platform-tools", "rel"  -Destination "dist\main" -Recurse
