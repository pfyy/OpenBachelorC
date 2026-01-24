from .config import config

if config["use_gadget"]:
    PACKAGE_NAME = "anime.pvz.online"
else:
    PACKAGE_NAME = "com.hypergryph.arknights"
