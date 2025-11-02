"""
NLP Conversation Module
Natural language processing and intelligent conversation management
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from collections import defaultdict
import json

from src.utils.logger import NEOLogger


@dataclass
class Message:
    """Conversation message"""
    id: str
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime
    intent: Optional[str] = None
    entities: Optional[Dict[str, Any]] = None
    confidence: float = 1.0


@dataclass
class ConversationContext:
    """Conversation context"""
    user_id: str
    session_id: str
    messages: List[Message]
    user_preferences: Dict[str, Any]
    metadata: Dict[str, Any]


class NLPConversation:
    """
    Advanced NLP and conversation management system
    """
    
    def __init__(self):
        self.logger = NEOLogger("NLPConversation")
        self.logger.info("NLP Conversation module initialized")
        
        self.conversations: Dict[str, ConversationContext] = {}
        self.intent_patterns = self._load_intent_patterns()
        self.entity_extractors = self._load_entity_extractors()
        
        self._message_counter = 0
    
    def _load_intent_patterns(self) -> Dict[str, List[str]]:
        """Load intent recognition patterns"""
        return {
            "greeting": [
                r"\b(hi|hello|hey|greetings)\b",
                r"\bgood (morning|afternoon|evening)\b"
            ],
            "farewell": [
                r"\b(bye|goodbye|see you|farewell)\b",
                r"\btalk to you later\b"
            ],
            "question": [
                r"^(what|when|where|who|why|how)\b",
                r"\?$"
            ],
            "command": [
                r"^(do|make|create|run|execute|start|stop)\b",
                r"\b(please|could you|can you)\s+(do|make|create)"
            ],
            "help": [
                r"\b(help|assist|support)\b",
                r"how (do|can) (i|you)"
            ],
            "gratitude": [
                r"\b(thank|thanks|appreciate)\b"
            ],
            "system_control": [
                r"\b(shutdown|restart|reboot|system)\b"
            ],
            "code_request": [
                r"\b(code|program|script|function)\b",
                r"\b(write|create|generate).*(code|program)"
            ],
            "research": [
                r"\b(research|find|search|look up)\b",
                r"(what|tell me) (is|are|about)"
            ],
            "security": [
                r"\b(security|vulnerability|hack|penetration)\b",
                r"\b(password|encryption|secure)\b"
            ]
        }
    
    def _load_entity_extractors(self) -> Dict[str, str]:
        """Load entity extraction patterns"""
        return {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "url": r'https?://[^\s]+',
            "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            "number": r'\b\d+\.?\d*\b',
            "date": r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            "time": r'\b\d{1,2}:\d{2}(?::\d{2})?\s*(?:AM|PM|am|pm)?\b'
        }
    
    def create_conversation(self, user_id: str) -> str:
        """
        Create a new conversation session
        
        Args:
            user_id: User identifier
        
        Returns:
            Session ID
        """
        session_id = f"session_{user_id}_{int(datetime.now().timestamp())}"
        
        context = ConversationContext(
            user_id=user_id,
            session_id=session_id,
            messages=[],
            user_preferences={},
            metadata={"created_at": datetime.now().isoformat()}
        )
        
        self.conversations[session_id] = context
        
        self.logger.info(f"Created conversation session: {session_id} for user: {user_id}")
        
        return session_id
    
    def process_message(
        self,
        session_id: str,
        message: str,
        role: str = "user"
    ) -> Dict[str, Any]:
        """
        Process incoming message
        
        Args:
            session_id: Conversation session ID
            message: Message content
            role: Message role (user/assistant)
        
        Returns:
            Processing result with intent and entities
        """
        if session_id not in self.conversations:
            self.logger.error(f"Conversation not found: {session_id}")
            return {"error": "Conversation not found"}
        
        context = self.conversations[session_id]
        
        # Generate message ID
        self._message_counter += 1
        message_id = f"msg_{self._message_counter}"
        
        # Analyze message
        intent, confidence = self.detect_intent(message)
        entities = self.extract_entities(message)
        sentiment = self.analyze_sentiment(message)
        
        # Create message object
        msg = Message(
            id=message_id,
            role=role,
            content=message,
            timestamp=datetime.now(),
            intent=intent,
            entities=entities,
            confidence=confidence
        )
        
        # Add to conversation
        context.messages.append(msg)
        
        self.logger.info(f"Processed message: {message_id} (intent: {intent}, confidence: {confidence:.2f})")
        
        return {
            "message_id": message_id,
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "sentiment": sentiment,
            "context": self._get_conversation_summary(session_id)
        }
    
    def detect_intent(self, text: str) -> Tuple[str, float]:
        """
        Detect intent from text
        
        Args:
            text: Input text
        
        Returns:
            Tuple of (intent, confidence)
        """
        text_lower = text.lower()
        intent_scores = defaultdict(float)
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    intent_scores[intent] += 1.0
        
        if not intent_scores:
            return "unknown", 0.5
        
        # Get intent with highest score
        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        
        # Normalize confidence
        total_score = sum(intent_scores.values())
        confidence = best_intent[1] / total_score if total_score > 0 else 0.5
        
        return best_intent[0], min(confidence, 1.0)
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text
        
        Args:
            text: Input text
        
        Returns:
            Dictionary of entity types and values
        """
        entities = {}
        
        for entity_type, pattern in self.entity_extractors.items():
            matches = re.findall(pattern, text)
            if matches:
                entities[entity_type] = matches
        
        return entities
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text
        
        Args:
            text: Input text
        
        Returns:
            Sentiment analysis result
        """
        # Simple sentiment analysis based on keywords
        positive_words = ['good', 'great', 'excellent', 'awesome', 'wonderful', 'love', 'like', 'best', 'happy', 'perfect']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'poor', 'sad', 'angry', 'disappointed']
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        # Calculate sentiment score (-1 to 1)
        total = positive_count + negative_count
        if total == 0:
            sentiment_score = 0.0
            sentiment = "neutral"
        else:
            sentiment_score = (positive_count - negative_count) / total
            
            if sentiment_score > 0.3:
                sentiment = "positive"
            elif sentiment_score < -0.3:
                sentiment = "negative"
            else:
                sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "score": sentiment_score,
            "positive_indicators": positive_count,
            "negative_indicators": negative_count
        }
    
    def generate_response(
        self,
        session_id: str,
        user_message: str
    ) -> str:
        """
        Generate response to user message
        
        Args:
            session_id: Conversation session ID
            user_message: User's message
        
        Returns:
            Generated response
        """
        # Process user message
        analysis = self.process_message(session_id, user_message, role="user")
        
        intent = analysis.get("intent", "unknown")
        entities = analysis.get("entities", {})
        
        # Generate appropriate response based on intent
        response = self._generate_intent_response(intent, user_message, entities)
        
        # Add response to conversation
        self.process_message(session_id, response, role="assistant")
        
        return response
    
    def _generate_intent_response(
        self,
        intent: str,
        message: str,
        entities: Dict[str, Any]
    ) -> str:
        """Generate response based on detected intent"""
        responses = {
            "greeting": "Hello! I'm NEO, your Neural Executive Operator. How can I assist you today?",
            "farewell": "Goodbye! Feel free to reach out anytime you need assistance.",
            "help": "I can help you with various tasks including system control, coding assistance, research, cybersecurity, and much more. What would you like help with?",
            "gratitude": "You're welcome! I'm here to help anytime.",
            "system_control": "I can help with system operations. Please specify what you'd like me to do (e.g., get system info, manage processes).",
            "code_request": "I'd be happy to help with coding. Please describe what you need - I can write code, debug, analyze, or optimize.",
            "research": "I can research any topic for you. What would you like me to investigate?",
            "security": "I can assist with cybersecurity tasks including vulnerability scanning, password analysis, and security assessments. What specific security task do you need?",
            "question": f"That's an interesting question. Let me help you with that: {message}",
            "command": "I understand you want me to perform a task. I'll help you with that.",
            "unknown": "I understand. Could you please provide more details about what you'd like me to do?"
        }
        
        return responses.get(intent, responses["unknown"])
    
    def get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get conversation history
        
        Args:
            session_id: Conversation session ID
            limit: Maximum number of messages
        
        Returns:
            List of messages
        """
        if session_id not in self.conversations:
            return []
        
        context = self.conversations[session_id]
        messages = context.messages[-limit:]
        
        return [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
                "intent": msg.intent,
                "confidence": msg.confidence
            }
            for msg in messages
        ]
    
    def _get_conversation_summary(self, session_id: str) -> Dict[str, Any]:
        """Get conversation context summary"""
        if session_id not in self.conversations:
            return {}
        
        context = self.conversations[session_id]
        
        return {
            "session_id": session_id,
            "user_id": context.user_id,
            "message_count": len(context.messages),
            "created_at": context.metadata.get("created_at"),
            "last_intent": context.messages[-1].intent if context.messages else None
        }
    
    def summarize_conversation(self, session_id: str) -> str:
        """
        Generate conversation summary
        
        Args:
            session_id: Conversation session ID
        
        Returns:
            Summary text
        """
        if session_id not in self.conversations:
            return "Conversation not found"
        
        context = self.conversations[session_id]
        
        if not context.messages:
            return "No messages in conversation"
        
        # Count intents
        intent_counts = defaultdict(int)
        for msg in context.messages:
            if msg.intent:
                intent_counts[msg.intent] += 1
        
        # Build summary
        summary_parts = [
            f"Conversation Summary for Session: {session_id}",
            f"Total Messages: {len(context.messages)}",
            f"Duration: {context.messages[0].timestamp.isoformat()} to {context.messages[-1].timestamp.isoformat()}",
            "",
            "Main Topics:"
        ]
        
        for intent, count in sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            summary_parts.append(f"  - {intent}: {count} messages")
        
        return "\n".join(summary_parts)
    
    def clear_conversation(self, session_id: str) -> bool:
        """
        Clear conversation history
        
        Args:
            session_id: Conversation session ID
        
        Returns:
            Success status
        """
        if session_id in self.conversations:
            del self.conversations[session_id]
            self.logger.info(f"Cleared conversation: {session_id}")
            return True
        
        return False
    
    def export_conversation(self, session_id: str, format: str = "json") -> str:
        """
        Export conversation
        
        Args:
            session_id: Conversation session ID
            format: Export format (json, text)
        
        Returns:
            Exported conversation
        """
        history = self.get_conversation_history(session_id, limit=1000)
        
        if format == "json":
            return json.dumps(history, indent=2)
        
        elif format == "text":
            lines = []
            for msg in history:
                lines.append(f"[{msg['timestamp']}] {msg['role'].upper()}: {msg['content']}")
            return "\n".join(lines)
        
        return "Unsupported format"


if __name__ == "__main__":
    # Test NLP conversation
    nlp = NLPConversation()
    
    # Create session
    session = nlp.create_conversation("user_123")
    
    # Test messages
    test_messages = [
        "Hello, how are you?",
        "Can you help me write some Python code?",
        "What is artificial intelligence?",
        "Thanks for your help!"
    ]
    
    for msg in test_messages:
        response = nlp.generate_response(session, msg)
        print(f"User: {msg}")
        print(f"NEO: {response}\n")
    
    # Get summary
    summary = nlp.summarize_conversation(session)
    print(summary)
