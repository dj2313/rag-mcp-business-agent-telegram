import sys
import os
from dotenv import load_dotenv

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot_interface.bot import application, setup_bot

if __name__ == "__main__":
    load_dotenv()
    
    # Check for keys
    if not os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN") == "your_telegram_bot_token_here":
        print("CRITICAL: TELEGRAM_BOT_TOKEN not set in .env")
        sys.exit(1)
        
    if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "your_groq_api_key_here":
        print("WARNING: GROQ_API_KEY not set. LLM features will fail.")

    print("--- 🤖 RAG + MCP Business Agent Starting ---")
    
    # In Phase 1, we just run the bot. 
    # In later phases, we will also start the MCP server.
    try:
        if not application:
            print("Initializing bot setup...")
            application = setup_bot()
            
        if application:
            print("Bot is starting up... Press Ctrl+C to stop.")
            application.run_polling()
        else:
            print("Failed to initialize bot. Check your TOKEN in .env")
    except KeyboardInterrupt:
        print("\nAgent shutting down...")
    except Exception as e:
        print(f"Error: {e}")
