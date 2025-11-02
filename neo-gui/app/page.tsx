'use client';

import { useState, useRef, useEffect } from 'react';
import ChatMessage from '@/components/ChatMessage';
import CommandInput from '@/components/CommandInput';
import Sidebar from '@/components/Sidebar';
import Header from '@/components/Header';

interface Message {
  id: string;
  type: 'user' | 'neo' | 'system';
  content: string;
  timestamp: Date;
  command?: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'system',
      content: 'Welcome to NEO - Neural Executive Operator! 🤖',
      timestamp: new Date(),
    },
    {
      id: '2',
      type: 'neo',
      content: "Hello! I'm NEO, your AI-powered assistant with Google Gemini integration. How can I help you today?",
      timestamp: new Date(),
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (input: string) => {
    if (!input.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Call NEO backend API
      const response = await fetch('/api/neo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ command: input }),
      });

      const data = await response.json();

      // Add NEO response
      const neoMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'neo',
        content: data.response || 'I apologize, but I encountered an error processing your request.',
        timestamp: new Date(),
        command: data.command_type,
      };
      setMessages((prev) => [...prev, neoMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'system',
        content: 'Error connecting to NEO backend. Please ensure the server is running.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          {isLoading && (
            <div className="flex items-center space-x-2 text-gray-400">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
              <span>NEO is thinking...</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <CommandInput onSend={handleSendMessage} disabled={isLoading} />
      </div>
    </div>
  );
}
