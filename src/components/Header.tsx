// React import not needed with modern JSX transform
import type { ConnectionState, OutputLine } from '../types';

interface HeaderProps {
  connection: ConnectionState;
  setConnection: React.Dispatch<React.SetStateAction<ConnectionState>>;
  addOutputLine: (text: string, type?: OutputLine['type']) => void;
}

export default function Header({ connection, setConnection, addOutputLine }: HeaderProps) {
  const toggleConnection = async () => {
    if (connection.isConnected) {
      disconnect();
    } else {
      connect();
    }
  };

  const connect = async () => {
    addOutputLine(`🔌 Connecting to ${connection.host}:${connection.port}...`, "info");
    
    try {
      const response = await fetch('/api/connect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ host: connection.host, port: connection.port })
      });
      
      const data = await response.json();
      
      if (data.success) {
        setConnection(prev => ({ ...prev, isConnected: true }));
        addOutputLine("✅ " + data.message, "success");
        addOutputLine("💡 Try: local player = UEHelpers.GetPlayer()", "info");
      } else {
        addOutputLine("❌ " + data.message, "error");
      }
    } catch (error) {
      addOutputLine("❌ Connection error: " + error, "error");
    }
  };

  const disconnect = async () => {
    try {
      const response = await fetch('/api/disconnect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      const data = await response.json();
      setConnection(prev => ({ ...prev, isConnected: false }));
      addOutputLine("⛔ " + data.message, "info");
    } catch (error) {
      addOutputLine("❌ Disconnect error: " + error, "error");
    }
  };

  const updateHost = (value: string) => {
    setConnection(prev => ({ ...prev, host: value }));
  };

  const updatePort = (value: string) => {
    const port = parseInt(value, 10);
    if (!isNaN(port)) {
      setConnection(prev => ({ ...prev, port }));
    }
  };

  return (
    <div className="header">
      <div className="title">⚡ UE4SS Lua REPL</div>
      <div className="status">
        <div className="connection-config">
          <label>Host:</label>
          <input 
            type="text" 
            value={connection.host}
            onChange={(e) => updateHost(e.target.value)}
          />
          <label>Port:</label>
          <input 
            type="text" 
            value={connection.port}
            onChange={(e) => updatePort(e.target.value)}
          />
          <button 
            className={`btn ${connection.isConnected ? 'btn-primary' : 'btn-secondary'}`}
            onClick={toggleConnection}
          >
            {connection.isConnected ? 'Disconnect' : 'Connect'}
          </button>
        </div>
        <div className={`status-indicator ${connection.isConnected ? 'connected' : ''}`}></div>
        <span>{connection.isConnected ? 'Connected' : 'Disconnected'}</span>
      </div>
    </div>
  );
} 