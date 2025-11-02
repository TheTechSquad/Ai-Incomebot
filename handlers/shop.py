from telegram import Update
from telegram.ext import ContextTypes
from models.user import get_user, update_user_gpu_power
import os

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display the GPU power shop"""
    shop_message = """
🏪 **AI INCOME GPU SHOP**

💎 **Power Packages Available:**

🔥 **Starter Pack** - $3
⚡ 30,000 Base Power + 7,500 Bonus
💰 Total: 37,500 GPU Power
📈 Command: `/buy 3`

🚀 **Pro Pack** - $5  
⚡ 50,000 Base Power + 12,500 Bonus
💰 Total: 62,500 GPU Power
📈 Command: `/buy 5`

💎 **Elite Pack** - $10
⚡ 100,000 Base Power + 25,000 Bonus  
💰 Total: 125,000 GPU Power
📈 Command: `/buy 10`

🔥 **Mega Pack** - $20
⚡ 200,000 Base Power + 50,000 Bonus
💰 Total: 250,000 GPU Power
📈 Command: `/buy 20`

💡 **Formula:** Base Power = Amount × 10,000 + 25% Bonus

📞 **How to Buy:**
1️⃣ Choose your package
2️⃣ Use the `/buy [amount]` command
3️⃣ Contact admin for payment details
4️⃣ Get instant GPU power boost!

⚠️ Payment methods: PayPal, Crypto, Bank Transfer
    """
    
    await update.message.reply_text(
        shop_message,
        parse_mode='Markdown'
    )

async def buy_power(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle GPU power purchase"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.message.reply_text("❌ User not found. Please use /start first.")
        return
    
    # Check if amount is provided
    if not context.args or len(context.args) == 0:
        await update.message.reply_text(
            "💡 Usage: `/buy [amount]`\n"
            "Example: `/buy 5` for $5 package\n"
            "Use /shop to see available packages.",
            parse_mode='Markdown'
        )
        return
    
    try:
        amount = float(context.args[0])
        if amount <= 0:
            raise ValueError("Amount must be positive")
    except ValueError:
        await update.message.reply_text("❌ Please enter a valid positive number.")
        return
    
    # Calculate GPU power based on the formula from instructions
    base_power = amount * 10000
    bonus_power = base_power * 0.25
    total_power = int(base_power + bonus_power)
    
    purchase_message = f"""
🛒 **Purchase Request Submitted**

💰 Package: ${amount} USD
⚡ Base Power: {int(base_power):,}
🎁 Bonus Power: {int(bonus_power):,}
🔥 **Total GPU Power: {total_power:,}**

📋 **Next Steps:**
1️⃣ Contact admin: @{os.getenv('ADMIN_USERNAME', 'admin_username')}
2️⃣ Send your Telegram ID: `{user_id}`
3️⃣ Mention package: ${amount} USD
4️⃣ Complete payment
5️⃣ Get instant power boost!

💳 **Payment Methods:**
• PayPal • Crypto • Bank Transfer

⏰ Processing time: Usually instant after payment confirmation.

📞 **Admin Contact:** @{os.getenv('ADMIN_USERNAME', 'admin_username')}
    """
    
    await update.message.reply_text(
        purchase_message,
        parse_mode='Markdown'
    )

async def confirm_purchase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to confirm purchase (for demo purposes)"""
    # This would normally be restricted to admin users
    user_id = update.effective_user.id
    
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Usage: /confirm [user_id] [amount]")
        return
    
    try:
        target_user_id = context.args[0] 
        amount = float(context.args[1])
        
        # Calculate power
        base_power = amount * 10000
        bonus_power = base_power * 0.25
        total_power = int(base_power + bonus_power)
        
        # Update user's GPU power
        updated_user = update_user_gpu_power(target_user_id, total_power)
        
        if updated_user:
            await update.message.reply_text(
                f"✅ Purchase confirmed!\n"
                f"User {target_user_id} received {total_power:,} GPU power.\n"
                f"New total: {updated_user.gpu_power:,}"
            )
        else:
            await update.message.reply_text("❌ User not found.")
            
    except ValueError:
        await update.message.reply_text("❌ Invalid amount.")