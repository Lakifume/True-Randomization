function TableContains(table, value)
    for i = 1, #table do
        if (table[i] == value) then
            return true
        end
    end
    return false
end

function Print(...)
    local param = tostring(...)
    if (...).ToString ~= nil then param = (...):ToString() end
    print("[RandoUtils] " .. param .. "\n")
end