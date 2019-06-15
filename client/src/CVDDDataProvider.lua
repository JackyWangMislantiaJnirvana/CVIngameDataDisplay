local event = require("event")
local component = require("component")
local serialization = require("serialization")
if component.modem == nil then
  error("at least one modem is required for CVDD service")
end
local modem = component.modem

---@field dataBuffer
local M = {}

M.ADDRESS_CENTRAL = ""
M.PORT_NUMBER = 0

-- Unregister? Oh, NO-WAY! that requires the original function registered, and I think
-- it's not necessary to store that.(For now, the handler function is a anonymous function)
-- If you DO want to unregister this handler, use the halt bottom.
function M.registerProviderService()
  -- Triggered when receiving Central's polling request for data.
  event.listen("modem_message",
          function(_, _, remoteAddress, port, _)
            if remoteAddress == M.ADDRESS_CENTRAL and port == M.PORT_NUMBER then
              modem.send(serialization.serialize(M.dataBuffer, false))
            else
              -- "Not my business. Go away."
              return
            end
          end)
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

function M.submitVector(name, dimension, ...)
  M.dataBuffer[name] = {
    type = "vector",
    dimension = dimension,
    value = { ... }
  }
end

return M