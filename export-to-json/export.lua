#!/usr/bin/env lua

local json = require ("dkjson")

-- the factorio lua files want to use data:extend so we implement it here
data = {}
data.raw = {}
function data.extend(self, otherdata)
  for _, e in ipairs(otherdata) do
    if not e.type or not e.name then
      error("Missing name or type in the following prototype definition " .. serpent.block(e))
    end
    self.raw[e.name] = e
  end
end

for k, v in ipairs(arg) do
    if k >= 1 then
        dofile(v)
    end
end


local str = json.encode(data.raw, { indent = true })

print (str)