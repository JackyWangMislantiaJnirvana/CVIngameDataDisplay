local event = require("event")
local component = require("component")
local serialization = require("serialization")
if component.modem == nil then
  error("at least one modem is required for CVDD service")
end
local modem = component.modem

local logger = require("logging").new("/home/log/provider.log")
                                 :setDebug(false)
                                 :setChannel(true, true)

---@field dataBuffer
local M = {
  dataBuffer = {}
}

M.ADDRESS_CENTRAL = "ef2ec3b8-939c-40eb-a8b2-819b643d4a2d"
M.PORT_NUMBER = 1340

-- Unregister? Oh, NO-WAY! that requires the original function registered, and I think
-- it's not necessary to store that.(For now, the handler function is a anonymous function)
-- If you DO want to unregister this handler, use the halt bottom.
function M.registerProviderService()
  -- Open the port for **listening**
  modem.open(M.PORT_NUMBER)
  logger:info("modem opened on " .. M.PORT_NUMBER, "Provider.registerProviderService")

  -- Triggered when receiving Central's polling request for data.
  event.listen("modem_message",
          function(_, _, remoteAddress, port, _)
            logger:info("req is received.", "Provider.ReqListener")
            logger:debug("remoteAddress = " .. remoteAddress, "Provider.ReqListener")
            logger:debug("port = " .. port, "Provider.ReqListener")
            logger:debug("(remoteAddress == M.ADDRESS_CENTRAL) = " .. tostring(remoteAddress == M.ADDRESS_CENTRAL),
                    "Provider.ReqListener")
            if remoteAddress == M.ADDRESS_CENTRAL and port == M.PORT_NUMBER then
              modem.send(M.ADDRESS_CENTRAL, M.PORT_NUMBER, serialization.serialize(M.dataBuffer, false))
              logger:info("response sent.", "Provider.ReqListener")
            else
              -- "Not my business. Go away."
              logger:warning("ignoring one req from "
                      .. remoteAddress ..
                      ". Make sure central address is right.", "Provider.ReqListener")
            end
            logger:debug("reached end-of-func", "Provider.ReqListener")
          end)
  logger:info("cvdd listener registered.", "Provider.registerProviderService")
end

function M.submitText(name, value)
  M.dataBuffer[name] = {
    type = "text",
    value = value
  }
end

function M.submitPhyQuantity(name, value, unit)
  M.dataBuffer[name] = {
    type = "phyQuantity",
    value = value,
    unit = unit
  }
end

function M.submitBoolean(name, value)
  M.dataBuffer[name] = {
    type = "boolean",
    value = value
  }
end

function M.submitVector(name, ...)
  M.dataBuffer[name] = {
    type = "vector",
    value = { ... }
  }
end

return M