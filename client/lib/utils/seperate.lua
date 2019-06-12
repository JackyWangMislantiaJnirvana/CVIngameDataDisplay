local function seperate(str, seperator)
  local result = {}
  string.gsub(str, "[^"..seperator.."]+",
  function(w) table.insert(result, w) end)
  return result
end

return seperate