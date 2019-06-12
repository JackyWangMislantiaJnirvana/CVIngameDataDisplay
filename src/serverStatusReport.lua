---
--- Note: terminate the program using Ctrl+Alt+C
---

local internet = require("internet")
local os = require("os")
local sep = require("utils.seperate")
local json = require("json")

local url = "http://127.0.0.1:5000/"
-- how long is the time between two auto posts
-- measured in seconds
local sleepTime = 10

local testData = {
  status = "OK",
  message = "panda_2134 played chicken with a train; the train won."
}
local isTest = false

-- Just an alias to shorten the typing.
-- When calling internet.request(), openOS
-- WON'T test the connectivity at once.
-- ANY network error will not appear until you read the response
-- data from the response object.
function postData(url, data)
  return internet.request(url, data)
end

-- Network err handling is located here.
function printResponse(responseObject)
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
    io.stderr:write("[err] " .. responseMessage)
  end
end

if isTest then
  print("========Post=Connectivity=Test=======")
  print("[***] sending http post to " .. url)
  printResponse(postData(url, testData))
end

---@class ProviderManager
local ProviderManager = {
  ---@type table<string, fun():table>
  providers = {}
}

function ProviderManager.registerProvider(name, callback)
  ProviderManager.providers[name] = callback
end

----------------------------------------------------------------------------------------------
ProviderManager.registerProvider(
        "in-game date",
        function()
          local res = sep(os.date(), " ")
          return {
            date = res[1],
            time = res[2]
          }
        end
)

ProviderManager.registerProvider(
        "death message",
        function()
          return { message = "panda_2134 played chicken with a train; the train won" }
        end
)
-----------------------------------------------------------------------------------------------

if not isTest then
  while true do
    local data = {}
    for name, callback in pairs(ProviderManager.providers) do
      data[name] = json.encode(callback())
    end
    printResponse(postData(url, data))
    os.sleep(sleepTime)
  end
end
