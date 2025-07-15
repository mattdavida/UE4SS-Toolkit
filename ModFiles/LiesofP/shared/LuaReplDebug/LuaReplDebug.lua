local debugger = require("ue4ss_debugger")
print("🧪 Testing UE4SS Debugger...")

-- Start the debugger
local success = debugger.start({
    port = 8172,
    timeout = 0
})

if success then
    print("------------ ✅ Debugger started successfully! ------------ ")
else
    print("------------ ❌ Failed to start debugger ------------ ")
    return
end

-- Background update loop using ExecuteInGameThread  
ExecuteInGameThread(function()
    local function background_update()
        if debugger.is_running() then
            debugger.update()
        end
        
        -- Schedule next update
        ExecuteWithDelay(100, background_update) -- Update every 100ms
    end
    
    background_update()
    print("🔄 Background update loop started")
end)