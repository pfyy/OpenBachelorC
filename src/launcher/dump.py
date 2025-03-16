import os
import json

from adb import pull_file

DUMP_DIRPATH = "dump/"

remote_filepath_prefix = "/sdcard/Android/data/com.hypergryph.arknights/files/"

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
}


def pull_dumped_json(emulator_id):
    os.makedirs(DUMP_DIRPATH, exist_ok=True)

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
            print(f"err: failed to pull remote {remote_filename}")
