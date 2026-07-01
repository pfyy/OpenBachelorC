from .config import config

if config["use_gadget"]:
    PACKAGE_NAME = "anime.pvz.online"
    # PACKAGE_NAME = "anime.pvz.online.en"
else:
    PACKAGE_NAME = "com.hypergryph.arknights"
    # PACKAGE_NAME = "com.YoStarEN.Arknights"
