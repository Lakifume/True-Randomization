require("utils")
require("bloodstainedUtils")

local checkedBosses = { "N1003", "N2013", "N2001" }
local warpBossDestinations = { ["N2001"] = "m09TRN_003" }
local hasWarpSucceeded = false

---@param warpTarget string
function WarpTo(warpTarget)
    if hasWarpSucceeded then return end

    ExecuteInGameThread(function()
        ---@type UPBGameInstance?
        local gameInstance = ValidUObjectOrNil(GetGameInstance())
        if gameInstance == nil then
            Print("GameInstance was invalid, cancelling warp")
            return
        end
        local currentRoom = gameInstance.pRoomManager:GetCurrentRoomId():ToString()
        if currentRoom == warpTarget then
            hasWarpSucceeded = true
            return
        end

        gameInstance.pRoomManager:Warp(FName(warpTarget), true, true, FName("None"), { A = 1, R = 0, G = 0, B = 0 })

        --Try again, in case warp failed
        ExecuteWithDelay(2000, function()
            WarpTo(warpTarget)
        end)
    end)
end

function EndBoss(currentBoss, bossName)
    currentBoss:EndBossBattle()

    if warpBossDestinations[bossName] == nil then return end

    ExecuteWithDelay(20000, function()
        hasWarpSucceeded = false
        WarpTo(warpBossDestinations[bossName])
    end)
end

function UnlockRoomIfCurrentBossDeadLoop()
    ExecuteWithDelay(1000, UnlockRoomIfCurrentBossDeadLoop)
    ExecuteInGameThread(function()
        local gameInstance = GetGameInstance()
        if gameInstance == nil then
            Print("Game instance invalid")
            return
        end

        ---@type APBBaseCharacter?
        local currentBoss = ValidUObjectOrNil(gameInstance.CurrentBoss)
        if currentBoss == nil then return end

        local bossName = currentBoss:GetBossId():ToString()
        if not TableContains(checkedBosses, bossName) then return end

        if currentBoss:GetHitPoint() > 0 then return end

        ExecuteWithDelay(8500, function()
            EndBoss(currentBoss, bossName)
        end)
    end)
end

Print("Mod loaded")
UnlockRoomIfCurrentBossDeadLoop()
