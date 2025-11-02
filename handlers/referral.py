from telegram import Update
from telegram.ext import ContextTypes
from models.user import get_user
import os

async def referral_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate and display referral link"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.message.reply_text("❌ User not found. Please use /start first.")
        return
    
    # Get bot username (you'll need to set this in environment or config)
    bot_username = os.getenv('BOT_USERNAME', 'AI_INCOME_Bot')
    referral_url = f"https://t.me/{bot_username}?start={user_id}"
    
    referral_message = f"""
🔗 **Your Referral Program**

💎 Invite friends and earn rewards!
⚡ Each successful referral gives you +500 GPU Power
🔥 Your friends get extra starting power too!

📋 **Your Referral Info:**
🆔 Your Code: `{user.referral_code}`
🔗 Your Link: {referral_url}

💰 **How it Works:**
1️⃣ Share your link with friends
2️⃣ They join using your link
3️⃣ You both get bonus GPU power!
4️⃣ Start earning more hashes together!

📤 **Share this link:**
{referral_url}
    """
    
    await update.message.reply_text(
        referral_message,
        parse_mode='Markdown'
    )

async def referral_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show referral statistics"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.message.reply_text("❌ User not found. Please use /start first.")
        return
    
    # In a real implementation, you'd query the database for referral count
    # For now, we'll show a placeholder
    stats_message = f"""
📊 **Referral Statistics**

👥 Total Referrals: Coming Soon
💰 Bonus Earned: Coming Soon
🔥 Referral Power: Coming Soon

🔗 Your Code: `{user.referral_code}`
💡 Keep sharing to earn more rewards!
    """
    
    await update.message.reply_text(
        stats_message,
        parse_mode='Markdown'
    )