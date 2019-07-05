---
--- Note: terminate the program using Ctrl+Alt+C
--- Note: internet.request() supports BOTH http and https
---

--{{{ Imports
local internet = require("internet")
local os = require("os")
local json = require("json")
local event = require("event")
local logger = require("logging").new("/home/log/central.log")
                                 :setDebug(true)
                                 :setChannel(true, true)
local serialization = require("serialization")
local component = require("component")
local iter = require("utils.iterators")

if component.modem == nil then
  error("at least one modem is required for CVDD service")
end
local modem = component.modem
--}}}

--{{{ Helpers
---@class DataPost
local DataPost = {}
DataPost.__index = DataPost

function DataPost.new(data)
  local object = {}

  --- Actual dataPost table
  ---@private
  object.data = data

  setmetatable(object, DataPost)
  return object
end

function DataPost:appendAuthHeader(apiSecret)
  self.apiSecret = apiSecret
  return self
end

function DataPost:postTo(url)
  local body = {payload = self.data, api_secret = self.apiSecret};
  local header = {}
  header["Content-Type"] = "application/json"
  self.response = internet.request(url, json.encode(body), header)
  return self
end

function DataPost:receiveAndPrintResponse()
  local success, responseMessage = pcall(function()
    local res = {}
    for chunk in self.response do
      table.insert(res, chunk)
    end
    return table.concat(res)
  end)
  if success then
    print("[ok] post was sent to and accepted by server.")
    print("---------Start-Of-Response----------")
    print(responseMessage)
    print("---------End-Of-Response------------")
  else
    logger:severe(responseMessage, "Central.receiveAndPrintResponse")
  end
end

---@class ProviderManager
local ProviderManager = {
  ---@type table<string, fun():table>
  localProviders = {},
  ---@type table<string, string>
  remoteProviders = {}
}

function ProviderManager.setPortNumber(portNumber)
  ProviderManager.portNumber = portNumber
end

function ProviderManager.setNetTimeout(netTimeout)
  ProviderManager.netTimeout = netTimeout
end

function ProviderManager.registerLocalProvider(id, callback)
  ProviderManager.localProviders[id] = callback
end

function ProviderManager.registerRemoteProvider(id, address)
  ProviderManager.remoteProviders[id] = address
end

function ProviderManager.collectData()
  local collectedData = {}
  for id, callback in pairs(ProviderManager.localProviders) do
    collectedData[id] = callback()
  end

  logger:debug("now collecting remote data", "Central.ProviderManager.collectData")
  for id, providerAddress in pairs(ProviderManager.remoteProviders) do
    modem.send(providerAddress, ProviderManager.portNumber, "REQ_DATA")
    local receivedData = select(6,
            event.pull(ProviderManager.netTimeout,
                    "modem_message",
                    nil,
                    providerAddress,
                    ProviderManager.portNumber,
                    nil))
    logger:debug("receivedData = " .. tostring(receivedData), "Central.ProviderManager.collectData")
    if receivedData then
      collectedData[id] = serialization.unserialize(receivedData)
    else
      logger:warning("Provider " .. id .. " do not response.", "Central.ProviderManager.collectData")
    end
  end
  logger:info("collectedData = " .. serialization.serialize(collectedData, true), "Central.ProviderManager.collectData()")
  return DataPost.new(collectedData)
end

--}}}

