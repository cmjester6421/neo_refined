import { useState } from 'react';

interface CommandInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export default function CommandInput({ onSend, disabled }: CommandInputProps) {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSend(input);
      setInput('');
    }
  };

  const quickCommands = [
    { label: 'AI Query', command: '/ai ' },
    { label: 'Code Analysis', command: '/code ' },
    { label: 'Solve Problem', command: '/solve ' },
    { label: 'System Info', command: 'show system info' },
  ];

  return (
    <div className="border-t border-gray-800 bg-gray-900 p-4">
      {/* Quick Commands */}
      <div className="mb-3 flex flex-wrap gap-2">
        {quickCommands.map((cmd) => (
          <button
            key={cmd.label}
            onClick={() => setInput(cmd.command)}
            className="text-xs px-3 py-1 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-full transition-colors"
            disabled={disabled}
          >
            {cmd.label}
          </button>
        ))}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="flex space-x-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a command or use /ai, /code, /solve..."
          className="flex-1 bg-gray-800 text-white rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
          disabled={disabled}
        />
        <button
          type="submit"
          disabled={disabled || !input.trim()}
          className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Send
        </button>
      </form>

      {/* Help Text */}
      <div className="mt-2 text-xs text-gray-500">
        Tip: Use <code className="bg-gray-800 px-1 rounded">/ai</code> for AI queries,{' '}
        <code className="bg-gray-800 px-1 rounded">/code</code> for code analysis, or{' '}
        <code className="bg-gray-800 px-1 rounded">/solve</code> for problem solving
      </div>
    </div>
  );
}
