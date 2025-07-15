import { useEffect, useRef } from 'react';
import type { OutputLine } from '../types';

interface OutputPanelProps {
  outputLines: OutputLine[];
  clearOutput: () => void;
}

export default function OutputPanel({ outputLines, clearOutput }: OutputPanelProps) {
  const outputRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new output is added
  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [outputLines]);

  const formatText = (text: string) => {
    // Handle newlines by converting them to <br> tags
    if (text.includes('\n')) {
      const escapedText = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#x27;')
        .replace(/\n/g, '<br>');
      return { __html: escapedText };
    }
    return null;
  };

  return (
    <div className="output-panel">
      <div className="panel-header">
        Console Output
        <div className="controls">
          <button className="btn btn-secondary" onClick={clearOutput}>
            🗑️ Clear Output
          </button>
        </div>
      </div>
      <div className="output-content" ref={outputRef}>
        {outputLines.map((line, index) => {
          const formattedText = formatText(line.text);
          return (
            <div 
              key={index} 
              className={`output-line${line.type ? ` output-${line.type}` : ''}`}
            >
              {formattedText ? (
                <span dangerouslySetInnerHTML={formattedText} />
              ) : (
                line.text
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
} 