import os
import json

from .const import PACKAGE_NAME
from .adb import pull_file

DUMP_DIRPATH = "dump/"

remote_filepath_prefix = f"/sdcard/Android/data/{PACKAGE_NAME}/files/"

remote_local_filename_mapping = {
    "dump.cs": "dump.cs",
    "skin_db (Torappu.SkinDB).json": "skin_table.json",
    "charword_db (Torappu.CharWordDB).json": "charword_table.json",
    "uni_equip_db (Torappu.UniEquipDB).json": "uniequip_table.json",
    "CharacterDB.json": "character_table.json",
    "StoryDB.json": "story_table.json",
    "stage_db (Torappu.StageDB).json": "stage_table.json",
    "handbook_info_db (Torappu.HandbookInfoDB).json": "handbook_info_table.json",
    "retro_db (Torappu.RetroDB).json": "retro_table.json",
    "display_meta_db (Torappu.DisplayMetaDB).json": "display_meta_table.json",
    "medal_db (Torappu.MedalDB).json": "medal_table.json",
    "StoryReviewDB.json": "story_review_table.json",
    "story_review_meta_db (Torappu.StoryReviewMetaDB).json": "story_review_meta_table.json",
    "enemy_handbook_db (Torappu.EnemyHandBookDB).json": "enemy_handbook_table.json",
    "activity_db (Torappu.ActivityDB).json": "activity_table.json",
    "char_patch_db (Torappu.CharPatchDB).json": "char_patch_table.json",
    "climb_tower_db (Torappu.ClimbTowerDB).json": "climb_tower_table.json",
    "building_db (Torappu.BuildingDB).json": "building_data.json",
    "sandbox_perm_db (Torappu.SandboxPermDB).json": "sandbox_perm_table.json",
    "roguelike_topic_db (Torappu.RoguelikeTopicDB).json": "roguelike_topic_table.json",
    "SkillDB.json": "skill_table.json",
    "BattleUniEquipDB.json": "battle_equip_table.json",
    "gacha_db (Torappu.GachaDB).json": "gacha_table.json",
    "item_db (Torappu.ItemDB).json": "item_table.json",
    "campaign_db (Torappu.CampaignDB).json": "campaign_table.json",
    "audio_db (Torappu.Audio.Middleware.Data.TorappuAudioDB).json": "audio_data.json",
    "ChapterDB.json": "chapter_table.json",
    "char_meta_db (Torappu.CharMetaDB).json": "char_meta_table.json",
    "charm_db (Torappu.CharmDB).json": "charm_table.json",
    "checkin_db (Torappu.CheckInDB).json": "checkin_table.json",
    "clue_db (Torappu.ClueDB).json": "clue_data.json",
    "crisis_v2_db (Torappu.CrisisV2DB).json": "crisis_v2_table.json",
    "crisis_db (Torappu.CrisisDB).json": "crisis_table.json",
    "favor_db (Torappu.FavorDB).json": "favor_table.json",
    "game_data_consts_db (Torappu.GameDataConstsDB).json": "gamedata_const.json",
    "HandbookTeamDB.json": "handbook_team_table.json",
    "hotupdate_meta_db (Torappu.HotUpdateMetaDB).json": "hotupdate_meta_table.json",
    "mission_db (Torappu.MissionDB).json": "mission_table.json",
    "open_server_db (Torappu.OpenServerDB).json": "open_server_table.json",
    "RangeDB.json": "range_table.json",
    "ReplicateDB.json": "replicate_table.json",
    "shop_client_db (Torappu.ShopClientDB).json": "shop_client_table.json",
    "tip_db (Torappu.TipDB).json": "tip_table.json",
    "TokenDB.json": "token_table.json",
    "zone_db (Torappu.ZoneDB).json": "zone_table.json",
    "init_text_db (Torappu.InitTextDB).json": "init_text.json",
    "main_text_db (Torappu.MainTextDB).json": "main_text.json",
    "meta_ui_db (Torappu.MetaUIDisplayDB).json": "meta_ui_table.json",
    "CharMasterDB.json": "char_master_table.json",
    "special_operator_db (Torappu.SpecialOperatorDB).json": "special_operator_table.json",
}


def pull_dumped_json(emulator_id):
    os.makedirs(DUMP_DIRPATH, exist_ok=True)

    err_filename_lst = []

    for remote_filename, local_filename in remote_local_filename_mapping.items():
        remote_filepath = os.path.join(remote_filepath_prefix, remote_filename)
        local_filepath = os.path.join(DUMP_DIRPATH, local_filename)
        pull_file(
            emulator_id,
            remote_filepath,
            local_filepath,
        )

        if os.path.isfile(local_filepath):
            if local_filename.endswith(".json"):
                with open(local_filepath, encoding="utf-8") as f:
                    json_obj = json.load(f)

                with open(local_filepath, "w", encoding="utf-8") as f:
                    json.dump(json_obj, f, ensure_ascii=False, indent=4)
        else:
            err_filename_lst.append(remote_filename)
            print(f"err: failed to pull remote {remote_filename}")

    print("----------")

    print(f"summary: {len(err_filename_lst)} error(s)")

    if err_filename_lst:
        print(
            "failed to pull remote",
            ",".join([remote_filename for remote_filename in err_filename_lst]),
        )
