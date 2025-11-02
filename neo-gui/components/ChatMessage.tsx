import React, { useState, useEffect } from 'react';

interface Message {
  id: string;
  type: 'user' | 'neo' | 'system';
  content: string;
  timestamp: Date;
  command?: string;
}

interface ChatMessageProps {
  message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);

  const isUser = message.type === 'user';
  const isSystem = message.type === 'system';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-3xl rounded-lg px-4 py-3 ${
          isUser
            ? 'bg-blue-600 text-white'
            : isSystem
            ? 'bg-yellow-600/20 text-yellow-200 border border-yellow-600/50'
            : 'bg-gray-800 text-gray-100'
        }`}
      >
        {!isUser && !isSystem && (
          <div className="flex items-center space-x-2 mb-2">
            <div className="w-6 h-6 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center text-xs font-bold">
              N
            </div>
            <span className="font-semibold text-sm text-gray-300">NEO</span>
            {message.command && (
              <span className="text-xs px-2 py-0.5 bg-blue-500/20 text-blue-400 rounded">
                {message.command}
              </span>
            )}
          </div>
        )}
        {isUser && (
          <div className="flex items-center space-x-2 mb-2">
            <div className="w-6 h-6 rounded-full bg-gray-600 flex items-center justify-center text-xs font-bold">
              U
            </div>
            <span className="font-semibold text-sm">You</span>
          </div>
        )}
        <div className="prose prose-invert max-w-none">
          <p className="whitespace-pre-wrap text-sm leading-relaxed">{message.content}</p>
        </div>
        {mounted && (
          <div className="mt-2 text-xs opacity-50">
            {message.timestamp.toLocaleTimeString()}
          </div>
        )}
      </div>
    </div>
  );
}
