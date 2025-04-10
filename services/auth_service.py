import random
import string
from datetime import datetime, timedelta

# In production, use a proper storage like Redis
# This is simplified for demonstration
otp_store = {}  # phone_number -> (otp, expiry)

def generate_otp(length=6):
    """Generate a random OTP of the specified length"""
    return ''.join(random.choices(string.digits, k=length))

def send_otp(phone_number):
    """
    Send an OTP to the provided phone number
    In a real application, this would integrate with an SMS service provider
    """
    otp = generate_otp()
    expiry = datetime.utcnow() + timedelta(minutes=10)
    otp_store[phone_number] = (otp, expiry)
    
    # In production: Send the OTP via an SMS service
    print(f"OTP for {phone_number}: {otp}")
    
    return True

def verify_otp(phone_number, otp):
    """Verify if the provided OTP is valid for the phone number"""
    if phone_number not in otp_store:
        return False
    
    stored_otp, expiry = otp_store[phone_number]
    
    if datetime.utcnow() > expiry:
        # OTP expired
        del otp_store[phone_number]
        return False
    
    if otp != stored_otp:
        return False
    
    # OTP verified successfully, remove it from store
    del otp_store[phone_number]
    return True
