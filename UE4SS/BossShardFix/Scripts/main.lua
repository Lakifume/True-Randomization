local gameInstance = FindFirstOf("PBGameInstance")

function CanExecuteCommand()
    local player = GetGameInstance():GetPlayerCharacter(0)
    local interfaceHUD = FindFirstOf("PBInterfaceHUD")
    if not IsInList({1, 6, 9}, GetGameInstance():GetGameModeType()) then return false end
    if not player:IsValid() then return false end
    if player:GetHitPoint() <= 0 then return false end
    if not interfaceHUD:IsValid() then return false end
    if not interfaceHUD:GetGaugeWidget():GetIsVisible() then return false end
    if GetGameInstance().LoadingManagerInstance:IsLoadingScreenVisible() then return false end
    return true
end

NotifyOnNewObject("/Script/ProjectBlood.TutorialWidgetBase", function(ConstructedObject)
    if GetClassName(ConstructedObject) == "TutorialShardWindow_C" then
        local shardWindowClosePreHook, shardWindowClosePostHook
        shardWindowClosePreHook, shardWindowClosePostHook = RegisterHook("/Game/Core/UI/Tutorialv2/TutorialShardWindow.TutorialShardWindow_C:OnCloseWindow", function()
            CheckBossSoftlock()
            UnregisterHook("/Game/Core/UI/Tutorialv2/TutorialShardWindow.TutorialShardWindow_C:OnCloseWindow", shardWindowClosePreHook, shardWindowClosePostHook)
        end)
    end
end)

function CheckBossSoftlock()
    local currentBoss = GetGameInstance().CurrentBoss
    if currentBoss:IsValid() then
        local bossName = currentBoss:GetBossId():ToString()
        if IsInList({"N1003", "N2001", "N2013"}, bossName) and currentBoss:GetHitPoint() <= 0 then
            ExecuteInGameThread(function() currentBoss:EndBossBattle(true) end)
        end
        if bossName == "N2001" then
            ExecuteWithDelay(2000, function()
                ExecuteInGameThread(function() GetGameInstance().pRoomManager:Warp(FName("m09TRN_003"), false, false, FName("None"), {}) end)
            end)
        end
    end
end

RegisterKeyBind(Key.F2, function()
    if CanExecuteCommand() then CheckBossSoftlock() end
end)

function GetGameInstance()
    if not gameInstance:IsValid() then
        gameInstance = FindFirstOf("PBGameInstance")
    end
    return gameInstance
end

function GetClassName(object)
    return SplitString(object:GetFullName(), " ")[1]
end

function IsInList(list, item)
    for index = 1,#list,1 do
        if list[index] == item then return true end
    end
    return false
end

function SplitString(inString, separator)
    local list = {}
    for subString in string.gmatch(inString, "([^"..separator.."]+)") do
        table.insert(list, subString)
    end
    return list
end