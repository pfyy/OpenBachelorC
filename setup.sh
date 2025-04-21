sudo apt update
sudo apt install -y python3-pip python3-venv adb jq
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
