--{{{ Client Run Level
-- Used for debug purpose.
-- Don't change this item if you don't know what your're doing.
runLevel(RUN_LEVEL.localIntegrate)
--}}}

--{{{ Local Test Settings
localTestServerUrl("http://127.0.0.1:5000")
--}}}

--{{{ Server Connectivity
-- No tailing "/" !!!
baseUrl("")

username("CV")
apiSecret("xxxxxxxx-xxxx-xxxx-xxxxxxxxxxxx")
--}}}

--{{{ MCU Connectivity
portNumber(1340)
sleepTimeout(20)
netTimeout(2)
--}}}

--{{{ Provider Registration
provider("2cd9f618", "b4bf4d2a-a7ad-4df9-b4f9-5593eb3a8652")
--}}}