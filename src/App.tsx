import { useState } from 'react';
import './styles/playground.css';
import Header from './components/Header';
import AppNavbar from './components/Navbar';
import MainContent from './components/MainContent';
import LiesOfPInterface from './components/LiesOfPInterface';
import type { ConnectionState, OutputLine, AppMode } from './types';

function App() {
  const [currentMode, setCurrentMode] = useState<AppMode>('repl');
  
  const [connection, setConnection] = useState<ConnectionState>({
    isConnected: false,
    host: 'localhost',
    port: 8172
  });

  const [outputLines, setOutputLines] = useState<OutputLine[]>([
    { text: "⚡ Welcome to UE4SS Toolkit!", type: "info" },
    { text: "🎮 Select a game mode from the dropdown above", type: "info" },
    { text: "🔌 Connect to your game's UE4SS debugger", type: "info" },
    { text: "🚀 No more save-reload cycles!", type: "info" }
  ]);

  const addOutputLine = (text: string, type: OutputLine['type'] = '') => {
    setOutputLines(prev => [...prev, { text, type }]);
  };

  const clearOutput = () => {
    setOutputLines([]);
  };

  const handleModeChange = (mode: AppMode) => {
    setCurrentMode(mode);
    clearOutput();
    
    // Add mode-specific welcome messages
    switch (mode) {
      case 'repl':
        addOutputLine("⚡ REPL Mode - Interactive Lua Console", "info");
        addOutputLine("⌨️  Type Lua commands and press Enter", "info");
        addOutputLine("💡 Try: local player = UEHelpers.GetPlayer()", "info");
        break;
      case 'lies-of-p':
        addOutputLine("🎭 Lies of P Mode - Game Management Tools", "info");
        addOutputLine("🚀 Use the teleport system to travel instantly", "info");
        addOutputLine("🔌 Connect to UE4SS to enable all features", "info");
        break;
    }
  };

  const renderContent = () => {
    switch (currentMode) {
      case 'lies-of-p':
        return (
          <LiesOfPInterface
            connection={connection}
            addOutputLine={addOutputLine}
          />
        );
      case 'repl':
      default:
        return (
          <MainContent
            connection={connection}
            outputLines={outputLines}
            addOutputLine={addOutputLine}
            clearOutput={clearOutput}
          />
        );
    }
  };

  return (
    <div>
      <AppNavbar 
        currentMode={currentMode}
        onModeChange={handleModeChange}
      />
      <Header 
        connection={connection}
        setConnection={setConnection}
        addOutputLine={addOutputLine}
      />
      {renderContent()}
    </div>
  );
}

export default App;
