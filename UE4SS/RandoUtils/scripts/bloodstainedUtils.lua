function ValidUObjectOrNil(uObject)
    if uObject ~= nil and uObject:IsValid() then return uObject end
    return nil
end

local gameInstanceCache
---@return UPBGameInstance?
function GetGameInstance()
    if ValidUObjectOrNil(gameInstanceCache) == nil then
        ---@type UPBGameInstance?
        gameInstanceCache = ValidUObjectOrNil(FindFirstOf("PBGameInstance"))
    end

    return gameInstanceCache
end
