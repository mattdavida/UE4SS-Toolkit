# UE4SS Toolkit - Professional Game Development Interface

**Advanced UE4SS debugging and mod development platform with real-time Lua execution, intelligent game integration, and modern web UI**

![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![Material-UI](https://img.shields.io/badge/Material--UI-0081CB?style=flat&logo=material-ui&logoColor=white)
![Development](https://img.shields.io/badge/Status-Active%20Development-orange)

## 🎯 Overview

The UE4SS Toolkit is a comprehensive development platform that revolutionizes Unreal Engine game modding and debugging. Built with modern web technologies, it provides a professional-grade interface for real-time Lua code execution, advanced game state manipulation, and sophisticated mod management through UE4SS (Unreal Engine Scripting System).

**What makes this special:**
- **Zero save-reload cycles** - Execute code instantly in running games
- **Professional debugging tools** - Auto-completion, command history, intelligent result parsing
- **Game-specific interfaces** - Custom UIs tailored for specific games (starting with Lies of P)
- **Real-time socket communication** - Bidirectional data flow with game engines
- **Modern web architecture** - TypeScript React frontend with Python Flask backend

## ✨ Key Features

### 🔧 Advanced Lua REPL
- **Interactive code execution** with 40+ UE4SS function auto-completion
- **Intelligent result parsing** - Automatic TArray/TMap unpacking and formatting
- **Command history** with up/down arrow navigation
- **Smart error handling** with detailed stack traces
- **UEHelpers integration** - Direct access to engine utilities

### 🎮 Game-Specific Interfaces
- **Lies of P Integration**: Professional teleport management with 192+ locations
- **Searchable location database** with category grouping (Base Game, DLC, Boss Challenges)
- **Dual teleport methods** - Direct teleportation vs. pocket watch targeting
- **Real-time location discovery** - Dynamic loading from game data
- **Intelligent fallback systems** - Works even when game disconnected

### 🌐 Professional Web Architecture
- **React TypeScript frontend** with Material-UI components
- **Flask Python backend** with comprehensive API
- **Real-time connection management** - IPv4/IPv6 socket handling
- **Cross-platform compatibility** - Windows, macOS, Linux support

### 🔌 Advanced Communication System
- **Socket-based debugging** - Real-time bidirectional communication
- **Connection state management** - Automatic reconnection and error recovery
- **Multi-protocol support** - IPv4/IPv6 with intelligent fallback
- **Command queuing** - Handles rapid-fire requests gracefully

## 🚀 Technical Architecture

### Frontend (React TypeScript)
```typescript
// Modern React with TypeScript, Material-UI components
interface ConnectionState {
  isConnected: boolean;
  host: string;
  port: number;
}

// Game-specific interfaces with state management
interface LiesOfPState {
  selectedLocation: TeleportLocation | null;
  locations: TeleportLocation[];
  teleportMethod: 'TeleportTo' | 'SetTeleportTarget';
}
```

### Backend (Python Flask)
```python
# API with intelligent result parsing
@app.route('/api/execute', methods=['POST'])
def api_execute():
    """Execute Lua code with auto-unpacking and formatting"""
    result = execute_lua_code(code)
    # Auto-unpack TArrays, format results, handle errors
    return enhanced_result_with_intelligent_parsing(result)
```

### UE4SS Integration
```lua
-- Direct socket communication with the running game
function execute_repl_command(command)
    -- Real-time code execution in game context
    return pcall(loadstring(command))
end
```

## 📋 Game Support

### 🎭 Lies of P (Full Integration)
- **192+ teleport locations** organized by area and type
- **Boss challenge system** with direct arena access
- **DLC integration** with Winter Sea content
- **Save game manipulation** (NG+ rounds, humanity, items)
- **Pocket watch override hooks** for seamless teleportation

### 🌸 ENDER MAGNOLIA (Coming Soon)
- Fast travel system integration
- Save state management
- Achievement/collectible tracking

### 🔧 Framework Support
The toolkit is designed as a **modular framework** - adding new games involves:
1. Creating game-specific TypeScript interfaces
2. Implementing backend API endpoints
3. Adding UE4SS mod integration
4. Building custom UI components

## 🔗 Related Repositories

This toolkit is part of a comprehensive UE4SS modding ecosystem. The following repositories work together to provide the complete experience:

### Core Dependencies
- **[UE4SS Lua Utils](https://github.com/mattdavida/UE4SS_Lua_Utils)** - Shared framework containing debugging utilities, socket communication, type definitions, and common helpers used across all of my UE4SS mods
- **[Lies of P - Ultimate Access](https://github.com/mattdavida/LiesofP-UltimateAccess)** - Complete UE4SS mod for Lies of P featuring boss access, DLC integration, teleportation system, and save manipulation

### Framework Architecture
```
UE4SS Toolkit (this repo)     # Web interface and REPL
├── UE4SS_Lua_Utils          # Shared utilities (submodule)
└── Game-Specific Mods       # Individual game integrations
    └── LiesofP-UltimateAccess
```

*Note: Future releases will integrate these as git submodules for streamlined dependency management.*

## 🛠️ Installation & Setup

### Prerequisites
- **Node.js 18+** - For frontend development
- **Python 3.8+** - For backend server
- **UE4SS** - Game-specific installation required
- **Supported Game** - Currently Lies of P, ENDER MAGNOLIA planned

### Quick Start
```bash
# Clone the repository
git clone https://github.com/your-username/ue4ss-toolkit.git
cd ue4ss-toolkit

# Install frontend dependencies
npm install

# Install backend dependencies  
pip install -r requirements.txt

# Build frontend
npm run build

# Start the server
python playground_server.py
```

Open `http://localhost:5000` and start coding!

### Game Setup
1. **Install UE4SS** in your game directory
2. **Clone mod repositories**:
   - [Lies of P Mod](https://github.com/mattdavida/LiesofP-UltimateAccess)
   - [UE4SS Lua Utils](https://github.com/mattdavida/UE4SS_Lua_Utils)
3. **Configure mods.txt** to enable the debugging mod
4. **Launch game** - The REPL automatically detects and connects

## 🔌 API Reference

### Connection Management
```javascript
POST /api/connect     // Test UE4SS debugger connection
POST /api/disconnect  // Disconnect from debugger  
GET  /api/status      // Get current connection state
```

### Code Execution
```javascript
POST /api/execute     // Execute Lua code with intelligent parsing
// Request: { "command": "UEHelpers.GetPlayer():GetActorLocation()" }
// Response: Auto-formatted with unpacked results
```

### Game Integration
```javascript
POST /api/fetch-teleport-spots  // Load game locations dynamically
// Returns: Categorized locations with fallback support
```

## 🎮 Usage Examples

### Basic Lua Execution
```lua
-- Get player information
local player = UEHelpers.GetPlayer()
print("Player location:", player:GetActorLocation())

-- Manipulate game state
FindFirstOf("PlayerCharacter"):SetActorLocation(FVector(0, 0, 100))
```

### Advanced Game Integration
```typescript
// Teleport to specific location using the interface
const locations = await fetch('/api/fetch-teleport-spots');
await executeTeleport('LD_Hotel_Main', 'TeleportTo');
```

### Real-time Debugging
```lua
-- Hook into game events for real-time monitoring
RegisterHook("BP_Player_C:TakeDamage", function(self, damage)
    print("Player took damage:", damage)
end)
```

## 🏗️ Development Architecture

### Project Structure
```
ue4ss-toolkit/
├── src/                    # React TypeScript frontend
│   ├── components/         # Reusable UI components
│   ├── types/             # TypeScript definitions
│   └── styles/            # Custom CSS styles
├── public/                 # Static assets
├── playground_server.py    # Flask backend server
├── simple_debug_parameterized.py  # UE4SS communication
└── requirements.txt        # Python dependencies
```

### Key Components
- **ReplPanel** - Interactive Lua console with auto-completion
- **LiesOfPInterface** - Game-specific teleport management
- **GroupedSelect** - Sophisticated location picker with search
- **ConnectionManager** - Real-time socket state management

## 🔬 Technical Innovations

### Intelligent Result Parsing
The system automatically detects and unpacks complex UE4SS data structures:
```python
# Automatic TArray unpacking
"TArray[192]" → Expanded list with element details
"FVector(X=100,Y=200,Z=300)" → Formatted coordinate display
"UObject*" → GetFullName() + class information
```

### Smart Connection Management
```python
# Multi-protocol connection with graceful fallback
IPv6 localhost (::1) → IPv4 fallback (127.0.0.1) → Custom host
```

### Game-Specific Data Integration
```python
# Dynamic location loading with multiple data sources
Live game data → Python structure → Static fallback
```

## 🎯 Use Cases

### For Game Modders
- **Rapid prototyping** - Test mod ideas without restart cycles
- **Debug game state** - Inspect objects, values, and relationships
- **Location discovery** - Find internal names for teleport targets

### For Speedrunners  
- **Practice specific scenarios** - Teleport to any game location instantly
- **Test routing strategies** - Quickly validate new route ideas
- **Debug movement mechanics** - Real-time position and state monitoring

### For Developers
- **Learn UE4 internals** - Explore engine systems and APIs
- **Prototype systems** - Test complex game logic interactively
- **Performance analysis** - Monitor game performance in real-time

### For Content Creators
- **Video setup** - Quickly reach any game location for recordings
- **Screenshot sessions** - Access hidden areas and debug cameras
- **Demonstration tools** - Show game mechanics and hidden features


## 🚧 Development Status

**Current Phase:** Active Development  
**Stability:** Beta - Core features working, polish ongoing  
**Feedback:** Welcome! This is a personal development project showcasing UE4SS integration techniques.

## 🤝 Contributing

This project demonstrates advanced game modding techniques and modern web development practices. Contributions are welcome!

### Development Setup
```bash
# Frontend development
npm run dev        # Start Vite dev server

# Backend development  
python playground_server.py --debug  # Enable Flask debug mode

# Type checking
npm run lint       # ESLint + TypeScript checking
```

### Adding New Games
1. **Research UE4SS compatibility** for the target game
2. **Create game-specific components** in `src/components/`
3. **Implement backend APIs** for game data integration
4. **Add TypeScript types** for game-specific data structures
5. **Build UE4SS mod** for socket communication

## 📈 Performance & Reliability

- **Sub-100ms response times** for most Lua commands
- **Automatic reconnection** on network failures
- **Graceful degradation** when game not available
- **Memory-efficient** result caching and parsing
- **Cross-platform socket handling** with IPv4/IPv6 support

## 🔒 Security Considerations

- **Local-only by default** - No external network exposure
- **Sandboxed execution** - Lua code runs in game context only
- **Input validation** - All commands validated before transmission
- **No persistent storage** - Session-based state management

## 📜 License & Attribution

This project is released under the MIT License for educational and personal use.

**Dependencies:**
- **Flask** - Backend web framework
- **React** - Frontend UI library  
- **Material-UI** - Professional UI components
- **TypeScript** - Type-safe development
- **Socket libraries** - Real-time communication

## 🚀 Future Roadmap

- **Git submodule integration** - Streamlined mod dependency management
- **One-click deployment** - Automated UE4SS setup and mod installation
- **Additional game support** - ENDER MAGNOLIA, other UE4 titles

---

**Built with ❤️ for the game modding community**

*Demonstrating the intersection of modern web development and game engine reverse engineering*
