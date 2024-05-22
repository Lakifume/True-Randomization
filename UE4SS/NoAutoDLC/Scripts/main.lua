local gameInstance = FindFirstOf("PBGameInstance")
local enableAutoDLC = false

function CanExecuteCommand()
    return GetGameInstance():GetGameModeType() == 0
end

RegisterHook("/Script/ProjectBlood.PBLoadingManager:ShowLoadingScreen", function()
    if not enableAutoDLC then
        GetGameInstance().pDLCManager.m_DLCs[9].Available  = false
        GetGameInstance().pDLCManager.m_DLCs[10].Available = false
        GetGameInstance().pDLCManager.m_DLCs[11].Available = false
        GetGameInstance().pDLCManager.m_DLCs[12].Available = false
    end
end)

RegisterKeyBind(Key.F4, function()
    if CanExecuteCommand() then
        enableAutoDLC = not enableAutoDLC
        GetGameInstance():OCDisplayMsg("Automatic costume DLC " .. (enableAutoDLC and "enabled" or "disabled"), 3.0, 0, 0, false)
    end
end)

function GetGameInstance()
    if not gameInstance:IsValid() then
        gameInstance = FindFirstOf("PBGameInstance")
    end
    return gameInstance
end