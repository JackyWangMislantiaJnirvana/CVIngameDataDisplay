--- logging
--- A light weight logger for OpenOS
---
--- Log Format
--- [<time stamp>][<level>][<log pusher>] <log message>

-- TODO: Update tester and test it again.

local os = require("os")
local term = require("term")

---@class LoggingLevel[]
---@private
local levels = {
  INFO = "Info",
  WARNING = "Warning",
  SEVERE = "Severe",
  FATAL = "Fatal",
  DEBUG = "Debug",
}

--- A light weight logger for OpenOS
---@class Logger
---@public
local M = {}
M.__index = M

--- mapping from log file dir to file handles
---@type table<string, file>
---@private
M.fileHandles = {}

function M.new(logFileDir)
  ---@type Logger
  local object = {}

  -- Hmmm, it seems that emmyLua
  -- cannot claim a field as private field.
  -- Sad face :(

  --- dir of file to output log
  ---@private
  object.logFileDir = logFileDir

  --- debug flag
  --- initially false
  ---@private
  object.isDebug = false

  --- write-to-filesystem flag
  --- initially true
  ---@private
  object.isFs = true

  --- echo-to-terminal flag
  --- initially true
  ---@private
  object.isEcho = true

  setmetatable(object, M)
  M.setLogDir(object, logFileDir)

  return object
end

--- Set whether the logger should
--- handle `debug` message.
---@param value boolean
function M:setDebug(value)
  checkArg(1, value, "boolean")
  self.isDebug = value
  return self
end

--- Set where to write log message.
---@param isFs boolean @write to filesystem
---@param isEcho boolean @write to terminal
function M:setChannel(isFs, isEcho)
  checkArg(1, isFs, "boolean")
  checkArg(2, isEcho, "boolean")
  self.isFs = isFs
  self.isEcho = isEcho
  return self
end

---@param logDir string
---@public
function M:setLogDir(logDir)
  checkArg(1, logDir, "string")
  self.fileHandles[logDir] = assert(io.open(logDir, "a"),
          "failed to open " .. logDir)
  self.logFileDir = logDir
  return self
end

---@param msg string
---@param loggingLevel LoggingLevel
---@param logPusher string
---@return void
---@private
function M:pushLog(msg, loggingLevel, logPusher)
  -- Log format:
  -- [time] [level] [log_pusher] log message
  local logMsg = string.format(
          "[%s][%s][%s] %s\n",
          os.date(), loggingLevel, logPusher, msg)

  if loggingLevel == levels.INFO then
    term.gpu().setForeground(0x0049FF)
    io.stdout:write(logMsg)
    term.gpu().setForeground(0xFFFFFF)
  elseif loggingLevel == levels.WARNING then
    term.gpu().setForeground(0xFFFF00)
    io.stdout:write(logMsg)
    term.gpu().setForeground(0xFFFFFF)
  elseif loggingLevel == levels.SEVERE then
    io.stderr:write(logMsg)
  elseif loggingLevel == levels.DEBUG then
    -- Debug message is not printed to screen.
  end

  -- Write to the log file
  -- Stacktrace is included in a fatal message
  if loggingLevel == levels.FATAL then
    self.fileHandles[self.logFileDir]:write(
            logMsg .. debug.traceback() .. "\n")
  else
    self.fileHandles[self.logFileDir]:write(logMsg):flush()
  end

  -- Fatal message will trigger a error
  if loggingLevel == levels.FATAL then
    error(logMsg)
  end
end
--- Log a `info` message
---@param msg string
---@return Logger
---@public
function M:info(msg, logPusher)
  checkArg(1, msg, "string")
  self:pushLog(msg, levels.INFO, logPusher)
  return self
end

--- Log a `warning` message
---@param msg string
---@return Logger
---@public
function M:warning(msg, logPusher)
  checkArg(1, msg, "string")
  self:pushLog(msg, levels.WARNING, logPusher)
  return self
end

--- Log a `severe` message
---@param msg string
---@return Logger
---@public
function M:severe(msg, logPusher)
  checkArg(1, msg, "string")
  self:pushLog(msg, levels.SEVERE, logPusher)
  return self
end

--- Log a `fatal` message
--- calling it will also generate an error
--- (A wrapper of standard error() method)
---@param msg string
---@return void
---@public
function M:fatal(msg, logPusher)
  checkArg(1, msg, "string")
  self:pushLog(msg, levels.FATAL, logPusher)
end

--- Log a `debug` message
---@param msg string
---@return Logger
---@public
function M:debug(msg, logPusher)
  checkArg(1, msg, "string")
  self:pushLog(msg, levels.DEBUG, logPusher)
  return self
end

return M
