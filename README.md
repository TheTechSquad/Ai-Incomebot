# 🤖 AI INCOME Telegram Bot + Web Interface

A comprehensive cryptocurrency mining simulation platform featuring both a Telegram bot and a modern web interface. Users can mine virtual hashes, upgrade GPU power, track referrals, and convert earnings to USDT.

## 🌟 Features

### 🤖 Telegram Bot
- **💎 Crypto Mining Simulation**: Users can mine virtual hashes using GPU power
- **⚡ GPU Power System**: Upgradeable mining power with shop functionality  
- **👥 Referral Program**: Earn bonuses by inviting friends
- **💰 Virtual Economy**: Convert hashes to USDT value
- **🏪 Power Shop**: Purchase GPU power upgrades
- **📊 Statistics**: Track mining progress and earnings
- **💸 Withdrawal System**: Request withdrawals when minimum is reached
- **🌐 Web App Integration**: Launch enhanced web interface from bot

### 🌐 Web Interface (Telegram Web App)
- **🎨 Beautiful Dashboard**: Modern, responsive interface with animations
- **⛏️ Enhanced Mining**: Interactive mining with real-time progress animations
- **📊 Advanced Statistics**: Detailed analytics with charts and progress tracking
- **🛒 Interactive Shop**: GPU power packages with calculator and comparisons
- **📱 Mobile Optimized**: Touch-friendly design for all devices
- **🎯 Achievement System**: Progress bars and unlockable achievements
- **💫 Real-time Updates**: Live data synchronization with Telegram bot
- **🎮 Gamified Experience**: Engaging animations and feedback

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Domain name or hosting service (for web interface deployment)

### 2. Installation

```bash
# Clone or download the project
cd ai-income-bot

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

1. Copy the environment template:
   ```bash
   cp env_template.txt .env
   ```

2. Edit `.env` file and configure:
   ```
   BOT_TOKEN=your_actual_bot_token_here
   BOT_USERNAME=your_bot_username
   ADMIN_USERNAME=your_admin_username
   WEB_APP_URL=https://your-domain.com
   FLASK_SECRET_KEY=your-secure-secret-key
   ```

### 4. Development Mode

```bash
# Run bot only
python bot.py

# Run web app only  
python app.py

# Run both together
python run.py
```

### 5. Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions for:
- Heroku
- Railway
- VPS/Server
- Docker

## 📁 Project Structure

```
ai_income_bot/
├── bot.py                 # Main bot application
├── handlers/              # Command handlers
│   ├── start.py          # Start command and user registration
│   ├── miner.py          # Mining functionality
│   ├── referral.py       # Referral system
│   ├── withdraw.py       # Withdrawal system
│   └── shop.py           # GPU power shop
├── models/               # Database models
│   └── user.py          # User model and database functions
├── utils/                # Utility functions
│   ├── mining.py        # Mining calculations
│   └── referral.py      # Referral utilities
├── requirements.txt      # Python dependencies
├── env_template.txt     # Environment variables template
├── instructions.txt     # Original project instructions
└── README.md           # This file
```

## 🎮 Bot Commands

### 🌐 Web Interface Commands
- `/webapp` - Launch the enhanced web interface (⭐ Recommended)
- `/start` - Welcome message with web app and bot options

### 🏠 Main Commands
- `/help` - Show all available commands
- `/stats` - View your mining statistics

### ⛏️ Mining Commands  
- `/miner` or `/mine` - Start mining hashes
- `/automine` - Information about auto-mining (premium feature)

### 💰 Economy Commands
- `/shop` - View GPU power packages
- `/buy [amount]` - Purchase GPU power (e.g., `/buy 5` for $5 package)
- `/withdraw` - Check withdrawal options and balance

### 👥 Social Commands
- `/referral` - Get your referral link to invite friends
- `/refstats` - View referral statistics

### 📊 Additional Commands
- `/history` - View withdrawal history
- `/leaderboard` - Top miners leaderboard (coming soon)

### 🌟 Interactive Features
- **Inline Keyboards**: Tap buttons for quick actions
- **Web App Integration**: Seamless transition to web interface
- **Real-time Updates**: Live synchronization between bot and web app

## 💰 Economy System

### Mining Formula
- **Base Hashes** = GPU Power × 0.0005
- **Random Factor** = ±20% variation for engagement
- **USDT Conversion** = 1 Hash = $0.01 USDT

### GPU Power Packages
- **$3 Package**: 37,500 GPU Power (30K base + 25% bonus)
- **$5 Package**: 62,500 GPU Power (50K base + 25% bonus)  
- **$10 Package**: 125,000 GPU Power (100K base + 25% bonus)
- **$20 Package**: 250,000 GPU Power (200K base + 25% bonus)

### Referral Bonuses
- **Referrer**: +500 GPU Power per successful referral
- **New User**: +200 GPU Power when joining via referral link

## 🗄️ Database Schema

The bot uses SQLite database with the following user model:

```python
class User:
    telegram_id: str (unique)
    gpu_power: int (default: 1000)
    mined_hashes: float (default: 0.0)
    referral_code: str (unique, auto-generated)
    referred_by: str (optional)
    last_mine_time: datetime
    created_at: datetime
```

## 🔧 Development

### Adding New Commands

1. Create handler function in appropriate file in `handlers/`
2. Import and register in `bot.py`
3. Add command documentation to help message

### Database Operations

Use the provided functions in `models/user.py`:
- `create_or_update_user(telegram_id, referral_code)`
- `get_user(telegram_id)`
- `update_user_mining(telegram_id, hashes_earned)`
- `update_user_gpu_power(telegram_id, additional_power)`

### Mining Calculations

Use functions in `utils/mining.py`:
- `calculate_mining(gpu_power)` - Calculate hashes earned
- `calculate_usdt_value(hashes)` - Convert hashes to USDT
- `estimate_daily_earnings(gpu_power)` - Estimate daily earnings

## 🚀 Deployment

### Heroku Deployment

1. Create `Procfile`:
   ```
   web: python bot.py
   ```

2. Set environment variables in Heroku dashboard
3. Deploy using Git or Heroku CLI

### VPS Deployment

1. Upload files to server
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables
4. Run with process manager like PM2 or systemd

## 🔒 Security Notes

- Never commit `.env` file or real bot tokens
- Use environment variables for all sensitive data
- Implement rate limiting for production use
- Add admin authentication for sensitive commands
- Consider using PostgreSQL for production instead of SQLite

## 🧪 Testing Checklist

- [ ] `/start` registers user and handles referral codes
- [ ] `/miner` calculates and awards hashes correctly
- [ ] `/referral` generates working invite links  
- [ ] `/buy 3` shows correct GPU power calculation
- [ ] `/withdraw` shows proper USDT conversion
- [ ] Database operations work correctly
- [ ] Error handling works for invalid commands

## 📝 Future Enhancements

- [ ] Real cryptocurrency integration
- [ ] Auto-mining background tasks
- [ ] Leaderboard system
- [ ] Admin dashboard
- [ ] CAPTCHA protection
- [ ] Daily mining limits
- [ ] Achievement system
- [ ] Multi-language support

## 🆘 Support

- **Technical Issues**: Check logs for error messages
- **Bot Token**: Get from [@BotFather](https://t.me/botfather)
- **Database Issues**: Ensure SQLite permissions are correct
- **Deployment Help**: Check platform-specific documentation

## 📄 License

This project is for educational purposes. Please ensure compliance with local regulations regarding cryptocurrency and financial services.

---

**Created by**: AI Assistant  
**Last Updated**: November 2, 2025  
**Version**: 1.0.0