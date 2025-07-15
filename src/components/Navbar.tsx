import type { AppMode, GameMode } from '../types';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
interface NavbarProps {
  currentMode: AppMode;
  onModeChange: (mode: AppMode) => void;
}

const GAME_MODES: GameMode[] = [
  {
    id: 'repl',
    name: 'REPL',
    description: 'Interactive Lua REPL Console'
  },
  {
    id: 'lies-of-p',
    name: 'Lies of P',
    description: 'Teleport & Game Management'
  },
];

export default function AppNavbar({ currentMode, onModeChange }: NavbarProps) {
  const currentGameMode = GAME_MODES.find(mode => mode.id === currentMode);

  const handleModeSelect = (eventKey: string | null) => {
    if (eventKey) {
      onModeChange(eventKey as AppMode);
    }
  };

  return (
    <Navbar expand="lg" bg="dark" variant="dark" data-bs-theme="dark">
        <Navbar.Brand href="#home">UE4SS Modding Tools</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <NavDropdown 
              title={`Mode: ${currentGameMode?.name || 'Unknown'}`} 
              id="mode-nav-dropdown"
              onSelect={handleModeSelect}
            >
              {GAME_MODES.map((mode) => (
                <NavDropdown.Item 
                  key={mode.id} 
                  eventKey={mode.id}
                  active={currentMode === mode.id}
                >
                  <strong>{mode.name}</strong>
                  <br />
                  <small className="text-muted">{mode.description}</small>
                </NavDropdown.Item>
              ))}
            </NavDropdown>
          </Nav>
        </Navbar.Collapse>
    </Navbar>
  );
} 