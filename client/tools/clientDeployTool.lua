local os = require("os")
local shell = require("shell")
local fs = require("filesystem")
local io = require("io")

local args = shell.parse(...)

local urlHead = "https://raw.githubusercontent.com/JackyWangMislantiaJnirvana/CVIngameDataDisplay/master/client/"

local function downloadFile(origin, destination)
  print("Deploying " .. destination .. ".")
  if fs.exists(destination) then
    print("File already exists. Updating.")
    os.execute("rm " .. destination)
  end
  os.execute("wget " .. urlHead .. origin .. " " .. destination)
end

-- lib deploy
print("Trying to make directories... Don't panic if they already exist.")
os.execute("mkdir /usr/lib/utils/")
os.execute("mkdir /home/log/")
downloadFile("lib/json.lua", "/usr/lib/json.lua")
downloadFile("lib/utils/separate.lua", "/usr/lib/utils/separate.lua")
downloadFile("lib/utils/iterators.lua", "/usr/lib/utils/iterators.lua")
downloadFile("lib/logging.lua", "/usr/lib/logging.lua")

-- binary deploy
if args[1] == "central" then
  downloadFile("src/CVDDCentral.lua", "/home/CVDDCentral.lua")
  downloadFile("src/config.lua", "/home/config.lua")
elseif args[1] == "mcu" then
  downloadFile("src/CVDDDataProvider.lua", "/usr/lib/CVDDDataProvider.lua")
else
  io.stderr:write("clientDeployTool: bad argument. What's accepted: central/mcu.")
end
