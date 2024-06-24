local gameInstance = FindFirstOf("PBGameInstance")

function CanExecuteCommand()
    if not IsInList({1, 6, 9}, GetGameInstance():GetGameModeType()) then return false end
    if not GetGameInstance().LoadingManagerInstance:IsValid() then return false end
    if GetGameInstance().LoadingManagerInstance:IsLoadingScreenVisible() then return false end
    local player = GetGameInstance():GetPlayerCharacter(0)
    if not player:IsValid() then return false end
    if player.Killed then return false end
    if player.CurrentryWarpingByWarpRoom then return false end
    local interfaceHUD = GetGameInstance():GetLocalPlayerController().MyHUD
    if not interfaceHUD:IsValid() then return false end
    if not interfaceHUD:GetGaugeWidget():IsValid() then return false end
    if not interfaceHUD:GetGaugeWidget():GetIsVisible() then return false end
    return true
end

function WarpToStartingRoom()
    targetRoom = GetGameInstance():GetGameModePlayerType() == 6 and "m05SAN_023" or "m01SIP_000"
    ExecuteInGameThread(function() GetGameInstance().pRoomManager:Warp(FName(targetRoom), false, false, FName("None"), {}) end)
end

RegisterKeyBind(Key.F3, function()
    if CanExecuteCommand() then WarpToStartingRoom() end
end)

function GetGameInstance()
    if not gameInstance:IsValid() then
        gameInstance = FindFirstOf("PBGameInstance")
    end
    return gameInstance
end

function IsInList(list, item)
    for index = 1,#list,1 do
        if list[index] == item then return true end
    end
    return false
end