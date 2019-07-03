local M = {}

function M.allValues(table)
  local currentKey
  return function()
    local val
    currentKey, val = next(table, currentKey)
    return val
  end
end

function M.allKeys(table)
  local currentKey
  return function()
    local val
    currentKey, val = next(table, currentKey)
    return currentKey
  end
end

return M