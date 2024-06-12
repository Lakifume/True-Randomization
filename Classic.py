from System import *
import Utility

def init():
    global item_to_level
    item_to_level = {
        "ItemCommonMoneyMedium":       "Stage_00",
        "ItemCommonMoneySmall":        "Stage_00",
        "ItemCommonMPLarge":           "Stage_00",
        "ItemCommonMPSmall":           "Stage_00",
        "ItemCommonWeaponDagger":      "Stage_00",
        "ItemCommonMagicKillAll":      "Stage_01",
        "ItemCommonMoneyLarge":        "Stage_01",
        "ItemCommonPotionInvisible":   "Stage_01",
        "ItemCommonWeaponBoneArc":     "Stage_01",
        "ItemCommonWeaponRuinousRood": "Stage_01",
        "ItemCommonWeaponUnholyFire":  "Stage_01",
        "ItemCommonMagicTimeShard":    "Stage_02",
        "ItemSecretCrown":             "Stage_02",
        "ItemSecretGoblet":            "Stage_03",
        "ItemSpecialExtraLife":        "Stage_03",
        "ItemTreasureChest":           "Stage_04",
        "ItemSecretLuckyCat":          "Stage_5A",
        "ItemSpecialFood":             "Stage_5B"
    }

def randomize_candle_drops():
    #Convert the drop dictionary to a weighted list
    classic_pool = []
    for item in constant["ClassicDrop"]:
        for num in range(constant["ClassicDrop"][item]):
            classic_pool.append(item)
    #Search for any instance of SpawnItemTypeClass and replace it with a random item
    for stage in ["Stage_00", "Stage_01", "Stage_02", "Stage_03", "Stage_04", "Stage_05A", "Stage_05B"]:
        filename = f"Classic_{stage}_Objects"
        for export in game_data[filename].Exports:
            for data in export.Data:
                if str(data.Name) != "SpawnItemTypeClass":
                    continue
                item_name = "None" if int(str(data.Value)) == 0 else str(game_data[filename].Imports[abs(int(str(data.Value))) - 1].ObjectName).split("_")[2]
                #Don't randomize the item if it isn't in the pool list
                if not item_name in classic_pool:
                    continue
                chosen_item = random.choice(classic_pool)
                data.Value = FPackageIndex(0) if chosen_item == "None" else Utility.copy_asset_import(chosen_item, f"Classic_{classic_item_to_level[chosen_item]}_Objects", filename)
                break