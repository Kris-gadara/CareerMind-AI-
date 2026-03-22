"""
CareerMind AI - Chatbot Module
===============================
Interactive career counseling chatbot powered by Ollama (local LLM)
with fallback to the Phi analyzer when Ollama is unavailable.
"""

import os
import json
import requests
from typing import Generator, Optional
from dataclasses import dataclass, field

# Default Ollama configuration
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "mistral")


@dataclass
class Message:
    """Represents a chat message."""
    role: str  # "user", "assistant", or "system"
    content: str


class CareerChatbot:
    """
    Interactive career counseling chatbot.

    Uses Ollama API for chat completions when available,
    falls back to PhiResumeAnalyzer for single-turn responses.
    """

    # System prompt that defines the chatbot's persona
    SYSTEM_PROMPT = """You are CareerMind AI, an expert career counselor with deep knowledge of:
- The tech industry and job market trends
- Resume writing and optimization
- Salary negotiation strategies
- Skill development and learning paths
- Interview preparation
- Career transitions and growth

Guidelines:
- Be encouraging but honest about skill gaps
- Give practical, actionable advice
- Keep responses concise (under 200 words) unless asked for detail
- Always end with one actionable next step
- When you don't know something, say so
- Personalize advice based on the user's resume when available"""

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        fallback_analyzer=None,
        base_url: str = OLLAMA_BASE_URL
    ):
        """
        Initialize the chatbot.

        Args:
            model: Ollama model name (e.g., "mistral", "llama2")
            fallback_analyzer: PhiResumeAnalyzer instance for fallback
            base_url: Ollama API base URL
        """
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.fallback = fallback_analyzer
        self.conversation_history: list[Message] = []
        self.resume_context: dict = {}
        self._ollama_available: Optional[bool] = None

    def is_ollama_running(self) -> bool:
        """
        Check if Ollama server is running and accessible.

        Returns:
            True if Ollama is available, False otherwise
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=2
            )
            self._ollama_available = response.status_code == 200
            return self._ollama_available
        except (requests.RequestException, ConnectionError):
            self._ollama_available = False
            return False

    def get_available_models(self) -> list[str]:
        """
        Get list of models installed in Ollama.

        Returns:
            List of model names, or empty list if Ollama unavailable
        """
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                return [m["name"] for m in data.get("models", [])]
        except (requests.RequestException, json.JSONDecodeError):
            pass
        return []

    def set_model(self, model: str):
        """
        Change the Ollama model being used.

        Args:
            model: Name of the model (e.g., "mistral", "llama2:7b")
        """
        self.model = model

    def set_resume_context(self, resume_data: dict):
        """
        Set resume context for personalized responses.

        Args:
            resume_data: Dictionary from parser.parse_resume()
        """
        self.resume_context = resume_data

        # Add context to system prompt if resume is available
        if resume_data and resume_data.get("parse_success"):
            skills = resume_data.get("skills", [])[:20]
            experience = resume_data.get("experience_years", 0)
            name = resume_data.get("name", "")

            context_addition = f"""

Current user context:
- Name: {name or 'Not provided'}
- Experience: {experience} years
- Key skills: {', '.join(skills) if skills else 'Not extracted'}

