local function separate(str, separator)
  local result = {}
  string.gsub(str, "[^" .. separator .. "]+",
  function(w) table.insert(result, w) end)
  return result
end

return separate