--{{{ Config Loader
local RUN_LEVEL = {
  localCT = 1,
  productivityCT = 2,
  localIntegrate = 3,
  productivity = 4
}
local REQUIRED_CONFIGS = {}

local env = {
  RUN_LEVEL = RUN_LEVEL
}
local config = {}

table.insert(REQUIRED_CONFIGS, "runLevel")
function env.runLevel(runLevel)
  if runLevel ~= RUN_LEVEL.localCT and
          runLevel ~= RUN_LEVEL.localIntegrate and
          runLevel ~= RUN_LEVEL.productivity and
          runLevel ~= RUN_LEVEL.productivityCT then
    logger:fatal("Invalid run level.", "Central.ConfigLoader.RunLevel")
  end
  config.runLevel = runLevel
end

table.insert(REQUIRED_CONFIGS, "baseUrl")
function env.baseUrl(baseUrl)
  if type(baseUrl) ~= "string" then
    logger:fatal("Invalid baseUrl.", "Central.ConfigLoader.BaseUrl")
  end
  config.baseUrl = baseUrl
end

table.insert(REQUIRED_CONFIGS, "username")
function env.username(username)
  if type(username) ~= "string" then
    logger:fatal("Invalid username.", "Central.ConfigLoader.Username")
  end
  config.username = username
end

table.insert(REQUIRED_CONFIGS, "apiSecret")
function env.apiSecret(apiSecret)
  if type(apiSecret) ~= "string" then
    logger:fatal("Invalid api secret.", "Central.ConfigLoader.ApiSecret")
  end
  config.apiSecret = apiSecret
end

function env.provider(hash, address)
  if type(hash) ~= "string" then
    logger:fatal("Invalid hash.", "Central.ConfigLoader.Provider")
  elseif type(address) ~= "string" then
    logger:fatal("Invalid address.", "Central.ConfigLoader.Provider")
  end
  ProviderManager.registerRemoteProvider(hash, address)
end

table.insert(REQUIRED_CONFIGS, "sleepTimeout")
function env.sleepTimeout(sleepTimeout)
  if type(sleepTimeout) ~= "number" then
    logger:fatal("Invalid sleep timeout.", "Central.ConfigLoader.SleepTimeout")
  end
  config.sleepTimeout = sleepTimeout
end

table.insert(REQUIRED_CONFIGS, "netTimeout")
function env.netTimeout(netTimeout)
  if type(netTimeout) ~= "number" then
    logger:fatal("Invalid net timeout.", "Central.ConfigLoader.NetTimeout")
  end
  config.netTimeout = netTimeout
end

table.insert(REQUIRED_CONFIGS, "portNumber")
function env.portNumber(portNumber)
  config.portNumber = portNumber
end

function env.localTestServerUrl(url)
  config.localTestServerUrl = url
end

local ok, err = pcall(loadfile("config.lua", "t", env))
if not ok then
  logger:fatal("cannot load settings, reason: " .. err, "Central.ConfigLoader")
else
  local missingConfigs = {}
  for requiredConfig in iter.allValues(REQUIRED_CONFIGS) do
    if config[requiredConfig] == nil then
      table.insert(missingConfigs, requiredConfig)
    end
  end
  if #missingConfigs ~= 0 then
    logger:severe(
            "Missing config item(s):\n" .. table.concat(missingConfigs, "\n"),
            "Central.ConfigLoader"
    )
  end
end

config.productivityUrl = table.concat {
  config.baseUrl,
  "/users/",
  config.username,
  "/update"
}

if config.runLevel == RUN_LEVEL.localCT or config.runLevel == RUN_LEVEL.localIntegrate then
  config.targetUrl = config.localTestServerUrl
elseif config.runLevel == RUN_LEVEL.productivityCT or config.runLevel == RUN_LEVEL.productivity then
  config.targetUrl = config.productivityUrl
end

ProviderManager.setNetTimeout(config.netTimeout)
ProviderManager.setPortNumber(config.portNumber)
--}}}

--{{{ Main
logger:info("===LoggerTest===", "Central.Main")
logger:warning("===LoggerTest===", "Central.Main")
logger:severe("===LoggerTest===", "Central.Main")

logger:info("Crescent Ville Data Display Client Central Data Collector", "Central.Main")
if config.runLevel == RUN_LEVEL.localCT then
  logger:info("Running local post connectivity test.", "Central.Main")
  --receiveAndPrintResponse(sendHTTPPost(config.targetUrl, testData))
  local testData = {
    status = "OK",
    message = "panda_2134 played chicken with a train; the train won."
  }
  DataPost.new(testData):appendAuthHeader(config.apiSecret):postTo(config.targetUrl):receiveAndPrintResponse()
elseif config.runLevel == RUN_LEVEL.localIntegrate or config.runLevel == RUN_LEVEL.productivity then
  if RUN_LEVEL == RUN_LEVEL.productivity then
    logger:info("Running in productivity env.", "Central.Main")
  elseif config.runLevel == RUN_LEVEL.localIntegrate then
    logger:info("Running local integrate test.", "Central.Main")
  end
  modem.open(config.portNumber)
  logger:info("Listening port " .. config.portNumber .. ".", "Central.Main")

  while true do
    ProviderManager.collectData()
                   :appendAuthHeader(config.apiSecret)
                   :postTo(config.targetUrl)
                   :receiveAndPrintResponse()

    os.sleep(config.sleepTimeout)
  end
else
  logger:severe("Run level not specified. Exiting...")
end
--}}}
