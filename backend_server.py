"""
FastAPI Backend Server for NEO GUI
This server provides HTTP API endpoints for the Next.js frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.ai_engine import NEOAIEngine

app = FastAPI(title="NEO AI Backend", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Engine
ai_engine = NEOAIEngine()

class CommandRequest(BaseModel):
    command: str

class CommandResponse(BaseModel):
    response: str
    command_type: str
    data: dict = {}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "NEO AI Backend API",
        "version": "1.0.0",
        "status": "online",
        "gemini_status": "active" if ai_engine.gemini else "inactive"
    }

@app.get("/api/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "gemini_available": ai_engine.gemini is not None,
        "model": ai_engine.gemini.model_name if ai_engine.gemini else None
    }

@app.post("/api/command", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    """Execute a NEO command and return the response"""
    try:
        command = request.command.strip()
        
        if not command:
            raise HTTPException(status_code=400, detail="Command cannot be empty")
        
        # Determine command type
        command_type = "general"
        if command.startswith("/ai "):
            command_type = "ai"
            prompt = command[4:].strip()
            response = ai_engine.generate_response(prompt)
        elif command.startswith("/code "):
            command_type = "code"
            code = command[6:].strip()
            response = ai_engine.analyze_code_with_ai(code)
        elif command.startswith("/solve "):
            command_type = "solve"
            problem = command[7:].strip()
            response = ai_engine.solve_with_ai(problem)
        elif command.startswith("/summarize "):
            command_type = "summarize"
            text = command[11:].strip()
            response = ai_engine.summarize_with_ai(text)
        elif command.startswith("/translate "):
            command_type = "translate"
            # Parse language and text
            parts = command[11:].strip().split(maxsplit=1)
            if len(parts) < 2:
                raise HTTPException(status_code=400, detail="Usage: /translate <language> <text>")
            target_lang, text = parts
            response = ai_engine.translate_with_ai(text, target_lang)
        elif command.startswith("/models"):
            command_type = "models"
            models = ai_engine.list_available_models()
            response = "Available Gemini Models:\n\n" + "\n".join([f"- {model}" for model in models])
        elif command.startswith("/help"):
            command_type = "help"
            response = """
NEO AI Assistant - Available Commands:

🤖 AI Commands:
  /ai <prompt>              - Generate AI response
  /code <code>              - Analyze code quality and suggest improvements
  /solve <problem>          - Solve a problem or answer a question
  /summarize <text>         - Summarize long text
  /translate <lang> <text>  - Translate text to target language
  /models                   - List available AI models
  /help                     - Show this help message

💡 Quick Commands (buttons):
  - Ask AI               → /ai 
  - Analyze Code         → /code 
  - Solve Problem        → /solve 
  - Summarize Text       → /summarize 

📝 Examples:
  /ai What is machine learning?
  /code def hello(): print("hi")
  /solve How do I sort a list in Python?
  /summarize [your long text here]
  /translate spanish Hello, how are you?
  /translate french Bonjour le monde

All commands powered by Google Gemini AI 🚀
"""
        else:
            # General command - use AI to respond
            command_type = "general"
            response = ai_engine.generate_response(command)
        
        return CommandResponse(
            response=response,
            command_type=command_type,
            data={}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error executing command: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error executing command: {str(e)}"
        )

@app.get("/api/models")
async def list_models():
    """List available AI models"""
    try:
        models = ai_engine.list_available_models()
        return {
            "models": models,
            "current": ai_engine.gemini.model_name if ai_engine.gemini else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting NEO AI Backend Server...")
    print("📡 Server will run on http://localhost:8000")
    print("🌐 Frontend should connect to this URL")
    print("✨ Press Ctrl+C to stop\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
