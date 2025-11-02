"""
AI INCOME Web App
Flask web application for the Telegram bot with Telegram Web Apps integration
"""

import os
import json
import hashlib
import hmac
from urllib.parse import unquote
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv
import logging

# Import existing bot models and utilities
from models.user import get_user, create_or_update_user, update_user_mining, update_user_gpu_power
from utils.mining import calculate_mining, calculate_usdt_value, estimate_daily_earnings

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram Bot Token for Web App validation
BOT_TOKEN = os.getenv('BOT_TOKEN')

def verify_telegram_web_app_data(init_data, bot_token):
    """Verify Telegram Web App initialization data"""
    try:
        # Parse the init_data
        parsed_data = {}
        for item in init_data.split('&'):
            key, value = item.split('=', 1)
            parsed_data[key] = unquote(value)
        
        # Extract hash and create data_check_string
        received_hash = parsed_data.pop('hash', '')
        
        # Create data_check_string
        data_check_items = []
        for key in sorted(parsed_data.keys()):
            data_check_items.append(f"{key}={parsed_data[key]}")
        data_check_string = '\n'.join(data_check_items)
        
        # Create secret key
        secret_key = hmac.new(b'WebAppData', bot_token.encode(), hashlib.sha256).digest()
        
        # Calculate hash
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        
        return calculated_hash == received_hash
    except Exception as e:
        logger.error(f"Error verifying Telegram Web App data: {e}")
        return False

def get_user_from_telegram_data(init_data):
    """Extract user information from Telegram Web App init data"""
    try:
        parsed_data = {}
        for item in init_data.split('&'):
            key, value = item.split('=', 1)
            parsed_data[key] = unquote(value)
        
        user_data = json.loads(parsed_data.get('user', '{}'))
        return user_data.get('id')
    except Exception as e:
        logger.error(f"Error extracting user from Telegram data: {e}")
        return None

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """User dashboard with mining interface"""
    # Get user data from Telegram Web App
    init_data = request.args.get('tgWebAppData', '')
    
    if not init_data:
        return render_template('error.html', message="This app must be opened through Telegram")
    
    # Verify Telegram Web App data
    if not verify_telegram_web_app_data(init_data, BOT_TOKEN):
        return render_template('error.html', message="Invalid Telegram data")
    
    # Get user ID
    user_id = get_user_from_telegram_data(init_data)
    if not user_id:
        return render_template('error.html', message="Could not identify user")
    
    # Get user from database
    user = get_user(user_id)
    if not user:
        return render_template('error.html', message="User not found. Please start the bot first with /start")
    
    return render_template('dashboard.html', user=user)

@app.route('/shop')
def shop():
    """GPU power shop page"""
    init_data = request.args.get('tgWebAppData', '')
    
    if not init_data or not verify_telegram_web_app_data(init_data, BOT_TOKEN):
        return render_template('error.html', message="Invalid access")
    
    user_id = get_user_from_telegram_data(init_data)
    user = get_user(user_id) if user_id else None
    
    if not user:
        return render_template('error.html', message="User not found")
    
    # GPU Power packages
    packages = [
        {"id": 1, "price": 3, "base_power": 30000, "bonus_power": 7500, "total_power": 37500},
        {"id": 2, "price": 5, "base_power": 50000, "bonus_power": 12500, "total_power": 62500},
        {"id": 3, "price": 10, "base_power": 100000, "bonus_power": 25000, "total_power": 125000},
        {"id": 4, "price": 20, "base_power": 200000, "bonus_power": 50000, "total_power": 250000}
    ]
    
    return render_template('shop.html', user=user, packages=packages)

@app.route('/api/mine', methods=['POST'])
def api_mine():
    """API endpoint for mining operation"""
    try:
        data = request.get_json()
        init_data = data.get('init_data', '')
        
        if not verify_telegram_web_app_data(init_data, BOT_TOKEN):
            return jsonify({"error": "Invalid Telegram data"}), 401
        
        user_id = get_user_from_telegram_data(init_data)
        user = get_user(user_id) if user_id else None
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Calculate mining results
        hashes_earned = calculate_mining(user.gpu_power)
        
        # Update user's mined hashes
        update_user_mining(user_id, hashes_earned)
        
        # Get updated user data
        updated_user = get_user(user_id)
        usdt_value = calculate_usdt_value(updated_user.mined_hashes)
        
        return jsonify({
            "success": True,
            "hashes_earned": hashes_earned,
            "total_hashes": updated_user.mined_hashes,
            "usdt_value": usdt_value,
            "gpu_power": updated_user.gpu_power
        })
        
    except Exception as e:
        logger.error(f"Mining API error: {e}")
        return jsonify({"error": "Mining failed"}), 500

@app.route('/api/stats', methods=['POST'])
def api_stats():
    """API endpoint for user statistics"""
    try:
        data = request.get_json()
        init_data = data.get('init_data', '')
        
        if not verify_telegram_web_app_data(init_data, BOT_TOKEN):
            return jsonify({"error": "Invalid Telegram data"}), 401
        
        user_id = get_user_from_telegram_data(init_data)
        user = get_user(user_id) if user_id else None
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        usdt_value = calculate_usdt_value(user.mined_hashes)
        daily_estimate = estimate_daily_earnings(user.gpu_power)
        
        return jsonify({
            "gpu_power": user.gpu_power,
            "total_hashes": user.mined_hashes,
            "usdt_value": usdt_value,
            "referral_code": user.referral_code,
            "daily_estimate": daily_estimate,
            "member_since": user.created_at.strftime('%Y-%m-%d')
        })
        
    except Exception as e:
        logger.error(f"Stats API error: {e}")
        return jsonify({"error": "Failed to get stats"}), 500

@app.route('/api/purchase', methods=['POST'])
def api_purchase():
    """API endpoint for GPU power purchase"""
    try:
        data = request.get_json()
        init_data = data.get('init_data', '')
        package_id = data.get('package_id')
        
        if not verify_telegram_web_app_data(init_data, BOT_TOKEN):
            return jsonify({"error": "Invalid Telegram data"}), 401
        
        user_id = get_user_from_telegram_data(init_data)
        user = get_user(user_id) if user_id else None
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Package mapping
        packages = {
            1: {"price": 3, "power": 37500},
            2: {"price": 5, "power": 62500},
            3: {"price": 10, "power": 125000},
            4: {"price": 20, "power": 250000}
        }
        
        package = packages.get(package_id)
        if not package:
            return jsonify({"error": "Invalid package"}), 400
        
        # In a real app, you would process payment here
        # For demo purposes, we'll just add the power
        update_user_gpu_power(user_id, package["power"])
        
        updated_user = get_user(user_id)
        
        return jsonify({
            "success": True,
            "message": f"Successfully purchased ${package['price']} package!",
            "new_gpu_power": updated_user.gpu_power,
            "power_added": package["power"]
        })
        
    except Exception as e:
        logger.error(f"Purchase API error: {e}")
        return jsonify({"error": "Purchase failed"}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('error.html', message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('error.html', message="Internal server error"), 500

if __name__ == '__main__':
    # Development server
    app.run(debug=True, host='0.0.0.0', port=5000)