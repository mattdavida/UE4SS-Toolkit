import { useState, useRef, useEffect } from 'react';
import type { ConnectionState, OutputLine, UE4SSFunction, ReplState } from '../types';

interface ReplPanelProps {
  connection: ConnectionState;
  addOutputLine: (text: string, type?: OutputLine['type']) => void;
}

// UE4SS functions for autocomplete (from original HTML)
const ue4ssFunctions: UE4SSFunction[] = [
  // Global UE4SS functions
  { name: "FindFirstOf(", desc: "Find first object of class" },
  { name: "FindAllOf(", desc: "Find all objects of class" },
  { name: "StaticFindObject(", desc: "Find object by name" },
  { name: "CreateInvalidObject()", desc: "Create invalid UObject" },
  { name: "print(", desc: "Print to console" },
  { name: "ExecuteInGameThread(", desc: "Execute code in game thread" },
  { name: "RegisterHook(", desc: "Register function hook" },
  { name: "DumpAllObjects()", desc: "Dump all objects to file" },
  { name: "GenerateSDK()", desc: "Generate C++ SDK" },
  { name: "LoadAsset(", desc: "Load asset by path" },
  { name: "ForEachUObject(", desc: "Iterate all UObjects" },
  { name: "NotifyOnNewObject(", desc: "Hook object construction" },
  { name: "RegisterKeyBind(", desc: "Register key binding" },
  { name: "FName(", desc: "Create FName" },
  { name: "FText(", desc: "Create FText" },
  
  // UEHelpers functions
  { name: "UEHelpers.GetPlayer()", desc: "Get the current player pawn" },
  { name: "UEHelpers.GetPlayerController()", desc: "Get the first player controller" },
  { name: "UEHelpers.GetEngine()", desc: "Get UEngine instance" },
  { name: "UEHelpers.GetGameInstance()", desc: "Get UGameInstance" },
  { name: "UEHelpers.GetWorld()", desc: "Get the main UWorld" },
  { name: "UEHelpers.GetGameViewportClient()", desc: "Get main viewport client" },
  { name: "UEHelpers.GetPersistentLevel()", desc: "Get UWorld->PersistentLevel" },
  { name: "UEHelpers.GetGameModeBase()", desc: "Get UWorld->AuthorityGameMode" },
  { name: "UEHelpers.GetGameStateBase()", desc: "Get UWorld->GameState" },
  { name: "UEHelpers.GetWorldSettings()", desc: "Get PersistentLevel->WorldSettings" },
  { name: "UEHelpers.GetWorldContextObject()", desc: "Get object for WorldContext parameter" },
  { name: "UEHelpers.GetAllPlayerStates()", desc: "Get array of all APlayerState" },
  { name: "UEHelpers.GetAllPlayers()", desc: "Get all players as APawn array" },
  { name: "UEHelpers.GetActorFromHitResult(", desc: "Get hit actor from FHitResult" },
  { name: "UEHelpers.GetGameplayStatics()", desc: "Get UGameplayStatics CDO" },
  { name: "UEHelpers.GetKismetSystemLibrary()", desc: "Get UKismetSystemLibrary CDO" },
  { name: "UEHelpers.GetKismetMathLibrary()", desc: "Get UKismetMathLibrary CDO" },
  { name: "UEHelpers.GetKismetStringLibrary()", desc: "Get UKismetStringLibrary CDO" },
  { name: "UEHelpers.GetKismetTextLibrary()", desc: "Get UKismetTextLibrary CDO" },
  { name: "UEHelpers.GetGameMapsSettings()", desc: "Get UGameMapsSettings CDO" },
  { name: "UEHelpers.FindFName(", desc: "Find existing FName or return None" },
  { name: "UEHelpers.AddFName(", desc: "Add new FName to pool" },
  { name: "UEHelpers.FindOrAddFName(", desc: "Find or add FName to pool" },
  { name: "UEHelpers.GetUEHelpersVersion()", desc: "Get UEHelpers module version" }
];

