"""
Callback handlers for inline keyboard buttons
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes
from models.user import get_user
from handlers.miner import miner
from handlers.start import stats
from handlers.shop import shop
from handlers.referral import referral_link
import os

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries from inline keyboards"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    data = query.data
    
    if data == "mine_telegram":
        # Trigger mining through Telegram interface
        await mine_telegram_interface(update, context)
        
    elif data == "show_stats":
        # Show user statistics
        await show_stats_callback(update, context)
        
    elif data == "show_shop":
        # Show GPU power shop
        await show_shop_callback(update, context)
        
    elif data == "show_referral":
        # Show referral information
        await show_referral_callback(update, context)
        
    elif data == "webapp_help":
        # Show web app help information
        await show_webapp_help(update, context)
        
    elif data.startswith("buy_"):
        # Handle package purchase
        package_id = int(data.split("_")[1])
        await handle_package_purchase(update, context, package_id)

async def mine_telegram_interface(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mining interface within Telegram"""
    from utils.mining import calculate_mining, calculate_usdt_value
    from models.user import update_user_mining
    
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.callback_query.edit_message_text("❌ User not found. Please use /start first.")
        return
    
    # Calculate mining results
    hashes_earned = calculate_mining(user.gpu_power)
    
    # Update user's mined hashes
    update_user_mining(user_id, hashes_earned)
    
    # Get updated user data
    updated_user = get_user(user_id)
    usdt_value = calculate_usdt_value(updated_user.mined_hashes)
    
    # Create web app button for enhanced experience
    web_app_url = os.getenv('WEB_APP_URL', 'https://your-domain.com') + '/dashboard'
    
    keyboard = [
        [InlineKeyboardButton(
            text="🚀 Try Web Interface", 
            web_app=WebAppInfo(url=web_app_url)
        )],
        [
            InlineKeyboardButton(text="⛏️ Mine Again", callback_data="mine_telegram"),
            InlineKeyboardButton(text="📊 View Stats", callback_data="show_stats")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    mining_result = f"""
🎉 **Mining Successful!**

⛏️ **Mining Results:**
• Hashes Earned: {hashes_earned:.6f}
• Value Earned: ${hashes_earned * 0.01:.4f}

📊 **Updated Totals:**
• Total Hashes: {updated_user.mined_hashes:.6f}
• Total USDT Value: ${usdt_value:.2f}
• GPU Power: {updated_user.gpu_power:,}

🌟 **Want a better experience?** Try our web interface with:
• Beautiful mining animations
• Real-time progress tracking
• Enhanced statistics
• Mobile-optimized design

Keep mining to increase your earnings! 💰
    """
    
    await update.callback_query.edit_message_text(
        mining_result,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def show_stats_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics in callback"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.callback_query.edit_message_text("❌ User not found. Please use /start first.")
        return
    
    usdt_value = user.mined_hashes * 0.01
    
    # Calculate daily estimate
    daily_hashes = user.gpu_power * 0.0005 * 24  # Assuming 24 mines per day
    daily_usdt = daily_hashes * 0.01
    
    web_app_url = os.getenv('WEB_APP_URL', 'https://your-domain.com') + '/dashboard'
    
    keyboard = [
        [InlineKeyboardButton(
            text="📊 Detailed Stats (Web)", 
            web_app=WebAppInfo(url=web_app_url)
        )],
        [
            InlineKeyboardButton(text="⛏️ Start Mining", callback_data="mine_telegram"),
            InlineKeyboardButton(text="🏪 GPU Shop", callback_data="show_shop")
        ],
        [InlineKeyboardButton(text="🔙 Back to Main", callback_data="back_to_start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    stats_message = f"""
📊 **Your AI INCOME Statistics**

👤 **Profile:**
• User ID: {user_id}
• Member since: {user.created_at.strftime('%Y-%m-%d')}
• Referral Code: `{user.referral_code}`

⚡ **Mining Power:**
• GPU Power: {user.gpu_power:,}
• Daily Potential: ~{daily_hashes:.4f} hashes
• Daily USDT: ~${daily_usdt:.2f}

💰 **Earnings:**
• Total Hashes: {user.mined_hashes:.6f}
• USDT Value: ${usdt_value:.2f}
• Progress to $10 withdrawal: {(usdt_value/10)*100:.1f}%

📈 **Performance:**
• Hashes per Mine: ~{user.gpu_power * 0.0005:.6f}
• USDT per Mine: ~${(user.gpu_power * 0.0005) * 0.01:.4f}

🎯 **Next Steps:**
• Mine more to increase earnings
• Upgrade GPU power in shop
• Invite friends for bonuses
    """
    
    await update.callback_query.edit_message_text(
        stats_message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def show_shop_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show GPU power shop in callback"""
    web_app_url = os.getenv('WEB_APP_URL', 'https://your-domain.com') + '/shop'
    
    keyboard = [
        [InlineKeyboardButton(
            text="🛒 Open Full Shop (Web)", 
            web_app=WebAppInfo(url=web_app_url)
        )],
        [
            InlineKeyboardButton(text="💳 $3 Package", callback_data="buy_1"),
            InlineKeyboardButton(text="💎 $5 Package", callback_data="buy_2")
        ],
        [
            InlineKeyboardButton(text="🏆 $10 Package", callback_data="buy_3"),
            InlineKeyboardButton(text="👑 $20 Package", callback_data="buy_4")
        ],
        [InlineKeyboardButton(text="🔙 Back to Main", callback_data="back_to_start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    shop_message = """
🏪 **GPU Power Shop**

Boost your mining capabilities with these power packages:

💳 **$3 Starter Package**
• Base Power: 30,000
• Bonus (25%): +7,500
• **Total: 37,500 GPU Power**
• Daily Estimate: ~$0.72

💎 **$5 Popular Package** ⭐
• Base Power: 50,000
• Bonus (25%): +12,500
• **Total: 62,500 GPU Power**
• Daily Estimate: ~$1.20

🏆 **$10 Best Value Package** 🔥
• Base Power: 100,000
• Bonus (25%): +25,000
• **Total: 125,000 GPU Power**
• Daily Estimate: ~$2.40

👑 **$20 Premium Package**
• Base Power: 200,000
• Bonus (25%): +50,000
• **Total: 250,000 GPU Power**
• Daily Estimate: ~$4.80

💡 **Why Upgrade?**
• Higher earnings per mining session
• Faster return on investment
• 25% bonus power on all packages
• Compound your growth potential

🌐 **For the best shopping experience with calculator, comparisons, and detailed info, use our web interface!**
    """
    
    await update.callback_query.edit_message_text(
        shop_message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def show_referral_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show referral information in callback"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if not user:
        await update.callback_query.edit_message_text("❌ User not found. Please use /start first.")
        return
    
    bot_username = os.getenv('BOT_USERNAME', 'AI_IncomeBot')
    referral_url = f"https://t.me/{bot_username}?start={user.referral_code}"
    
    keyboard = [
        [InlineKeyboardButton(text="📤 Share Referral Link", url=f"https://t.me/share/url?url={referral_url}&text=🤖 Join AI INCOME and start mining crypto! 💎%0A%0A⚡ Get 200 bonus GPU Power when you join!%0A💰 Start earning USDT immediately!%0A%0AUse my referral link:")],
        [
            InlineKeyboardButton(text="📊 My Stats", callback_data="show_stats"),
            InlineKeyboardButton(text="⛏️ Start Mining", callback_data="mine_telegram")
        ],
        [InlineKeyboardButton(text="🔙 Back to Main", callback_data="back_to_start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    referral_message = f"""
👥 **Referral Program**

🔗 **Your Referral Code:** `{user.referral_code}`

🎁 **Rewards:**
• You earn: **+500 GPU Power** per referral
• Your friend gets: **+200 GPU Power** bonus
• No limit on referrals!

📊 **Your Referral Stats:**
• Total Referrals: Coming Soon
• Bonus Power Earned: Coming Soon
• Referral Earnings: Coming Soon

🔗 **Your Referral Link:**
`{referral_url}`

💡 **How to Refer:**
1. Share your referral link with friends
2. They join using your link
3. Both of you get bonus GPU power!
4. Start mining together and earn more!

🌟 **Pro Tips:**
• Share in crypto communities
• Post on social media
• Tell friends about passive income
• The more referrals, the more power!

Click "Share Referral Link" to send it easily! 🚀
    """
    
    await update.callback_query.edit_message_text(
        referral_message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def show_webapp_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show web app help information"""
    keyboard = [
        [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_start")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    help_message = """
📱 **How to Use the Web App**

🌟 **Getting Started:**
1. Click "Launch Web Interface" button
2. The web app will open in Telegram
3. Enjoy enhanced features!

✨ **Web App Features:**
• 🎨 Beautiful animated interface
• ⛏️ Enhanced mining with progress bars
• 📊 Detailed statistics and charts
• 🛒 Interactive shop with calculator
• 📱 Mobile-optimized design
• 🎯 Achievement system
• 📈 Real-time updates

🔒 **Security:**
• Secure integration with Telegram
• Your data is protected
• No separate login required
• Works seamlessly with bot

💡 **Tips:**
• Use landscape mode for best experience
• All your bot data syncs automatically
• Web app works offline for viewing
• Haptic feedback on supported devices

🆘 **Troubleshooting:**
• If web app doesn't load, check connection
• Make sure Telegram is updated
• Close and reopen if needed
• Contact support if issues persist

Ready to try the enhanced experience? 🚀
    """
    
    await update.callback_query.edit_message_text(
        help_message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def handle_package_purchase(update: Update, context: ContextTypes.DEFAULT_TYPE, package_id: int):
    """Handle package purchase confirmation"""
    packages = {
        1: {"price": 3, "power": 37500, "name": "Starter"},
        2: {"price": 5, "power": 62500, "name": "Popular"}, 
        3: {"price": 10, "power": 125000, "name": "Best Value"},
        4: {"price": 20, "power": 250000, "name": "Premium"}
    }
    
    package = packages.get(package_id)
    if not package:
        await update.callback_query.edit_message_text("❌ Invalid package selected.")
        return
    
    web_app_url = os.getenv('WEB_APP_URL', 'https://your-domain.com') + '/shop'
    
    keyboard = [
        [InlineKeyboardButton(
            text="💳 Complete Purchase (Web)", 
            web_app=WebAppInfo(url=web_app_url)
        )],
        [
            InlineKeyboardButton(text="✅ Confirm Purchase", callback_data=f"confirm_buy_{package_id}"),
            InlineKeyboardButton(text="❌ Cancel", callback_data="show_shop")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    purchase_message = f"""
💳 **Purchase Confirmation**

📦 **Package:** {package['name']} (${package['price']})
⚡ **GPU Power:** {package['power']:,}
📈 **Daily Estimate:** ~${(package['power'] * 0.0005 * 24) * 0.01:.2f}
🔄 **Break-even:** ~{package['price'] / ((package['power'] * 0.0005 * 24) * 0.01):.0f} days

💡 **Note:** This is a demo purchase. In production, this would integrate with payment processors like:
• PayPal
• Stripe  
• Crypto payments
• Mobile payments

🌐 **For the best purchase experience with detailed breakdown and secure payment, use our web interface!**

⚠️ **Demo Mode:** Clicking confirm will add the power immediately for demonstration purposes.
    """
    
    await update.callback_query.edit_message_text(
        purchase_message,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return to main start interface"""
    from handlers.start import start
    
    # Simulate the start command
    await start(update, context)