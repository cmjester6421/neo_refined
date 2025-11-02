import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { command } = await request.json();

    if (!command) {
      return NextResponse.json(
        { error: 'Command is required' },
        { status: 400 }
      );
    }

    // Call the Python backend (FastAPI server)
    const backendUrl = process.env.NEO_BACKEND_URL || 'http://localhost:8000';
    
    const response = await fetch(`${backendUrl}/api/command`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ command }),
    });

    if (!response.ok) {
      throw new Error('Backend request failed');
    }

    const data = await response.json();

    return NextResponse.json({
      response: data.response || data.message,
      command_type: data.type || data.command_type,
      data: data.data,
    });
  } catch (error) {
    console.error('NEO API Error:', error);
    return NextResponse.json(
      {
        response: 'Sorry, I encountered an error processing your request. Please ensure the NEO backend server is running.',
        error: String(error),
      },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'NEO API is running',
    version: '1.0.0',
    status: 'online',
  });
}
