local gameInstance = FindFirstOf("PBGameInstance")

RegisterHook("/Script/ProjectBlood.PBC2ItemChest:OnOverlapChange", function(self, param1, param2)
    local chest = self:get()
    local player = GetGameInstance().m_pPBC2PlayerManager.m_pPlayer
    if chest.m_consumable == 3 and chest:IsOverlappingActor(player) then FindFirstOf("PBC2DebugHud"):GiveLife() end
end)

function GetGameInstance()
    if not gameInstance:IsValid() then
        gameInstance = FindFirstOf("PBGameInstance")
    end
    return gameInstance
end