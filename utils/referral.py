from models.user import get_user, Session
from sqlalchemy import func
import uuid

def generate_referral_code():
    """Generate a unique referral code"""
    return str(uuid.uuid4())[:8].upper()

def validate_referral_code(referral_code):
    """Validate if a referral code exists and belongs to a valid user"""
    session = Session()
    try:
        user = session.query(User).filter(User.telegram_id == referral_code).first()
        return user is not None
    finally:
        session.close()

def get_referral_count(user_telegram_id):
    """Get the number of users referred by a specific user"""
    session = Session()
    try:
        count = session.query(User).filter(User.referred_by == str(user_telegram_id)).count()
        return count
    finally:
        session.close()

def get_referral_stats(user_telegram_id):
    """Get detailed referral statistics for a user"""
    session = Session()
    try:
        from models.user import User
        
        # Get direct referrals
        referrals = session.query(User).filter(User.referred_by == str(user_telegram_id)).all()
        
        total_referrals = len(referrals)
        total_bonus_earned = total_referrals * 500  # 500 GPU power per referral
        
        # Calculate total GPU power contributed by referrals
        referral_gpu_power = sum(user.gpu_power for user in referrals)
        
        return {
            'total_referrals': total_referrals,
            'bonus_earned': total_bonus_earned,
            'referral_gpu_power': referral_gpu_power,
            'referrals': referrals
        }
    finally:
        session.close()

def process_referral_bonus(referrer_id, new_user_id):
    """Process referral bonus when a new user joins"""
    from models.user import update_user_gpu_power
    
    # Give bonus to referrer
    referrer_bonus = 500  # GPU power bonus for successful referral
    update_user_gpu_power(referrer_id, referrer_bonus)
    
    # Give bonus to new user
    new_user_bonus = 200  # Welcome bonus for joining via referral
    update_user_gpu_power(new_user_id, new_user_bonus)
    
    return referrer_bonus, new_user_bonus

def get_top_referrers(limit=10):
    """Get top users by referral count"""
    session = Session()
    try:
        from models.user import User
        
        # Query users with their referral counts
        top_referrers = session.query(
            User.telegram_id,
            func.count(User.referred_by).label('referral_count')
        ).filter(
            User.referred_by.isnot(None)
        ).group_by(
            User.referred_by
        ).order_by(
            func.count(User.referred_by).desc()
        ).limit(limit).all()
        
        return top_referrers
    finally:
        session.close()

def calculate_referral_rewards(referral_count):
    """Calculate rewards based on referral milestones"""
    rewards = []
    
    # Milestone rewards
    milestones = [
        (5, 2500, "🥉 Bronze Referrer"),
        (10, 6000, "🥈 Silver Referrer"), 
        (25, 15000, "🥇 Gold Referrer"),
        (50, 35000, "💎 Diamond Referrer"),
        (100, 75000, "👑 Elite Referrer")
    ]
    
    total_milestone_bonus = 0
    current_title = "🔰 New Referrer"
    
    for milestone, bonus, title in milestones:
        if referral_count >= milestone:
            total_milestone_bonus += bonus
            current_title = title
    
    return total_milestone_bonus, current_title

def format_referral_link(bot_username, user_id):
    """Format a referral link for sharing"""
    return f"https://t.me/{bot_username}?start={user_id}"