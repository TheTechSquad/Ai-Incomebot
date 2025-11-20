# 🚀 Render.com Deployment Guide

This guide will help you deploy your AI INCOME Bot to Render.com.

## 📋 Prerequisites

1. GitHub account with your code pushed
2. Render.com account (free) - Sign up at https://render.com

## 🎯 Deployment Steps

### Step 1: Create Render Account
1. Go to https://render.com
2. Click "Get Started" or "Sign Up"
3. Sign up with your GitHub account (recommended)
4. Authorize Render to access your GitHub repositories

### Step 2: Deploy Web App

1. **Create New Web Service**
   - Click "New +" button in Render dashboard
   - Select "Web Service"
   - Connect your GitHub repository: `TheTechSquad/Ai-Incomebot`
   - Click "Connect"

2. **Configure Web Service**
   ```
   Name: ai-income-webapp (or your preferred name)
   Region: Oregon (US West) or closest to you
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app --bind 0.0.0.0:$PORT
   Instance Type: Free
   ```

3. **Add Environment Variables**
   Click "Advanced" and add these environment variables:
   ```
   BOT_TOKEN=8170070120:AAEn5ds81XBsCpY6J_NTsU7ByElYunwCChQ
   BOT_USERNAME=AI_IncomeBot
   ADMIN_USERNAME=MrDelvan
   FLASK_SECRET_KEY=<generate random key>
   DEPLOYMENT_MODE=web_only
   ```

   To generate FLASK_SECRET_KEY, run:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes first time)
   - Your web app URL will be: `https://ai-income-webapp.onrender.com`

### Step 3: Deploy Bot (Background Worker)

1. **Create Background Worker**
   - Click "New +" again
   - Select "Background Worker"
   - Connect same repository: `TheTechSquad/Ai-Incomebot`

2. **Configure Worker**
   ```
   Name: ai-income-bot
   Region: Oregon (same as web app)
   Branch: main
   Build Command: pip install -r requirements.txt
   Start Command: python bot.py
   Instance Type: Free
   ```

3. **Add Environment Variables**
   ```
   BOT_TOKEN=8170070120:AAEn5ds81XBsCpY6J_NTsU7ByElYunwCChQ
   BOT_USERNAME=AI_IncomeBot
   ADMIN_USERNAME=MrDelvan
   DEPLOYMENT_MODE=bot_only
   ```

4. **Deploy**
   - Click "Create Background Worker"
   - Bot will start running in background

### Step 4: Update Bot Configuration

1. **Copy your Web App URL**
   - From Render dashboard: `https://ai-income-webapp.onrender.com`

2. **Update .env file locally**
   ```
   WEB_APP_URL=https://ai-income-webapp.onrender.com
   ```

3. **Update WEB_APP_URL in Render**
   - Go to your web service settings
   - Add/update environment variable:
     ```
     WEB_APP_URL=https://ai-income-webapp.onrender.com
     ```

4. **Update bot.py on Render**
   - Push changes to GitHub
   - Render will auto-deploy

### Step 5: Configure Telegram Bot Web App

1. **Open Telegram and message @BotFather**

2. **Set Menu Button**
   ```
   /setmenubutton
   Select: @AI_IncomeBot
   Type: url
   URL: https://ai-income-webapp.onrender.com/dashboard
   Button text: 🚀 Open Dashboard
   ```

3. **Test the Bot**
   - Open your bot: https://t.me/AI_IncomeBot
   - Click the menu button to open web app
   - Test commands like /start, /miner, /shop

## 🔧 Important Notes

### Free Tier Limitations
- Web services sleep after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- 750 hours/month free (shared across all services)
- Consider upgrading if you need 24/7 uptime

### Database Persistence
- Free tier uses ephemeral storage (data may be lost on restart)
- For production, add a PostgreSQL database:
  1. In Render, click "New +" → "PostgreSQL"
  2. Copy the Internal Database URL
  3. Add to environment variables: `DATABASE_URL=<postgres-url>`

### Auto-Deploy
- Render automatically deploys when you push to main branch
- You can disable this in service settings

## 🐛 Troubleshooting

### Web App Not Loading
- Check Render logs: Service → Logs tab
- Verify environment variables are set
- Check if service is sleeping (free tier)

### Bot Not Responding
- Check worker logs in Render dashboard
- Verify BOT_TOKEN is correct
- Ensure worker service is running

### Database Issues
- SQLite database resets on each deploy (free tier)
- Use PostgreSQL for persistent storage
- Check file permissions

## 📊 Monitoring

1. **View Logs**
   - Go to service in Render dashboard
   - Click "Logs" tab
   - Real-time logs show all activity

2. **Check Status**
   - Dashboard shows service health
   - Green = Running
   - Yellow = Deploying
   - Red = Error

3. **Restart Service**
   - Click "Manual Deploy" → "Clear build cache & deploy"
   - Or "Restart" for quick restart

## 🎉 Success Checklist

- [ ] Web app deployed and accessible
- [ ] Bot worker running in background
- [ ] Environment variables configured
- [ ] Web app URL updated in bot code
- [ ] BotFather menu button configured
- [ ] Bot responds to commands
- [ ] Web app loads in Telegram

## 🔗 Useful Links

- Render Dashboard: https://dashboard.render.com
- Render Docs: https://render.com/docs
- Your Bot: https://t.me/AI_IncomeBot
- Support: Contact @MrDelvan

---

**Deployed by**: AI Assistant  
**Last Updated**: November 20, 2025
