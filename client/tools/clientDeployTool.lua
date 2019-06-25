local os = require("os")
local shell = require("shell")

local args = shell.parse(...)

local urlHead = "https://raw.githubusercontent.com/JackyWangMislantiaJnirvana/CVIngameDataDisplay/client/client/"

-- lib deploy
os.execute("wget " .. urlHead .. "lib/json.lua" .. " /usr/lib/json.lua")
os.execute("wget " .. urlHead .. "lib/logging.lua" .. " /usr/lib/logging.lua")

-- binary deploy
if args[1] == "central" then
  os.execute("wget " .. urlHead .. "src/CVDDCentral.lua" .. " /home/CVDDCentral.lua")
elseif args[1] == "central" then
  os.execute("wget " .. urlHead .. "src/CVDDDataProvider.lua" .. " /usr/lib/CVDDDataProvider.lua")
end