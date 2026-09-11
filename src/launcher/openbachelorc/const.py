from .config import config
from .region import GAME_REGION, GameRegion

if config["use_gadget"]:
    match GAME_REGION:
        case GameRegion.GAME_REGION_CN:
            PACKAGE_NAME = "anime.pvz.online"
        case GameRegion.GAME_REGION_EN:
            PACKAGE_NAME = "anime.pvz.online.en"
else:
    match GAME_REGION:
        case GameRegion.GAME_REGION_CN:
            PACKAGE_NAME = "com.hypergryph.arknights"
        case GameRegion.GAME_REGION_EN:
            PACKAGE_NAME = "com.YoStarEN.Arknights"
