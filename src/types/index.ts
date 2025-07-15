export interface UE4SSFunction {
  name: string;
  desc: string;
}

export interface OutputLine {
  text: string;
  type: 'command' | 'success' | 'error' | 'info' | '';
}

export interface ConnectionState {
  isConnected: boolean;
  host: string;
  port: number;
}

export interface ApiResponse {
  success: boolean;
  result?: string;
  error?: string;
  message?: string;
  raw_output?: string;
}

export interface ReplState {
  input: string;
  history: string[];
  historyIndex: number;
  suggestions: UE4SSFunction[];
  selectedSuggestionIndex: number;
  showSuggestions: boolean;
}

// New types for game mode system
export type AppMode = 'repl' | 'lies-of-p' | 'ender-magnolia';

export interface GameMode {
  id: AppMode;
  name: string;
  description: string;
}

export type TeleportMethod = 'TeleportTo' | 'SetTeleportTarget';

export interface TeleportLocation {
  id: string;
  name: string;
  displayName: string;
  description?: string;
  chapter?: string;
  category?: string;
  subcategory?: string;
  chapterNum?: number;
}

export interface LiesOfPState {
  selectedLocation: TeleportLocation | null;
  locations: TeleportLocation[];
  isLoadingLocations: boolean;
  teleportMethod: TeleportMethod;
} 