local dataProvider = require("CVDDDataProvider")
local os = require("os")
local sep = require("utils.separate")
local SLEEP_TIME = 20
dataProvider.registerProviderService()

-- Main loop of MCU
while true do

  -- Generate some data to submit
  -- Data should be submitted in the form of a
  -- key-value-pair table
  local separated = sep(os.date(), " ")

  -- Submit data anytime as you like
  -- Calling this method does not cause any blocking,
  -- because data submitted is stored in local buffer.
  dataProvider.submitText("date", separated[1])
  dataProvider.submitText("time", separated[2])

  os.sleep(SLEEP_TIME)
end
