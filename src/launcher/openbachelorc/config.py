import json

CONF_JSON = "conf/config.json"

with open(CONF_JSON, encoding="utf-8") as f:
    config = json.load(f)
