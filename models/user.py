from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True, nullable=False)
    gpu_power = Column(Integer, default=1000)
    mined_hashes = Column(Float, default=0.0)
    referral_code = Column(String, unique=True)
    referred_by = Column(String, nullable=True)
    last_mine_time = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, telegram_id, referred_by=None):
        self.telegram_id = str(telegram_id)
        self.referral_code = str(uuid.uuid4())[:8]
        self.referred_by = referred_by

# Database setup
engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

def create_or_update_user(telegram_id, referral_code=None):
    """Create new user or return existing user"""
    session = get_session()
    try:
        user = session.query(User).filter(User.telegram_id == str(telegram_id)).first()
        if not user:
            # Check if referral code exists and is valid
            referred_by_user = None
            if referral_code:
                referred_by_user = session.query(User).filter(User.telegram_id == referral_code).first()
            
            user = User(telegram_id, referred_by=referral_code if referred_by_user else None)
            session.add(user)
            
            # Give bonus to referrer
            if referred_by_user:
                referred_by_user.gpu_power += 500  # Bonus for successful referral
                
        session.commit()
        # Refresh the user object to avoid detached instance issues
        session.refresh(user)
        
        # Create a new user object with the data to return
        user_data = {
            'telegram_id': user.telegram_id,
            'gpu_power': user.gpu_power,
            'mined_hashes': user.mined_hashes,
            'referral_code': user.referral_code,
            'referred_by': user.referred_by,
            'last_mine_time': user.last_mine_time,
            'created_at': user.created_at
        }
        return type('UserData', (), user_data)()
    finally:
        session.close()

def get_user(telegram_id):
    """Get user by telegram ID"""
    session = get_session()
    try:
        user = session.query(User).filter(User.telegram_id == str(telegram_id)).first()
        if user:
            # Create a new user object with the data to return
            user_data = {
                'telegram_id': user.telegram_id,
                'gpu_power': user.gpu_power,
                'mined_hashes': user.mined_hashes,
                'referral_code': user.referral_code,
                'referred_by': user.referred_by,
                'last_mine_time': user.last_mine_time,
                'created_at': user.created_at
            }
            return type('UserData', (), user_data)()
        return None
    finally:
        session.close()

def update_user_mining(telegram_id, hashes_earned):
    """Update user's mining data"""
    session = get_session()
    try:
        user = session.query(User).filter(User.telegram_id == str(telegram_id)).first()
        if user:
            user.mined_hashes += hashes_earned
            user.last_mine_time = datetime.utcnow()
            session.commit()
            session.refresh(user)
            
            # Return user data object
            user_data = {
                'telegram_id': user.telegram_id,
                'gpu_power': user.gpu_power,
                'mined_hashes': user.mined_hashes,
                'referral_code': user.referral_code,
                'referred_by': user.referred_by,
                'last_mine_time': user.last_mine_time,
                'created_at': user.created_at
            }
            return type('UserData', (), user_data)()
        return None
    finally:
        session.close()

def update_user_gpu_power(telegram_id, additional_power):
    """Update user's GPU power"""
    session = get_session()
    try:
        user = session.query(User).filter(User.telegram_id == str(telegram_id)).first()
        if user:
            user.gpu_power += additional_power
            session.commit()
            session.refresh(user)
            
            # Return user data object
            user_data = {
                'telegram_id': user.telegram_id,
                'gpu_power': user.gpu_power,
                'mined_hashes': user.mined_hashes,
                'referral_code': user.referral_code,
                'referred_by': user.referred_by,
                'last_mine_time': user.last_mine_time,
                'created_at': user.created_at
            }
            return type('UserData', (), user_data)()
        return None
    finally:
        session.close()