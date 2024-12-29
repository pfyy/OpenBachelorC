call venv\Scripts\activate.bat
pip install pyinstaller==6.11.1
pyinstaller -p . --contents-directory . --add-data conf:conf --add-data frida-server:frida-server --add-data platform-tools:platform-tools --add-data rel:rel src\launcher\main.py
pause
