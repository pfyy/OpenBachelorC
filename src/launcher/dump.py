import os
import json

from adb import pull_file

DUMP_DIRPATH = "dump/"

remote_filepath_prefix = "/sdcard/Android/data/com.hypergryph.arknights/files/"

remote_local_filename_mapping = {
    "dump.cs": "dump.cs",
    "Torappu.SkinTable.json": "skin_table.json",
    "Torappu.CharWordTable.json": "charword_table.json",
    "Torappu.UniEquipTable.json": "uniequip_table.json",
    "System.Collections.Generic.Dictionary`2[System.String,Torappu.CharacterData].json": "character_table.json",
    "System.Collections.Generic.Dictionary`2[System.String,Torappu.StoryData].json": "story_table.json",
    "Torappu.StageTable.json": "stage_table.json",
    "Torappu.HandbookInfoTable.json": "handbook_info_table.json",
    "Torappu.RetroStageTable.json": "retro_table.json",
    "Torappu.MedalData.json": "medal_table.json",
    "System.Collections.Generic.Dictionary`2[System.String,Torappu.StoryReviewGroupClientData].json": "story_review_table.json",
    "Torappu.StoryReviewMetaTable.json": "story_review_meta_table.json",
    "Torappu.EnemyHandBookDataGroup.json": "enemy_handbook_table.json",
    "Torappu.ActivityTable.json": "activity_table.json",
    "Torappu.CharPatchData.json": "char_patch_table.json",
    "Torappu.ClimbTowerTable.json": "climb_tower_table.json",
    "Torappu.BuildingData.json": "building_data.json",
    "Torappu.SandboxPermTable.json": "sandbox_perm_table.json",
    "Torappu.RoguelikeTopicTable.json": "roguelike_topic_table.json",
    "System.Collections.Generic.Dictionary`2[System.String,Torappu.SkillDataBundle].json": "skill_table.json",
    "System.Collections.Generic.Dictionary`2[System.String,Torappu.BattleEquipPack].json": "battle_equip_table.json",
    "Torappu.GachaData.json": "gacha_table.json",
    "Torappu.InventoryData.json": "item_table.json",
    "Torappu.CampaignTable.json": "campaign_table.json",
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