Personalize your advice based on this background."""

            # Store enhanced system prompt
            self._enhanced_system_prompt = self.SYSTEM_PROMPT + context_addition
        else:
            self._enhanced_system_prompt = self.SYSTEM_PROMPT

    def _get_system_prompt(self) -> str:
        """Get the current system prompt (with or without resume context)."""
        return getattr(self, '_enhanced_system_prompt', self.SYSTEM_PROMPT)

    def reset_conversation(self):
        """Clear chat history but keep resume context."""
        self.conversation_history = []

    def chat(self, user_message: str) -> str:
        """
        Send a message and get a response.

        Args:
            user_message: The user's message

        Returns:
            Assistant's response string
        """
        # Add user message to history
        self.conversation_history.append(Message(role="user", content=user_message))

        # Try Ollama first
        if self._ollama_available is None:
            self.is_ollama_running()

        if self._ollama_available:
            response = self._ollama_chat(user_message)
        else:
            response = self._fallback_chat(user_message)

        # Add assistant response to history
        self.conversation_history.append(Message(role="assistant", content=response))

        return response

    def _ollama_chat(self, user_message: str) -> str:
        """
        Get response from Ollama API.

        Args:
            user_message: The user's message

        Returns:
            Model's response
        """
        # Build messages for Ollama
        messages = [
            {"role": "system", "content": self._get_system_prompt()}
        ]

        # Add conversation history (last 10 exchanges to stay within context)
        history_limit = 20  # 10 exchanges = 20 messages
        recent_history = self.conversation_history[-history_limit:]

        for msg in recent_history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                    }
                },
                timeout=60
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("message", {}).get("content", "I couldn't generate a response.")
            else:
                return f"Ollama error: {response.status_code}. Trying fallback..."

        except requests.RequestException as e:
            self._ollama_available = False
            return self._fallback_chat(user_message)

    def _fallback_chat(self, user_message: str) -> str:
        """
        Use Phi analyzer as fallback when Ollama is unavailable.

        Args:
            user_message: The user's message

        Returns:
            Generated response
        """
        if self.fallback and self.fallback.is_loaded():
            return self.fallback.answer_career_question(
                user_message,
                self.resume_context
            )

        # Ultimate fallback: rule-based responses
        return self._rule_based_response(user_message)

    def _rule_based_response(self, user_message: str) -> str:
        """
        Generate a basic response when no AI is available.

        Args:
            user_message: The user's message

        Returns:
            Rule-based response
        """
        message_lower = user_message.lower()

        # Greeting
        if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
            return ("Hello! I'm CareerMind AI, your career counselor. "
                    "I can help with resume tips, career planning, salary advice, and more. "
                    "What would you like to discuss?")

        # Resume help
        if "resume" in message_lower:
            return ("Here are key resume tips:\n\n"
                    "1. **Quantify achievements** - Use numbers (e.g., 'Improved performance by 40%')\n"
                    "2. **Use keywords** - Match terms from job descriptions\n"
                    "3. **Keep it concise** - 1-2 pages max\n"
                    "4. **Lead with impact** - Most impressive points first\n\n"
                    "Would you like me to analyze your resume? Upload it in the Analysis tab.")

        # Salary
        if "salary" in message_lower or "pay" in message_lower or "compensation" in message_lower:
            return ("For salary negotiations:\n\n"
                    "1. **Research market rates** - Use Levels.fyi, Glassdoor, or LinkedIn\n"
                    "2. **Know your value** - List your unique skills and achievements\n"
                    "3. **Negotiate total comp** - Consider equity, bonuses, benefits\n"
                    "4. **Practice** - Rehearse your pitch beforehand\n\n"
                    "Check the Salary tab for a personalized estimate based on your profile.")

        # Interview
        if "interview" in message_lower:
            return ("Interview preparation tips:\n\n"
                    "1. **Research the company** - Know their products, culture, and recent news\n"
                    "2. **STAR method** - Structure behavioral answers with Situation, Task, Action, Result\n"
                    "3. **Practice coding** - LeetCode, HackerRank for technical rounds\n"
                    "4. **Prepare questions** - Show genuine interest in the role\n\n"
                    "What type of interview are you preparing for?")

        # Skills
        if "skill" in message_lower or "learn" in message_lower:
            return ("For skill development:\n\n"
                    "1. **Focus on fundamentals** - Strong foundations matter more than tool count\n"
                    "2. **Build projects** - Apply learning to real problems\n"
                    "3. **Stay current** - Follow industry trends, but don't chase every new thing\n"
                    "4. **Depth over breadth** - Better to master 5 skills than know 20 superficially\n\n"
                    "Check the Skill Gap tab to see which skills would benefit you most.")

        # Career change
        if "career" in message_lower and ("change" in message_lower or "switch" in message_lower):
            return ("For career transitions:\n\n"
                    "1. **Identify transferable skills** - Many skills apply across roles\n"
                    "2. **Bridge the gap** - Focus on 2-3 key missing skills\n"
                    "3. **Network** - Connect with people in your target field\n"
                    "4. **Start small** - Side projects or freelance work can build credibility\n\n"
                    "Check the Roadmap tab for a personalized transition plan.")

        # Default
        return ("I'm here to help with your career! I can assist with:\n\n"
                "- Resume optimization\n"
                "- Skill gap analysis\n"
                "- Salary expectations\n"
                "- Career path planning\n"
                "- Interview preparation\n\n"
                "What would you like to explore?")

    def stream_chat(self, user_message: str) -> Generator[str, None, None]:
        """
        Stream response token by token for real-time display.

        Args:
            user_message: The user's message

        Yields:
            Response chunks as they're generated
        """
        # Add user message to history
        self.conversation_history.append(Message(role="user", content=user_message))

        # Check Ollama availability
        if self._ollama_available is None:
            self.is_ollama_running()

        if not self._ollama_available:
            # Can't stream fallback, return full response
            response = self._fallback_chat(user_message)
            self.conversation_history.append(Message(role="assistant", content=response))
            yield response
            return

        # Build messages
        messages = [
            {"role": "system", "content": self._get_system_prompt()}
        ]

        history_limit = 20
        recent_history = self.conversation_history[-history_limit:]

        for msg in recent_history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": True,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                    }
                },
                stream=True,
                timeout=60
            )

            if response.status_code == 200:
                full_response = ""

                for line in response.iter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            chunk = data.get("message", {}).get("content", "")
                            if chunk:
                                full_response += chunk
                                yield chunk

                            # Check if stream is done
                            if data.get("done"):
                                break

                        except json.JSONDecodeError:
                            continue

                # Add complete response to history
                self.conversation_history.append(
                    Message(role="assistant", content=full_response)
                )
            else:
                error_msg = f"Error: {response.status_code}"
                self.conversation_history.append(
                    Message(role="assistant", content=error_msg)
                )
                yield error_msg

        except requests.RequestException as e:
            self._ollama_available = False
            fallback = self._fallback_chat(user_message)
            self.conversation_history.append(
                Message(role="assistant", content=fallback)
            )
            yield fallback

    def get_conversation_stats(self) -> dict:
        """
        Get statistics about the current conversation.

        Returns:
            Dictionary with message counts and other stats
        """
        user_msgs = sum(1 for m in self.conversation_history if m.role == "user")
        asst_msgs = sum(1 for m in self.conversation_history if m.role == "assistant")

        return {
            "total_messages": len(self.conversation_history),
            "user_messages": user_msgs,
            "assistant_messages": asst_msgs,
            "has_resume_context": bool(self.resume_context),
            "using_ollama": self._ollama_available or False,
            "model": self.model if self._ollama_available else "fallback"
        }

    def get_status(self) -> str:
        """
        Get a human-readable status of the chatbot.

        Returns:
            Status string
        """
        if self._ollama_available is None:
            self.is_ollama_running()

        if self._ollama_available:
            return f"Connected to Ollama ({self.model})"
        elif self.fallback and self.fallback.is_loaded():
            return f"Using Phi fallback ({self.fallback.model_name})"
        else:
            return "Using rule-based responses (limited)"


# ============================================================================
# Singleton instance
# ============================================================================

_chatbot_instance = None


def get_chatbot(fallback_analyzer=None) -> CareerChatbot:
    """Get or create the singleton CareerChatbot instance."""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = CareerChatbot(fallback_analyzer=fallback_analyzer)
    return _chatbot_instance


# ============================================================================
# TEST / DEBUG
# ============================================================================

if __name__ == "__main__":
    print("CareerChatbot Test")
    print("=" * 50)

    chatbot = CareerChatbot()

    # Check Ollama
    print(f"Checking Ollama at {chatbot.base_url}...")
    if chatbot.is_ollama_running():
        print("Ollama is running!")
        models = chatbot.get_available_models()
        print(f"Available models: {models}")
    else:
        print("Ollama not available. Using fallback responses.")

    print(f"\nStatus: {chatbot.get_status()}")

    # Set some resume context
    chatbot.set_resume_context({
        "name": "Test User",
        "skills": ["python", "sql", "pandas"],
        "experience_years": 2,
        "parse_success": True
    })

    # Test conversation
    print("\n--- Test Conversation ---")

    test_messages = [
        "Hello!",
        "How can I improve my resume?",
        "What skills should I learn for a data science role?"
    ]

    for msg in test_messages:
        print(f"\nYou: {msg}")
        response = chatbot.chat(msg)
        print(f"CareerMind: {response[:500]}...")

    print(f"\n\nConversation stats: {chatbot.get_conversation_stats()}")
