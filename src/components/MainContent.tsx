// React import not needed with modern JSX transform
import ReplPanel from './ReplPanel';
import OutputPanel from './OutputPanel';
import type { ConnectionState, OutputLine } from '../types';

interface MainContentProps {
  connection: ConnectionState;
  outputLines: OutputLine[];
  addOutputLine: (text: string, type?: OutputLine['type']) => void;
  clearOutput: () => void;
}

export default function MainContent({ 
  connection, 
  outputLines, 
  addOutputLine, 
  clearOutput 
}: MainContentProps) {
  return (
    <div className="">
      <ReplPanel 
        connection={connection}
        addOutputLine={addOutputLine}
      />
      <OutputPanel 
        outputLines={outputLines}
        clearOutput={clearOutput}
      />
    </div>
  );
} 