local os = require("os")
local shell = require("shell")
local fs = require("filesystem")

local args = shell.parse(...)

local urlHead = "https://raw.githubusercontent.com/JackyWangMislantiaJnirvana/CVIngameDataDisplay/client/client/"

local function downloadFile(origin, destination)
  print("Deploying " .. destination .. ".")
  if fs.exists(destination) then
    print("File already exists. Updating.")
    os.execute("rm " .. destination)
  end
  os.execute("wget " .. urlHead .. origin .. " " .. destination)
end

-- lib deploy
downloadFile("lib/json.lua", "/usr/lib/json.lua")

downloadFile("lib/logging.lua", "/usr/lib/logging.lua")

-- binary deploy
if args[1] == "central" then
  downloadFile("src/CVDDCentral.lua", "/home/CVDDCentral.lua")
elseif args[1] == "central" then
  downloadFile("src/CVDDDataProvider.lua", "/usr/lib/CVDDDataProvider.lua")
end