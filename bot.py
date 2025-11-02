"""
AI INCOME Telegram Bot
A crypto mining simulation bot with referral system and GPU power trading.
"""

import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Import handlers
from handlers.start import start, stats
from handlers.miner import miner, auto_mine
from handlers.referral import referral_link, referral_stats
from handlers.withdraw import withdraw, withdrawal_history
from handlers.shop import shop, buy_power, confirm_purchase
from handlers.callbacks import handle_callback_query

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def webapp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show web app button"""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
    
    # Your web app URL (replace with your actual domain)
    web_app_url = "https://your-domain.com/dashboard"  # Replace with your actual URL
    
    keyboard = [
        [InlineKeyboardButton(
            text="🚀 Open AI INCOME Web App", 
            web_app=WebAppInfo(url=web_app_url)
        )],
        [InlineKeyboardButton(
            text="📱 How to Use Web App", 
            callback_data="webapp_help"
        )]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    webapp_text = """
🌐 **AI INCOME Web Interface**

Experience the full power of AI INCOME with our web interface!

✨ **Features:**
• 🖥️ Beautiful dashboard with real-time stats
• ⛏️ Enhanced mining interface with animations
• 🏪 Interactive GPU power shop
• 📊 Detailed analytics and progress tracking
• 📱 Mobile-optimized responsive design

🎯 **Exclusive Web Features:**
• Mining progress animations
• Advanced statistics visualization  
• Purchase calculator and comparisons
• Achievement system with progress bars
• Enhanced referral sharing tools

🚀 **Click the button below to launch the web app!**
    """
    
    await update.message.reply_text(
        webapp_text,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help message with all available commands"""
    help_text = f"""
🤖 **AI INCOME Bot Commands**

🌐 **Web Interface:**
/webapp - Launch web interface (recommended!)

🏠 **Main Commands:**
/start - Welcome & register
/stats - View your statistics  
/help - Show this help message

⛏️ **Mining Commands:**
/miner - Start mining hashes
/automine - Auto-mining info (premium)

💰 **Economy Commands:**
/shop - View GPU power shop
/buy [amount] - Purchase GPU power
/withdraw - Check withdrawal options

👥 **Social Commands:**  
/referral - Get your referral link
/refstats - View referral statistics

📊 **Additional Commands:**
/history - Withdrawal history
/leaderboard - Top miners (coming soon)

💡 **Getting Started:**
1️⃣ Use /webapp for the best experience
2️⃣ Or use /miner to start earning hashes
3️⃣ Check /stats to monitor progress
4️⃣ Use /shop to boost your GPU power
5️⃣ Share /referral link with friends

🔥 **Pro Tips:**
• Use the web app for enhanced features!
• Mine regularly for consistent earnings
• Invite friends for bonus GPU power  
• Upgrade power for higher hash rates
• Join our community for updates!

💬 **Support:** Contact @{os.getenv('ADMIN_USERNAME', 'admin_username')}
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show leaderboard (placeholder)"""
    leaderboard_text = """
🏆 **AI INCOME Leaderboard**

👑 **Top Miners:** Coming Soon
💎 **Top Referrers:** Coming Soon  
⚡ **Highest GPU Power:** Coming Soon

📊 Compete with other miners and climb the ranks!
🔥 Check back soon for live leaderboard updates.

💡 Keep mining and referring to secure your spot!
    """
    await update.message.reply_text(leaderboard_text, parse_mode='Markdown')

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a message to notify about the error."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "❌ An error occurred while processing your request. Please try again later."
        )

def main():
    """Start the bot"""
    # Get bot token from environment variable
    bot_token = os.getenv('BOT_TOKEN')
    
    if not bot_token:
        logger.error("BOT_TOKEN environment variable not found!")
        print("❌ Error: Please set your BOT_TOKEN in the .env file")
        print("📝 Create a .env file with: BOT_TOKEN=your_bot_token_here")
        return
    
    # Create the Application
    application = Application.builder().token(bot_token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("webapp", webapp_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats))
    
    # Mining handlers
    application.add_handler(CommandHandler("miner", miner))
    application.add_handler(CommandHandler("mine", miner))  # Alias for /miner
    application.add_handler(CommandHandler("automine", auto_mine))
    
    # Shop handlers  
    application.add_handler(CommandHandler("shop", shop))
    application.add_handler(CommandHandler("buy", buy_power))
    application.add_handler(CommandHandler("confirm", confirm_purchase))
    
    # Withdrawal handlers
    application.add_handler(CommandHandler("withdraw", withdraw))
    application.add_handler(CommandHandler("history", withdrawal_history))
    
    # Referral handlers
    application.add_handler(CommandHandler("referral", referral_link))
    application.add_handler(CommandHandler("refstats", referral_stats))
    
    # Additional handlers
    application.add_handler(CommandHandler("leaderboard", leaderboard))
    
    # Callback query handler for inline keyboards
    application.add_handler(CallbackQueryHandler(handle_callback_query))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("🤖 AI INCOME Bot starting...")
    print("🚀 AI INCOME Bot is starting...")
    print("💡 Bot will run until you press Ctrl+C")
    
    try:
        # Run the bot until the user presses Ctrl-C
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
        print("\n🛑 Bot stopped successfully!")
    except Exception as e:
        logger.error(f"❌ Bot error: {e}")
        print(f"❌ Bot error: {e}")

if __name__ == '__main__':
    main()