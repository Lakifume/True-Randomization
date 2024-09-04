require("utility")

--Fix the boss doors not opening on certain bosses with different shards

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

--Add an option to warp back to the starting room

RegisterKeyBind(Key.F3, function()
    if CanExecuteCommand() then
        targetRoom = GetGameInstance():GetGameModePlayerType() == 6 and "m05SAN_023" or "m01SIP_000"
        ExecuteInGameThread(function() GetGameInstance().pRoomManager:Warp(FName(targetRoom), false, false, FName("None"), {}) end)
    end
end)

--Add a toggle to prevent DLC items from being given at the start of a file

local enableAutoDLC = false

RegisterHook("/Script/ProjectBlood.PBLoadingManager:ShowLoadingScreen", function()
    if not enableAutoDLC then
        GetGameInstance().pDLCManager.m_DLCs[9].Available  = false
        GetGameInstance().pDLCManager.m_DLCs[10].Available = false
        GetGameInstance().pDLCManager.m_DLCs[11].Available = false
        GetGameInstance().pDLCManager.m_DLCs[12].Available = false
    end
end)

RegisterKeyBind(Key.F4, function()
    if GetGameInstance():GetGameModeType() == 0 then
        enableAutoDLC = not enableAutoDLC
        GetGameInstance():OCDisplayMsg("Automatic costume DLC " .. (enableAutoDLC and "enabled" or "disabled"), 3.0, 0, 0, false)
    end
end)

--Replace the Aurora selection widget with Bloodless

NotifyOnNewObject("/Script/ProjectBlood.PBUserWidget", function(ConstructedObject)
    if GetClassName(ConstructedObject) == "PlayerCharaList_C" then
        local selecterCharaSetPreHook, selecterCharaSetPostHook
        selecterCharaSetPreHook, selecterCharaSetPostHook = RegisterHook("/Game/Core/UI/UI_Pause/Menu/LoadMenu/asset/StartupSelecter/PlayerChara/PLayerCharaList.PlayerCharaList_C:SetPlayerChara", function()
            UnregisterHook("/Game/Core/UI/UI_Pause/Menu/LoadMenu/asset/StartupSelecter/PlayerChara/PLayerCharaList.PlayerCharaList_C:SetPlayerChara", selecterCharaSetPreHook, selecterCharaSetPostHook)
            if ConstructedObject.Character == 3 then ConstructedObject:SetPlayerChara(6) end
        end)
    end
end)

--Display the current difficulty by recoloring the minimap outline

local difficulty_colors = {
    {R=0.0, G=1.0, B=0.0, A=1.0},
    {R=1.0, G=1.0, B=0.0, A=1.0},
    {R=1.0, G=0.0, B=0.0, A=1.0}
}

NotifyOnNewObject("/Script/ProjectBlood.PBUserWidgetMap", function(ConstructedObject)
    if GetClassName(ConstructedObject) == "MiniMapBlueprint_C" then
        local frame = ConstructedObject.Frame_Image
        local difficulty = GetGameInstance():GetGameLevel()
        if frame:IsValid() then
            frame:SetColorAndOpacity(difficulty_colors[difficulty])
        end
    end
end)

--Fix playable Bloodless' spawn location

NotifyOnNewObject("/Script/ProjectBlood.PBGameMode", function(ConstructedObject)
    if GetClassName(ConstructedObject) == "PBGameMode_Bloodless_BP_C" then
        ExecuteWithDelay(500, function()
            if GetGameInstance().pRoomManager:GetCurrentRoomId():ToString() == "m05SAN_023" then
                RespawnBloodless()
            end
        end)
    end
end)

function RespawnBloodless()
    local playerStarts = FindAllOf("PlayerStart")
    local roomCenter = GetGameInstance().pRoomManager:GetBottom()
    for index = 1,#playerStarts,1 do
        local location = playerStarts[index]:K2_GetActorLocation()
        if location.X > roomCenter.X - 1260.0 and location.X < roomCenter.X + 1260.0 and location.Z > roomCenter.Z and location.Z < roomCenter.Z + 720.0 then
            ExecuteInGameThread(function() GetPlayerCharacter():WarpToPlayerStart(playerStarts[index]) end)
            break
        end
    end
end

--Nerf the Miri Scepter melee swing by making it deplete half a bullet

local subtractBullet = false
local spawnWeaponPreHook, spawnWeaponPostHook

NotifyOnNewObject("/Script/ProjectBlood.PBStepBase", function(ConstructedObject)
    if GetClassName(ConstructedObject) == "Step_P0000_C" then
        if spawnWeaponPreHook ~= nil then UnregisterHook("/Game/Core/Character/P0000/Data/Step_P0000.Step_P0000_C:PlayerCtr_SpawnWeaponTrail", spawnWeaponPreHook, spawnWeaponPostHook) end
        spawnWeaponPreHook, spawnWeaponPostHook = RegisterHook("/Game/Core/Character/P0000/Data/Step_P0000.Step_P0000_C:PlayerCtr_SpawnWeaponTrail", function()
            inventory = GetPlayerCharacter().CharacterInventory
            if inventory:IsHoldingAMagicalGirlWand() and inventory.aEquipShortcuts.Head:ToString() ~= "Recyclehat" then
                if subtractBullet then ExecuteInGameThread(function() inventory:DecBullet() end) end
                subtractBullet = not subtractBullet
            end
        end)
    end
end)

--Fix the Effigy item from chests not giving you an extra life

RegisterHook("/Script/ProjectBlood.PBC2ItemChest:OnOverlapChange", function(self, param1, param2)
    local chest = self:get()
    local player = GetGameInstance().m_pPBC2PlayerManager.m_pPlayer
    if chest.m_consumable == 3 and chest:IsOverlappingActor(player) then FindFirstOf("PBC2DebugHud"):GiveLife() end
end)