# NEO AI Assistant - Next.js GUI

A modern web interface for the NEO AI Assistant powered by Google Gemini.

## Features

- 🤖 Interactive chat interface with NEO AI
- 💬 Real-time command execution
- 🎨 Modern dark theme UI
- ⚡ Quick command buttons
- 📊 Status indicators
- 🔥 Powered by Google Gemini AI

## Available Commands

### AI Commands
- `/ai <prompt>` - Generate AI response
- `/code <code>` - Analyze code quality
- `/solve <problem>` - Solve problems
- `/summarize <text>` - Summarize text
- `/translate <lang> <text>` - Translate text
- `/models` - List available models
- `/help` - Show help

## Quick Start

### Prerequisites

1. **Python Backend Requirements:**
   - Python 3.8+
   - All NEO dependencies installed
   - Gemini API key configured in `/workspaces/neo/.env`

2. **Frontend Requirements:**
   - Node.js 18+
   - npm or yarn

### Running the Application

You need to run **both** the Python backend and Next.js frontend:

#### Step 1: Start the Python Backend Server

```bash
# From the root /workspaces/neo directory
cd /workspaces/neo

# Install FastAPI and uvicorn if not already installed
pip install fastapi uvicorn pydantic

# Start the backend server
python backend_server.py
```

The backend will start on `http://localhost:8000`

#### Step 2: Start the Next.js Frontend (in a new terminal)

```bash
# From the neo-gui directory
cd /workspaces/neo/neo-gui

# Install dependencies (first time only)
npm install

# Start the development server
npm run dev
```

The frontend will start on `http://localhost:3000`

#### Step 3: Open in Browser

Navigate to `http://localhost:3000` and start chatting with NEO!

## Usage Examples

### Example 1: Ask AI a Question
```
/ai What is machine learning?
```

### Example 2: Analyze Code
```
/code def hello(): print("hi")
```

### Example 3: Solve a Problem
```
/solve How do I reverse a string in Python?
```

### Example 4: Summarize Text
```
/summarize Machine learning is a branch of artificial intelligence...
```

### Example 5: Translate Text
```
/translate spanish Hello, how are you today?
```

## Project Structure

```
neo-gui/
├── app/
│   ├── page.tsx              # Main chat interface
│   ├── layout.tsx            # Root layout
│   ├── globals.css           # Global styles
│   └── api/
│       └── neo/
│           └── route.ts      # API route handler
├── components/
│   ├── ChatMessage.tsx       # Message display component
│   ├── CommandInput.tsx      # Input form component
│   ├── Sidebar.tsx           # Features sidebar
│   └── Header.tsx            # Top navigation
├── .env.local                # Environment variables
└── package.json              # Dependencies
```

## Configuration

### Environment Variables

Create a `.env.local` file in the `neo-gui` directory:

```env
NEO_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=NEO AI Assistant
NEXT_PUBLIC_VERSION=1.0.0
```

### Backend Configuration

The backend server configuration is in `backend_server.py`. Default settings:
- Host: `0.0.0.0`
- Port: `8000`
- CORS enabled for `localhost:3000` and `localhost:3001`

## Development

### Install Dependencies

```bash
npm install
```

### Run Development Server

```bash
npm run dev
```

### Build for Production

```bash
npm run build
npm start
```

### Lint Code

```bash
npm run lint
```

## Tech Stack

### Frontend
- **Framework:** Next.js 16.0.1
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **UI:** React components

### Backend
- **Framework:** FastAPI
- **Language:** Python 3.8+
- **AI Engine:** Google Gemini API
- **Server:** Uvicorn

## Troubleshooting

### Backend Connection Issues

If you see "Please ensure the NEO backend server is running":

1. Verify the backend is running on port 8000
2. Check `.env.local` has correct `NEO_BACKEND_URL`
3. Ensure no firewall blocking localhost:8000

### CORS Errors

If you see CORS errors in browser console:

1. Check backend allows your frontend URL in CORS middleware
2. Restart the backend server after changes

### Gemini API Errors

If commands fail with API errors:

1. Verify Gemini API key in `/workspaces/neo/.env`
2. Check API key is valid and has quota
3. Test backend directly: `curl http://localhost:8000/api/health`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

Part of the NEO AI Assistant project.

## Support

For issues or questions:
- Check the main NEO documentation
- Review the USAGE.md file
- Open an issue on GitHub

---

Built with ❤️ using Next.js and Google Gemini AI
