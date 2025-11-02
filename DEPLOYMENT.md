# 🚀 AI INCOME Deployment Guide

This guide covers deploying the AI INCOME Telegram Bot with Web Interface to various platforms.

## 📋 Prerequisites

- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Domain name or hosting service (for web interface)

## 🌐 Deployment Options

### 1. Heroku Deployment (Recommended)

#### Step 1: Prepare for Heroku
```bash
# Install Heroku CLI
# Visit: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create new app
heroku create your-app-name
```

#### Step 2: Configure Environment Variables
```bash
# Set bot token
heroku config:set BOT_TOKEN=your_bot_token_here

# Set bot username
heroku config:set BOT_USERNAME=your_bot_username

# Set admin username
heroku config:set ADMIN_USERNAME=your_admin_username

# Set web app URL (use your Heroku app URL)
heroku config:set WEB_APP_URL=https://your-app-name.herokuapp.com

# Set Flask secret key
heroku config:set FLASK_SECRET_KEY=your-secure-random-key

# Set deployment mode
heroku config:set DEPLOYMENT_MODE=web_only

# Set production flag
heroku config:set PRODUCTION=true
```

#### Step 3: Deploy to Heroku
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"

# Add Heroku remote
heroku git:remote -a your-app-name

# Deploy
git push heroku main
```

#### Step 4: Set Webhook (for bot)
```bash
# Set webhook to your Heroku app
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-app-name.herokuapp.com/webhook"
```

### 2. Railway Deployment

#### Step 1: Setup Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init
```

#### Step 2: Configure Environment Variables
Set these in Railway dashboard:
- `BOT_TOKEN`: Your Telegram bot token
- `BOT_USERNAME`: Your bot username
- `ADMIN_USERNAME`: Your admin username  
- `WEB_APP_URL`: Your Railway app URL
- `FLASK_SECRET_KEY`: Secure random key
- `DEPLOYMENT_MODE`: web_only
- `PRODUCTION`: true

#### Step 3: Deploy
```bash
railway up
```

### 3. VPS/Server Deployment

#### Step 1: Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv nginx -y

# Create app user
sudo useradd -m -s /bin/bash aiincome
sudo su - aiincome
```

#### Step 2: Application Setup
```bash
# Clone/upload your code
git clone <your-repo-url> ai-income-bot
cd ai-income-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp env_template.txt .env
# Edit .env with your configuration
nano .env
```

#### Step 3: Process Manager (PM2)
```bash
# Install Node.js and PM2
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g pm2

# Create ecosystem file
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'ai-income-web',
    script: 'run.py',
    interpreter: 'python3',
    env: {
      DEPLOYMENT_MODE: 'web_only',
      PRODUCTION: 'true',
      PORT: 5000
    }
  }, {
    name: 'ai-income-bot',
    script: 'bot.py',
    interpreter: 'python3',
    env: {
      DEPLOYMENT_MODE: 'bot_only'
    }
  }]
};
EOF

# Start applications
pm2 start ecosystem.config.js
pm2 startup
pm2 save
```

#### Step 4: Nginx Configuration
```bash
# Create Nginx config
sudo nano /etc/nginx/sites-available/aiincome

# Add this configuration:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/aiincome /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### 4. Docker Deployment

#### Step 1: Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "run.py"]
```

#### Step 2: Create docker-compose.yml
```yaml
version: '3.8'

services:
  ai-income:
    build: .
    ports:
      - "5000:5000"
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - BOT_USERNAME=${BOT_USERNAME}
      - ADMIN_USERNAME=${ADMIN_USERNAME}
      - WEB_APP_URL=${WEB_APP_URL}
      - FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
      - DEPLOYMENT_MODE=combined
      - PRODUCTION=true
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

#### Step 3: Deploy with Docker
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `BOT_TOKEN` | Telegram bot token | Yes | - |
| `BOT_USERNAME` | Bot username (without @) | Yes | - |
| `ADMIN_USERNAME` | Admin username for support | Yes | - |
| `WEB_APP_URL` | Full URL of web interface | Yes | - |
| `FLASK_SECRET_KEY` | Flask session secret key | Yes | - |
| `DEPLOYMENT_MODE` | `combined`, `bot_only`, `web_only` | No | `combined` |
| `PRODUCTION` | Enable production mode | No | `false` |
| `PORT` | Web app port | No | `5000` |

### Deployment Modes

1. **combined**: Runs both bot and web app in same process
2. **bot_only**: Runs only the Telegram bot
3. **web_only**: Runs only the web interface

## 📊 Monitoring and Logs

### Heroku Logs
```bash
# View logs
heroku logs --tail

# View specific process logs
heroku logs --ps web --tail
```

### PM2 Monitoring
```bash
# Monitor processes
pm2 monit

# View logs
pm2 logs ai-income-web
pm2 logs ai-income-bot

# Restart if needed
pm2 restart all
```

### Docker Logs
```bash
# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f ai-income
```

## 🔒 Security Checklist

- [ ] Use strong, unique `FLASK_SECRET_KEY`
- [ ] Keep bot token secure and never commit to git
- [ ] Enable HTTPS/SSL for web interface
- [ ] Use environment variables for all secrets
- [ ] Regularly update dependencies
- [ ] Monitor logs for suspicious activity
- [ ] Set up proper firewall rules
- [ ] Use reverse proxy (Nginx) for production

## 🚨 Troubleshooting

### Common Issues

1. **Web App not opening in Telegram**
   - Check `WEB_APP_URL` is correctly set
   - Ensure HTTPS is enabled
   - Verify bot token is correct

2. **Bot not responding**
   - Check bot token is valid
   - Verify webhook is set correctly
   - Check process is running

3. **Database errors**
   - Ensure write permissions for SQLite
   - Check file paths are correct
   - Verify database initialization

4. **API errors**
   - Check internet connectivity
   - Verify all required environment variables
   - Monitor rate limits

### Health Checks

Create these endpoints for monitoring:

```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': time.time()}

@app.route('/ready')
def ready_check():
    # Check database connection, etc.
    return {'status': 'ready'}
```

## 📈 Scaling Considerations

### For High Traffic:
- Use PostgreSQL instead of SQLite
- Implement Redis for caching
- Use load balancer for multiple instances
- Consider microservices architecture
- Implement proper logging and monitoring

### Database Migration:
```bash
# Backup SQLite data
cp ai_income.db ai_income_backup.db

# Export to SQL
sqlite3 ai_income.db .dump > backup.sql

# Import to PostgreSQL
psql your_db < backup.sql
```

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section
2. Review logs for error messages
3. Ensure all environment variables are set
4. Check platform-specific documentation
5. Contact support with detailed error information

---

**Happy Deploying! 🚀**