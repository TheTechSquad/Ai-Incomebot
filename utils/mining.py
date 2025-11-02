import random
from datetime import datetime

def calculate_mining(gpu_power):
    """Calculate hashes earned based on GPU power"""
    # Base formula from instructions: gpu_power * 0.0005
    base_hashes = gpu_power * 0.0005
    
    # Add some randomness to make mining more engaging
    # Random factor between 0.8 and 1.2 (±20% variation)
    random_factor = random.uniform(0.8, 1.2)
    
    # Calculate final hashes earned
    hashes_earned = base_hashes * random_factor
    
    return round(hashes_earned, 6)

def calculate_mining_per_minute(gpu_power):
    """Calculate hashes per minute for auto-mining features"""
    return calculate_mining(gpu_power) / 5  # Assuming 5-minute mining cycles

def get_mining_efficiency(gpu_power):
    """Get mining efficiency rating"""
    if gpu_power < 5000:
        return "⭐ Low"
    elif gpu_power < 20000:
        return "⭐⭐ Medium"
    elif gpu_power < 50000:
        return "⭐⭐⭐ High"
    elif gpu_power < 100000:
        return "⭐⭐⭐⭐ Very High"
    else:
        return "⭐⭐⭐⭐⭐ Elite"

def calculate_usdt_value(hashes):
    """Calculate USDT value from hashes"""
    return hashes * 0.01

def estimate_daily_earnings(gpu_power, mining_sessions_per_day=12):
    """Estimate daily earnings based on GPU power"""
    # Assuming user mines 12 times per day (every 2 hours)
    daily_hashes = calculate_mining(gpu_power) * mining_sessions_per_day
    daily_usdt = calculate_usdt_value(daily_hashes)
    return daily_hashes, daily_usdt

def format_large_number(number):
    """Format large numbers with appropriate suffixes"""
    if number >= 1_000_000:
        return f"{number/1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number/1_000:.1f}K"
    else:
        return str(int(number))

def get_mining_tips():
    """Get random mining tips for users"""
    tips = [
        "💡 Mine every few hours for maximum efficiency!",
        "🔥 Invite friends to get bonus GPU power!",
        "⚡ Higher GPU power = more hashes per mining session!",
        "💰 Collect hashes regularly to build your USDT balance!",
        "🚀 Upgrade your GPU power in the shop for better rewards!",
        "📈 Check your stats regularly to track progress!",
        "⏰ Set reminders to mine consistently!",
        "💎 Every hash counts - keep mining!"
    ]
    return random.choice(tips)