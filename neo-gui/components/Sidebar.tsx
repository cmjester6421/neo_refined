interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
}

export default function Sidebar({ isOpen }: SidebarProps) {
  const features = [
    { icon: '🤖', name: 'AI Assistant', desc: 'Gemini-powered conversations' },
    { icon: '💻', name: 'Code Analysis', desc: 'Analyze and optimize code' },
    { icon: '🔒', name: 'Security', desc: 'Password & vulnerability tools' },
    { icon: '🖥️', name: 'System Control', desc: 'Monitor and manage system' },
    { icon: '🔬', name: 'Research', desc: 'Deep research capabilities' },
    { icon: '⚡', name: 'Automation', desc: 'Task scheduling & workflows' },
  ];

  const commands = [
    { cmd: '/ai <query>', desc: 'Ask AI anything' },
    { cmd: '/code <code>', desc: 'Analyze code' },
    { cmd: '/solve <problem>', desc: 'Problem solving' },
    { cmd: '/summarize <text>', desc: 'Summarize text' },
    { cmd: '/translate <lang> <text>', desc: 'Translate' },
  ];

  if (!isOpen) return null;

  return (
    <div className="w-80 bg-gray-800 border-r border-gray-700 p-6 overflow-y-auto">
      {/* Logo */}
      <div className="mb-8">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center">
            <span className="text-2xl font-bold">N</span>
          </div>
          <div>
            <h1 className="text-xl font-bold">NEO</h1>
            <p className="text-xs text-gray-400">Neural Executive Operator</p>
          </div>
        </div>
      </div>

      {/* Status */}
      <div className="mb-6 p-3 bg-green-500/10 border border-green-500/30 rounded-lg">
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm text-green-400">Gemini AI Active</span>
        </div>
      </div>

      {/* Features */}
      <div className="mb-8">
        <h2 className="text-sm font-semibold text-gray-400 mb-3">Features</h2>
        <div className="space-y-2">
          {features.map((feature) => (
            <div
              key={feature.name}
              className="p-3 bg-gray-700/50 rounded-lg hover:bg-gray-700 transition-colors cursor-pointer"
            >
              <div className="flex items-start space-x-3">
                <span className="text-2xl">{feature.icon}</span>
                <div>
                  <div className="text-sm font-medium">{feature.name}</div>
                  <div className="text-xs text-gray-400">{feature.desc}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Commands */}
      <div>
        <h2 className="text-sm font-semibold text-gray-400 mb-3">Quick Commands</h2>
        <div className="space-y-2">
          {commands.map((cmd) => (
            <div key={cmd.cmd} className="text-xs">
              <code className="block px-3 py-2 bg-gray-900 rounded text-blue-400 font-mono">
                {cmd.cmd}
              </code>
              <p className="text-gray-500 mt-1 px-3">{cmd.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="mt-8 pt-6 border-t border-gray-700 text-xs text-gray-500">
        <p>Version 1.0.0</p>
        <p className="mt-1">Powered by Google Gemini</p>
      </div>
    </div>
  );
}
