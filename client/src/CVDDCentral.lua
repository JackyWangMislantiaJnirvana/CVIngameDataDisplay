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
                                 :setDebug(false)
                                 :setChannel(true, true)
local serialization = require("serialization")
local component = require("component")
if component.modem == nil then
  error("at least one modem is required for CVDD service")
end
local modem = component.modem
--}}}

--{{{ Settings
local runLevelEnum = {
  localCT = 1,
  productivityCT = 2,
  localIntegrate = 3,
  productivity = 4
}

local runLevel = runLevelEnum.localIntegrate

local cvddServiceUsername = ""
local localTestServerUrl = "http://127.0.0.1:5000/"
local productivityUrl = table.concat { "/users/", cvddServiceUsername, "/update" }
local api_secret = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

local cvddPortNumber = 1340
-- how long is the time between two auto posts
-- measured in seconds
local sleepTime = 20
local netTimeout = 2

local testData = {
  status = "OK",
  message = "panda_2134 played chicken with a train; the train won."
}

if runLevel == runLevelEnum.localCT or runLevel == runLevelEnum.localIntegrate then
  targetUrl = localTestServerUrl
elseif runLevel == runLevelEnum.productivityCT or runLevel == runLevelEnum.productivity then
  targetUrl = productivityUrl
end
--}}}

--{{{ Auxs
-- Just an alias to shorten the typing.
-- When calling internet.request(), openOS
-- WON'T test the connectivity at once.
-- ANY network error will not appear until you read the response
-- data from the response object.
local function sendHTTPPost(url, data)
  return internet.request(url, data)
end

-- Network err handling is located here.
local function receiveAndPrintResponse(responseObject)
  local success, responseMessage = pcall(function()
    local res = {}
    for chunk in responseObject do
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

local function appendAuthHeader(post)
  post.api_secret = api_secret
  return post
end

local function appendPayload(post, payload)
  post.payload = json.encode(payload)
  return post
end

---@class ProviderManager
local ProviderManager = {
  ---@type table<string, fun():table>
  localProviders = {},
  remoteProviders = {}
}

function ProviderManager.registerLocalProvider(name, callback)
  ProviderManager.localProviders[name] = callback
end

function ProviderManager.registerRemoteProvider(name, address)
  ProviderManager.remoteProviders[name] = address
end

function ProviderManager.collectData()
  local collectedData = {}
  for name, callback in pairs(ProviderManager.localProviders) do
    collectedData[name] = callback()
  end

  logger:debug("now collecting remote data", "Central.ProviderManager.collectData")
  for name, providerAddress in pairs(ProviderManager.remoteProviders) do
    modem.send(providerAddress, cvddPortNumber, "REQ_DATA")
    local receivedData = select(6,
            event.pull(netTimeout,
                    "modem_message",
                    nil,
                    providerAddress,
                    cvddPortNumber,
                    nil))
    logger:debug("receivedData = " .. tostring(receivedData), "Central.ProviderManager.collectData")
    if receivedData then
      collectedData[name] = serialization.unserialize(receivedData)
    else
      logger:warning("Provider " .. name .. " do not response.", "Central.ProviderManager.collectData")
    end
  end
  logger:debug("collectedData = " .. serialization.serialize(collectedData, true), "Central.ProviderManager.collectData()")
  return collectedData
end
--}}}

--{{{ Provider Registration
ProviderManager.registerLocalProvider(
        "deathMessageProvider",
        function()
          return {
            message = {
              type = "text",
              value = "panda_2134 played chicken with a train; the train won"
            }
          }
        end
)

ProviderManager.registerRemoteProvider(
        "timer",
        "8093a0e2-c9d4-4899-97b5-84631742f166"
)
--}}}

--{{{ Main
logger:info("Crescent Ville Data Display Client Central Data Collector", "Central.Main")
if runLevel == runLevelEnum.localCT then
  logger:info("Running post connectivity test.", "Central.Main")
  receiveAndPrintResponse(sendHTTPPost(targetUrl, testData))
elseif runLevel == runLevelEnum.localIntegrate or runLevel == runLevelEnum.productivity then
  if runLevelEnum == runLevelEnum.productivity then
    logger:info("Running in productivity env.", "Central.Main")
  elseif runLevel == runLevelEnum.localIntegrate then
    logger:info("Running local integrate test.", "Central.Main")
  end
  modem.open(cvddPortNumber)
  logger:info("Listening port " .. cvddPortNumber .. ".", "Central.Main")

  while true do
    -- wow, I want a pipeline
    receiveAndPrintResponse(
            sendHTTPPost(
                    targetUrl,
                    appendAuthHeader(
                            appendPayload({},
                                    ProviderManager.collectData())
                    )
            )
    )
    os.sleep(sleepTime)
  end
end
--}}}