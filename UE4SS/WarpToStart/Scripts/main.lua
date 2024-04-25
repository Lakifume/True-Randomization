local gameInstance = FindFirstOf("PBGameInstance")

function CanExecuteCommand()
    local player = gameInstance:GetPlayerCharacter(0)
    local interfaceHUD = FindFirstOf("PBInterfaceHUD")
    if not IsInList({1, 6, 9}, gameInstance:GetGameModeType()) then return false end
    if not player:IsValid() then return false end
    if player:GetHitPoint() <= 0 then return false end
    if not interfaceHUD:IsValid() then return false end
    if not interfaceHUD:GetGaugeWidget():GetIsVisible() then return false end
    if gameInstance.LoadingManagerInstance:IsLoadingScreenVisible() then return false end
    return true
end

function WarpToStartingRoom()
    targetRoom = gameInstance:GetGameModePlayerType() == 6 and "m05SAN_023" or "m01SIP_000"
    ExecuteInGameThread(function() gameInstance.pRoomManager:Warp(FName(targetRoom), false, false, FName("None"), {}) end)
end

RegisterKeyBind(Key.F3, function()
    if CanExecuteCommand() then WarpToStartingRoom() end
end)

function IsInList(list, item)
    for index = 1,#list,1 do
        if list[index] == item then return true end
    end
    return false
end