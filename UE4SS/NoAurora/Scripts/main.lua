local gameInstance = FindFirstOf("PBGameInstance")

NotifyOnNewObject("/Script/ProjectBlood.PBUserWidget", function(ConstructedObject)
    if GetClassName(ConstructedObject) == "PlayerCharaList_C" then
        local selecterCharaSetPreHook, selecterCharaSetPostHook
        selecterCharaSetPreHook, selecterCharaSetPostHook = RegisterHook("/Game/Core/UI/UI_Pause/Menu/LoadMenu/asset/StartupSelecter/PlayerChara/PLayerCharaList.PlayerCharaList_C:SetPlayerChara", function()
            UnregisterHook("/Game/Core/UI/UI_Pause/Menu/LoadMenu/asset/StartupSelecter/PlayerChara/PLayerCharaList.PlayerCharaList_C:SetPlayerChara", selecterCharaSetPreHook, selecterCharaSetPostHook)
            if ConstructedObject.Character == 3 then ConstructedObject:SetPlayerChara(6) end
        end)
    end
end)

function GetClassName(object)
    return SplitString(object:GetFullName(), " ")[1]
end

function SplitString(inString, separator)
    local list = {}
    for subString in string.gmatch(inString, "([^"..separator.."]+)") do
        table.insert(list, subString)
    end
    return list
end