export default function ReplPanel({ connection, addOutputLine }: ReplPanelProps) {
  const [replState, setReplState] = useState<ReplState>({
    input: '',
    history: [],
    historyIndex: -1,
    suggestions: [],
    selectedSuggestionIndex: -1,
    showSuggestions: false
  });

  const inputRef = useRef<HTMLInputElement>(null);
  const suggestionsRef = useRef<HTMLDivElement>(null);

  // Focus input on mount
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  const showAutocomplete = (value: string) => {
    const input = value.toLowerCase().trim();
    
    if (!input) {
      hideAutocomplete();
      return;
    }
    
    const matches = ue4ssFunctions.filter(func => 
      func.name.toLowerCase().includes(input) ||
      func.desc.toLowerCase().includes(input)
    );
    
    if (matches.length === 0) {
      hideAutocomplete();
      return;
    }
    
    setReplState(prev => ({
      ...prev,
      suggestions: matches,
      selectedSuggestionIndex: -1,
      showSuggestions: true
    }));
  };

  const hideAutocomplete = () => {
    setReplState(prev => ({
      ...prev,
      suggestions: [],
      selectedSuggestionIndex: -1,
      showSuggestions: false
    }));
  };

  const navigateSuggestions = (direction: number) => {
    setReplState(prev => {
      if (prev.suggestions.length === 0) return prev;
      
      let newIndex = prev.selectedSuggestionIndex + direction;
      
      if (newIndex < 0) {
        newIndex = prev.suggestions.length - 1;
      } else if (newIndex >= prev.suggestions.length) {
        newIndex = 0;
      }
      
      return {
        ...prev,
        selectedSuggestionIndex: newIndex
      };
    });
  };

  const selectSuggestion = (functionName: string, executeImmediately = false) => {
    let newInput = functionName;
    
    // Position cursor appropriately
    if (functionName.endsWith('()')) {
      newInput = functionName.slice(0, -2) + '()';
    } else if (functionName.endsWith('(')) {
      newInput = functionName;
    }
    
    setReplState(prev => ({
      ...prev,
      input: newInput,
      showSuggestions: false,
      suggestions: [],
      selectedSuggestionIndex: -1
    }));
    
    hideAutocomplete();
    
    if (executeImmediately) {
      setTimeout(() => executeCommand(newInput), 50);
    }
    
    // Focus input
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  const selectCurrentSuggestion = (executeImmediately = false): boolean => {
    if (!replState.showSuggestions || replState.suggestions.length === 0) {
      return false;
    }
    
    const suggestionIndex = replState.selectedSuggestionIndex >= 0 
      ? replState.selectedSuggestionIndex 
      : 0;
      
    const functionName = replState.suggestions[suggestionIndex]?.name;
    if (functionName) {
      selectSuggestion(functionName, executeImmediately);
      return true;
    }
    
    return false;
  };

  const navigateHistory = (direction: number) => {
    setReplState(prev => {
      if (prev.history.length === 0) return prev;
      
      let newIndex = prev.historyIndex + direction;
      
      if (newIndex < 0) {
        newIndex = 0;
      } else if (newIndex >= prev.history.length) {
        return {
          ...prev,
          historyIndex: prev.history.length,
          input: ''
        };
      }
      
      return {
        ...prev,
        historyIndex: newIndex,
        input: prev.history[newIndex]
      };
    });
  };

  const executeCommand = async (commandToExecute?: string) => {
    const command = commandToExecute || replState.input.trim();
    
    if (!command) return;
    
    if (!connection.isConnected) {
      addOutputLine("❌ Not connected to game! Click Connect first.", "error");
      return;
    }

    // Add to history and clear input
    setReplState(prev => ({
      ...prev,
      history: [...prev.history, command],
      historyIndex: prev.history.length + 1,
      input: commandToExecute ? prev.input : '', // Only clear if executing current input
      showSuggestions: false
    }));
    
    // Show command in output
    addOutputLine("UE4SS> " + command, "command");
    
    try {
      const response = await fetch('/api/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ command: command })
      });
      
      const data = await response.json();
      
      if (data.success) {
        if (data.result && data.result !== 'nil') {
          addOutputLine("📊 " + data.result, "success");
        }
        
                 // Show any print output
         if (data.raw_output) {
           const lines = data.raw_output.split('\n');
           lines.forEach((line: string) => {
             if (line.trim() && line.includes('📊') && !line.includes('SUCCESS:')) {
               const cleanLine = line.replace(/.*📊\s*/, '');
               if (cleanLine && cleanLine !== data.result) {
                 addOutputLine(cleanLine, "success");
               }
             }
           });
         }
      } else {
        addOutputLine("❌ " + (data.error || "Unknown error"), "error");
        if (data.error && data.error.includes("Connection lost")) {
          // Note: We would need to update connection state, but we don't have access here
          // This could be improved with better state management
        }
      }
    } catch (error) {
      addOutputLine("❌ Network error: " + error, "error");
    }
  };

  const clearHistory = () => {
    setReplState(prev => ({
      ...prev,
      history: [],
      historyIndex: -1
    }));
    addOutputLine("🗑️ Command history cleared", "info");
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      if (replState.showSuggestions) {
        const executed = selectCurrentSuggestion(true);
        if (executed) {
          return;
        }
      }
      hideAutocomplete();
      executeCommand();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (replState.showSuggestions) {
        navigateSuggestions(-1);
      } else {
        navigateHistory(-1);
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (replState.showSuggestions) {
        navigateSuggestions(1);
      } else {
        navigateHistory(1);
      }
    } else if (e.key === 'Tab') {
      e.preventDefault();
      selectCurrentSuggestion(false);
    } else if (e.key === 'Escape') {
      hideAutocomplete();
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setReplState(prev => ({ ...prev, input: value }));
    showAutocomplete(value);
  };

  const handleInputKeyUp = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if ((e.key === 'Backspace' || e.key === 'Delete') && !replState.input.trim()) {
      hideAutocomplete();
    }
  };

  return (
    <div className="repl-panel">
      <div className="panel-header">
        Interactive Lua REPL
        <div className="controls">
          <button className="btn btn-secondary" onClick={clearHistory}>
            🗑️ Clear History
          </button>
        </div>
      </div>
      
      <div className="repl-help">
        <div className="help-section">
          <div className="help-title">Quick Start:</div>
          <div>1. Connect to your running game</div>
          <div>2. Type Lua commands and press Enter</div>
          <div>3. Use ↑↓ arrow keys for command history</div>
        </div>
        
        <div className="help-section">
          <div className="help-title">⚠️ Important:</div>
          <div style={{color: '#ffcc4d'}}>• Use global variables for state persistence</div>
          <div className="help-example">✅ player = UEHelpers.GetPlayer()</div>
          <div style={{color: '#ff6b6b'}}>✗ local player = UEHelpers.GetPlayer()</div>
          <div style={{fontSize: '12px', color: '#8a8a8a', marginTop: '3px'}}>
            Each command runs in separate context
          </div>
        </div>
        
        <div className="help-section">
          <div className="help-title">Examples:</div>
          <div className="help-example">player = UEHelpers.GetPlayer()</div>
          <div className="help-example">print(player:GetFullName())</div>
          <div className="help-example">player.Health = 100</div>
          <div className="help-example">FindFirstOf("PlayerController")</div>
        </div>
        
        <div className="help-section">
          <div className="help-title">Tips:</div>
          <div>• Build state incrementally, line by line</div>
          <div>• Each command executes immediately</div>
          <div>• Variables persist between commands</div>
          <div>• Use print() to see values</div>
        </div>
      </div>
      
      <div className="repl-input-container">
        <div className="repl-input">
          <span className="prompt">UE4SS&gt;</span>
          <div className="autocomplete-container">
            <input
              ref={inputRef}
              type="text"
              value={replState.input}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              onKeyUp={handleInputKeyUp}
              placeholder="Enter Lua command and press Enter..."
            />
            {replState.showSuggestions && (
              <div 
                ref={suggestionsRef}
                className="autocomplete-suggestions" 
                style={{ display: 'block' }}
              >
                {replState.suggestions.map((func, index) => (
                  <div
                    key={index}
                    className={`autocomplete-item ${
                      index === replState.selectedSuggestionIndex ? 'selected' : ''
                    }`}
                    onClick={() => selectSuggestion(func.name, false)}
                  >
                    <span className="function-name">{func.name}</span>
                    <span className="function-desc">{func.desc}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
} 