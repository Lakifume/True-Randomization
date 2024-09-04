local gameInstance = FindFirstOf("PBGameInstance")

function CanExecuteCommand()
    if not IsInList({1, 6, 9}, GetGameInstance():GetGameModeType()) then return false end
    if not GetGameInstance().LoadingManagerInstance:IsValid() then return false end
    if GetGameInstance().LoadingManagerInstance:IsLoadingScreenVisible() then return false end
    local player = GetPlayerCharacter()
    if not player:IsValid() then return false end
    if player.Killed then return false end 
    if player.CurrentryWarpingByWarpRoom then return false end
    local interfaceHUD = GetPlayerController().MyHUD
    if not interfaceHUD:IsValid() then return false end
    if not interfaceHUD:GetGaugeWidget():IsValid() then return false end
    if not interfaceHUD:GetGaugeWidget():GetIsVisible() then return false end
    return true
end

function GetGameInstance()
    if not gameInstance:IsValid() then
        gameInstance = FindFirstOf("PBGameInstance")
    end
    return gameInstance
end

function GetPlayerCharacter()
    return GetGameInstance():GetPlayerCharacter(0)
end

function GetPlayerController()
    return GetGameInstance():GetLocalPlayerController()
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