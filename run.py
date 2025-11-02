"""
Configuration and deployment setup for AI INCOME Bot + Web App
"""

import os
import threading
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_bot():
    """Run the Telegram bot"""
    print("🤖 Starting Telegram Bot...")
    from bot import main as bot_main
    bot_main()

def run_web_app():
    """Run the Flask web application"""
    print("🌐 Starting Web Application...")
    from app import app
    
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # For production deployment
    if os.environ.get('PRODUCTION'):
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        # For development
        app.run(host='0.0.0.0', port=port, debug=debug)

def main():
    """Main function to run both bot and web app"""
    deployment_mode = os.getenv('DEPLOYMENT_MODE', 'combined')
    
    if deployment_mode == 'bot_only':
        # Run only the bot
        run_bot()
        
    elif deployment_mode == 'web_only':
        # Run only the web app
        run_web_app()
        
    else:
        # Run both bot and web app (default)
        print("🚀 Starting AI INCOME Bot + Web App...")
        
        # Start bot in separate thread
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        
        # Give bot time to start
        time.sleep(2)
        
        # Run web app in main thread
        run_web_app()

if __name__ == '__main__':
    main()