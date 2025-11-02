#!/usr/bin/env python3
"""
AI INCOME Test Suite
Quick tests to verify bot and web app functionality
"""

import os
import sys
import sqlite3
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test environment configuration"""
    print("🔧 Testing Environment Configuration...")
    
    required_vars = ['BOT_TOKEN', 'BOT_USERNAME', 'ADMIN_USERNAME']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ Environment configuration OK")
    return True

def test_database():
    """Test database functionality"""
    print("🗄️ Testing Database...")
    
    try:
        from models.user import create_or_update_user, get_user
        
        # Test create user
        test_user_id = 123456789
        user = create_or_update_user(test_user_id, None)
        
        if user:
            print("✅ User creation OK")
        else:
            print("❌ User creation failed")
            return False
        
        # Test get user
        retrieved_user = get_user(test_user_id)
        
        if retrieved_user and retrieved_user.telegram_id == str(test_user_id):
            print("✅ User retrieval OK")
        else:
            print("❌ User retrieval failed")
            return False
        
        print("✅ Database tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_mining_logic():
    """Test mining calculations"""
    print("⛏️ Testing Mining Logic...")
    
    try:
        from utils.mining import calculate_mining, calculate_usdt_value, estimate_daily_earnings
        
        # Test mining calculation
        gpu_power = 1000
        hashes = calculate_mining(gpu_power)
        
        if hashes > 0:
            print(f"✅ Mining calculation OK: {hashes:.6f} hashes for {gpu_power} GPU power")
        else:
            print("❌ Mining calculation failed")
            return False
        
        # Test USDT conversion
        usdt_value = calculate_usdt_value(hashes)
        expected_usdt = hashes * 0.01
        
        if abs(usdt_value - expected_usdt) < 0.000001:
            print(f"✅ USDT conversion OK: {usdt_value:.4f} USDT")
        else:
            print("❌ USDT conversion failed")
            return False
        
        # Test daily estimate
        daily_estimate = estimate_daily_earnings(gpu_power)
        
        if daily_estimate > 0:
            print(f"✅ Daily estimate OK: ${daily_estimate:.2f}")
        else:
            print("❌ Daily estimate failed")
            return False
        
        print("✅ Mining logic tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Mining logic error: {e}")
        return False

def test_bot_token():
    """Test bot token validity"""
    print("🤖 Testing Bot Token...")
    
    bot_token = os.getenv('BOT_TOKEN')
    
    if not bot_token:
        print("❌ No bot token found")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data.get('result', {})
                print(f"✅ Bot token valid: {bot_info.get('first_name', 'Unknown')} (@{bot_info.get('username', 'Unknown')})")
                return True
        
        print("❌ Bot token invalid or bot not accessible")
        return False
        
    except Exception as e:
        print(f"❌ Bot token test error: {e}")
        return False

def test_web_app():
    """Test web app functionality"""
    print("🌐 Testing Web App...")
    
    try:
        from app import app
        
        # Test app creation
        if app:
            print("✅ Flask app created successfully")
        else:
            print("❌ Flask app creation failed")
            return False
        
        # Test basic route
        with app.test_client() as client:
            response = client.get('/')
            
            if response.status_code == 200:
                print("✅ Web app home route OK")
            else:
                print(f"❌ Web app home route failed: {response.status_code}")
                return False
        
        print("✅ Web app tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Web app error: {e}")
        return False

def test_imports():
    """Test all imports"""
    print("📦 Testing Imports...")
    
    try:
        import telegram
        print("✅ python-telegram-bot imported")
        
        import flask
        print("✅ Flask imported")
        
        import sqlalchemy
        print("✅ SQLAlchemy imported")
        
        from models import user
        print("✅ User model imported")
        
        from handlers import start, miner, shop, referral, withdraw, callbacks
        print("✅ Handler modules imported")
        
        from utils import mining, referral
        print("✅ Utility modules imported")
        
        print("✅ All imports successful")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_file_structure():
    """Test file structure"""
    print("📁 Testing File Structure...")
    
    required_files = [
        'bot.py',
        'app.py', 
        'run.py',
        'requirements.txt',
        '.env',
        'handlers/__init__.py',
        'models/__init__.py',
        'utils/__init__.py',
        'templates/base.html',
        'static/css/style.css',
        'static/js/app.js'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ File structure OK")
    return True

def main():
    """Run all tests"""
    print("🧪 AI INCOME Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment", test_environment),
        ("File Structure", test_file_structure), 
        ("Imports", test_imports),
        ("Database", test_database),
        ("Mining Logic", test_mining_logic),
        ("Bot Token", test_bot_token),
        ("Web App", test_web_app)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name} tests...")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Your AI INCOME setup is ready!")
        print("\n🚀 Next steps:")
        print("1. Deploy your application (see DEPLOYMENT.md)")
        print("2. Update WEB_APP_URL in .env with your actual domain")
        print("3. Test the bot with /start command")
        print("4. Test the web interface with /webapp command")
    else:
        print("⚠️ Some tests failed. Please fix the issues before deployment.")
    
    return failed == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)