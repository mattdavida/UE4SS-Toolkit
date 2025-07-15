import { useState, useEffect } from 'react';
import type { ConnectionState, OutputLine, TeleportLocation, LiesOfPState, TeleportMethod } from '../types';
import GroupedSelect from './GroupedSelect';

interface TeleportSpotsApiResponse {
  success: boolean;
  message?: string;
  locations?: TeleportLocation[];
  file_generated?: boolean;
  lua_output?: string;
  error_details?: string;
  error?: string;
  data_source?: string;
}

interface LiesOfPInterfaceProps {
  connection: ConnectionState;
  addOutputLine: (text: string, type?: OutputLine['type']) => void;
}

// Component will load locations from server automatically

export default function LiesOfPInterface({ connection, addOutputLine }: LiesOfPInterfaceProps) {
  const [liesOfPState, setLiesOfPState] = useState<LiesOfPState>({
    selectedLocation: null,
    locations: [],
    isLoadingLocations: false,
    teleportMethod: 'TeleportTo'
  });

  console.log('LOCATIONS: ', liesOfPState)

  // Auto-load locations when component mounts
  useEffect(() => {
    const autoLoadLocations = async () => {
      addOutputLine("🔄 Auto-loading teleport locations...", 'info');
      
      try {
        const response = await fetch('/api/fetch-teleport-spots', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        });
        
        const data: TeleportSpotsApiResponse = await response.json();
        
        if (data.success && data.locations) {
          setLiesOfPState(prev => ({ 
            ...prev, 
            locations: data.locations || [] 
          }));

          // Enhanced success message based on data source
          if (data.data_source === 'python_structure') {
            addOutputLine(`✅ Loaded ${data.locations.length} locations from Python data structure`, 'success');
          } else if (data.data_source === 'lua_generated') {
            addOutputLine(`✅ Loaded ${data.locations.length} locations from fresh Lua generation`, 'success');
            if (data.file_generated) {
              addOutputLine(`📝 Also generated fresh location file via Lua`, 'info');
            }
          } else if (data.data_source === 'fallback') {
            addOutputLine(`💡 Using ${data.locations.length} fallback locations (Python data unavailable)`, 'info');
            if (data.error_details) {
              addOutputLine(`⚠️ Details: ${data.error_details}`, 'error');
            }
          } else {
            // Legacy handling for older responses
            addOutputLine(`📖 Loaded ${data.locations.length} locations`, 'success');
          }
        } else {
          addOutputLine(`❌ Location loading failed: ${data.error || 'Unknown error'}`, 'error');
        }
      } catch (error) {
        addOutputLine(`❌ Location loading error: ${error}`, 'error');
      }
    };

    autoLoadLocations();
  }, []); // Empty dependency array - run once on mount

  const handleLocationSelect = (location: TeleportLocation | null) => {
    setLiesOfPState(prev => ({ ...prev, selectedLocation: location }));
  };

  const handleTeleportMethodChange = (method: TeleportMethod) => {
    setLiesOfPState(prev => ({ ...prev, teleportMethod: method }));
  };

  const handleTeleport = async () => {
    if (!connection.isConnected) {
      addOutputLine("❌ Not connected to UE4SS debugger", 'error');
      return;
    }

    if (!liesOfPState.selectedLocation) {
      addOutputLine("❌ No location selected", 'error');
      return;
    }

    const location = liesOfPState.selectedLocation;
    const methodName = liesOfPState.teleportMethod;
    
    addOutputLine(`🚀 Using ${methodName} to teleport to ${location.displayName}...`, 'info');

    try {
      const command = methodName === 'TeleportTo' 
        ? `TeleportTo("${location.name}")` 
        : `SetTeleportTarget("${location.name}")`;

      const response = await fetch('/api/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ command })
      });
      
      const data = await response.json();
      
      if (data.success) {
        addOutputLine(`✅ Successfully executed ${methodName} for ${location.displayName}`, 'success');
        if (data.result) {
          addOutputLine(`UE4SS> ${data.result}`, '');
        }
      } else {
        addOutputLine(`❌ ${methodName} failed: ${data.error || 'Unknown error'}`, 'error');
      }
    } catch (error) {
      addOutputLine(`❌ Teleport error: ${error}`, 'error');
    }
  };

  const loadAvailableLocations = async () => {
    if (!connection.isConnected) {
      addOutputLine("❌ Not connected to UE4SS debugger", 'error');
      return;
    }

    setLiesOfPState(prev => ({ ...prev, isLoadingLocations: true }));
    addOutputLine("🔍 Loading available teleport locations...", 'info');

    try {
      const response = await fetch('/api/fetch-teleport-spots', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      const data: TeleportSpotsApiResponse = await response.json();
      
      if (data.success && data.locations) {
        const newLocations = data.locations;

        setLiesOfPState(prev => ({ 
          ...prev, 
          locations: newLocations 
        }));
        
        // Show appropriate message based on data source
        if (data.data_source === 'python_structure') {
          addOutputLine(`✅ Loaded ${newLocations.length} locations from Python data structure`, 'success');
          if (data.file_generated) {
            addOutputLine(`📝 Also generated fresh location file via Lua`, 'info');
          }
        } else if (data.data_source === 'fallback') {
          addOutputLine(`💡 Using ${newLocations.length} fallback locations (Python data unavailable)`, 'info');
          if (data.error_details) {
            addOutputLine(`⚠️ Details: ${data.error_details}`, 'error');
          }
        } else {
          // Legacy handling for older responses
          addOutputLine(`📖 Loaded ${newLocations.length} locations`, 'success');
        }
      } else {
        addOutputLine(`❌ Location scan failed: ${data.error || 'Unknown error'}`, 'error');
        addOutputLine("💡 Using fallback locations", 'info');
      }
    } catch (error) {
      addOutputLine(`❌ Location scan error: ${error}`, 'error');
      addOutputLine("💡 Using fallback locations", 'info');
    } finally {
      setLiesOfPState(prev => ({ ...prev, isLoadingLocations: false }));
    }
  };

  return (
    <div className="game-interface">
      <div className="game-header">
        <h2>🎭 Lies of P - Game Management</h2>
        <p>Advanced modding tools for Lies of P</p>
      </div>

      <div className="game-sections">
        {/* Teleport Section */}
        <div className="game-section">
          <div className="section-header">
            <h3>🚀 Teleport System</h3>
            <div className="section-controls">
              <button 
                className="btn btn-secondary"
                onClick={loadAvailableLocations}
                disabled={!connection.isConnected || liesOfPState.isLoadingLocations}
              >
                {liesOfPState.isLoadingLocations ? 'Loading...' : 'Refresh Locations'}
              </button>
            </div>
          </div>
          
          <div className="section-info">
            <p>📊 <strong>Data Structure Loading:</strong> Uses hardcoded Python data structure for reliable access to all 192 teleport locations. Click "Refresh" to optionally regenerate the source file.</p>
          </div>

          {/* Teleport Method Selection */}
          <div className="teleport-method-selector" style={{ marginBottom: '15px', padding: '10px', background: '#2d2d30', borderRadius: '3px' }}>
            <label style={{ color: '#cccccc', fontSize: '14px', fontWeight: 'bold', marginBottom: '8px', display: 'block' }}>
              Function to call:
            </label>
            <div style={{ display: 'flex', gap: '20px' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', color: '#ffffff' }}>
                <input
                  type="radio"
                  name="teleportMethod"
                  value="TeleportTo"
                  checked={liesOfPState.teleportMethod === 'TeleportTo'}
                  onChange={(e) => handleTeleportMethodChange(e.target.value as TeleportMethod)}
                  style={{ marginRight: '5px' }}
                />
                <div>
                  <div style={{ fontSize: '14px', fontWeight: 'bold' }}>TeleportTo</div>
                  <div style={{ fontSize: '12px', color: '#cccccc' }}>Need pocket watch instance</div>
                </div>
              </label>
              <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', color: '#ffffff' }}>
                <input
                  type="radio"
                  name="teleportMethod"
                  value="SetTeleportTarget"
                  checked={liesOfPState.teleportMethod === 'SetTeleportTarget'}
                  onChange={(e) => handleTeleportMethodChange(e.target.value as TeleportMethod)}
                  style={{ marginRight: '5px' }}
                />
                <div>
                  <div style={{ fontSize: '14px', fontWeight: 'bold' }}>SetTeleportTarget</div>
                  <div style={{ fontSize: '12px', color: '#cccccc' }}>Override pocket watch destination</div>
                </div>
              </label>
            </div>
          </div>

          <div className="teleport-controls">
            <div className="test">
              <GroupedSelect 
                locations={liesOfPState.locations}
                selectedLocation={liesOfPState.selectedLocation}
                onLocationSelect={(location) => {
                  if (location) {
                    handleLocationSelect(location);
                  }
                }}
              />
            </div>

            <button 
              className="btn btn-primary teleport-btn"
              onClick={handleTeleport}
              disabled={!connection.isConnected || !liesOfPState.selectedLocation}
            >
              {liesOfPState.teleportMethod === 'TeleportTo' ? '🎯 Teleport Now' : '📍 Set Teleport Location'}
            </button>
          </div>
        </div>

        {/* Future sections can go here */}
        <div className="game-section">
          <div className="section-header">
            <h3>⚙️ Game Settings</h3>
          </div>
          <p className="coming-soon">Additional game management features coming soon...</p>
        </div>
      </div>
    </div>
  );
} 