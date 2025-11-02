from telegram import Update
from telegram.ext import ContextTypes
from models.user import create_or_update_user, get_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
    
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name
    
    # Check if there's a referral code in the command
    referral_code = None
    if context.args and len(context.args) > 0:
        referral_code = context.args[0]
    
    # Create or get existing user
    user = create_or_update_user(user_id, referral_code)
    
    # Your web app URL (replace with your actual domain)
    web_app_url = "https://your-domain.com/dashboard"  # Replace with your actual URL
    
    keyboard = [
        [InlineKeyboardButton(
            text="🚀 Launch Web Interface", 
            web_app=WebAppInfo(url=web_app_url)
        )],
        [
            InlineKeyboardButton(text="⛏️ Mine Here", callback_data="mine_telegram"),
            InlineKeyboardButton(text="📊 My Stats", callback_data="show_stats")
        ],
        [
            InlineKeyboardButton(text="🏪 GPU Shop", callback_data="show_shop"),
            InlineKeyboardButton(text="👥 Referrals", callback_data="show_referral")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = f"""
🤖 **Welcome to AI INCOME Bot, {username}!** 

💎 Start your crypto mining journey now!
⚡ Your starting GPU power: {user.gpu_power:,}
🔥 Begin mining and earn hashes that convert to USDT!

🌟 **Choose Your Experience:**
• 🖥️ **Web Interface** - Full-featured dashboard (recommended)
• 📱 **Telegram Bot** - Quick commands and notifications

📈 **Current Status:**
• 💪 GPU Power: {user.gpu_power:,}
• 🔥 Total Hashes: {user.mined_hashes:.6f}
• 💰 USDT Value: ${user.mined_hashes * 0.01:.2f}

🎯 **Quick Commands:**
/webapp - Launch web interface
/miner - Start mining hashes
/stats - View detailed statistics
/help - Show all commands

� **Tip:** Use the web interface for the best experience with animations, detailed stats, and enhanced features!
    """
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.message.reply_text("❌ User not found. Please use /start first.")
        return
    
    usdt_value = user.mined_hashes * 0.01
    
    stats_message = f"""
📊 **Your AI INCOME Stats:**

⚡ GPU Power: {user.gpu_power:,}
🔥 Total Hashes Mined: {user.mined_hashes:.6f}
💰 USDT Value: ${usdt_value:.2f}
🔗 Your Referral Code: {user.referral_code}
📅 Member since: {user.created_at.strftime('%Y-%m-%d')}

💡 Invite friends to earn bonus GPU power!
Use /referral to get your invite link.
    """
    
    await update.message.reply_text(
        stats_message,
        parse_mode='Markdown'
    )