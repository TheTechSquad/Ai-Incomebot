from telegram import Update
from telegram.ext import ContextTypes
from models.user import get_user
import os

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle withdrawal requests"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.message.reply_text("❌ User not found. Please use /start first.")
        return
    
    # Calculate USDT value from hashes
    usdt_amount = user.mined_hashes * 0.01
    min_withdrawal = 5.0  # Minimum $5 USDT withdrawal
    
    if usdt_amount < min_withdrawal:
        withdraw_message = f"""
💰 **Withdrawal Status**

💎 Current Balance: ${usdt_amount:.2f} USDT
📊 Total Hashes: {user.mined_hashes:.6f}

❌ **Minimum withdrawal: ${min_withdrawal} USDT**
⛏️ Keep mining to reach the minimum!

🔥 Need ${min_withdrawal - usdt_amount:.2f} more USDT
⚡ Increase GPU power with /buy for faster mining!
        """
    else:
        withdraw_message = f"""
💰 **Withdrawal Available**

💎 Available Balance: ${usdt_amount:.2f} USDT
📊 Total Hashes: {user.mined_hashes:.6f}

✅ **You can withdraw!**

🔧 **Withdrawal Methods:**
• USDT (TRC20)
• USDT (ERC20) 
• PayPal
• Bank Transfer

📞 **To Process Withdrawal:**
Contact admin @{os.getenv('ADMIN_USERNAME', 'admin_username')} with:
- Your Telegram ID: `{user_id}`
- Amount: ${usdt_amount:.2f} USDT
- Preferred method
- Wallet address/details

⚠️ Processing time: 24-48 hours
💼 Admin will verify and process your withdrawal.
        """
    
    await update.message.reply_text(
        withdraw_message,
        parse_mode='Markdown'
    )

async def withdrawal_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show withdrawal history"""
    await update.message.reply_text(
        """
📋 **Withdrawal History**

📊 No withdrawals yet.
💰 Start mining and earning to make your first withdrawal!

ℹ️ Withdrawal history will appear here once you make withdrawals.
        """,
        parse_mode='Markdown'
    )