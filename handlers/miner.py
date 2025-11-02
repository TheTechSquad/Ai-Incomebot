from telegram import Update
from telegram.ext import ContextTypes
from models.user import get_user, update_user_mining
from utils.mining import calculate_mining
from datetime import datetime, timedelta
import random

async def miner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /miner command for mining hashes"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.message.reply_text("❌ User not found. Please use /start first.")
        return
    
    # Check if user needs to wait before mining again (optional cooldown)
    current_time = datetime.utcnow()
    if user.last_mine_time:
        time_diff = current_time - user.last_mine_time
        cooldown_minutes = 5  # 5 minute cooldown between mining sessions
        if time_diff < timedelta(minutes=cooldown_minutes):
            remaining_time = cooldown_minutes - int(time_diff.total_seconds() / 60)
            await update.message.reply_text(
                f"⏰ Mining cooldown active! Wait {remaining_time} more minute(s) before mining again."
            )
            return
    
    # Calculate mining based on GPU power
    hashes_earned = calculate_mining(user.gpu_power)
    
    # Add some randomness to make it more engaging
    random_multiplier = random.uniform(0.8, 1.2)
    hashes_earned *= random_multiplier
    
    # Update user's mining data
    updated_user = update_user_mining(user_id, hashes_earned)
    
    if updated_user:
        usdt_value = hashes_earned * 0.01
        total_usdt = updated_user.mined_hashes * 0.01
        
        mining_message = f"""
⛏️ **Mining Successful!**

🔥 Hashes Mined: {hashes_earned:.6f}
💰 Value: ${usdt_value:.4f} USDT
⚡ GPU Power Used: {user.gpu_power:,}

📊 **Your Totals:**
🔥 Total Hashes: {updated_user.mined_hashes:.6f}
💰 Total USDT: ${total_usdt:.2f}

🚀 Use /buy to increase your GPU power!
💎 Use /referral to invite friends and earn bonuses!
        """
        
        await update.message.reply_text(
            mining_message,
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text("❌ Mining failed. Please try again.")

async def auto_mine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start auto-mining feature (premium feature simulation)"""
    await update.message.reply_text(
        """
🤖 **Auto-Mining Feature**

⚡ Auto-mining allows continuous hash generation!
💎 This premium feature mines every 10 minutes automatically.
🔥 Upgrade your account to unlock auto-mining.

💰 Contact admin to upgrade your account!
        """,
        parse_mode='Markdown'
    )