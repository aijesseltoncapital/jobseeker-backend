import requests
import json
from flask import current_app

def verify_google_token(token):
    """
    Verify a Google OAuth token and return user info if valid
    
    In a real implementation, this would use the Google API client library
    or make proper calls to Google's token info endpoint
    """
    try:
        # This is a simplified implementation
        # In production: Use google-auth library
        response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
        
        if response.status_code == 200:
            user_info = response.json()
            return {
                'sub': user_info.get('sub'),  # Google's user ID
                'email': user_info.get('email'),
                'name': user_info.get('name')
            }
        return None
    except Exception as e:
        print(f"Error verifying Google token: {e}")
        return None

def verify_linkedin_token(token):
    """
    Verify a LinkedIn OAuth token and return user info if valid
    
    In a real implementation, this would make calls to LinkedIn's API
    """
    try:
        # Get LinkedIn user profile
        # In production: Properly handle LinkedIn's OAuth flow
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get('https://api.linkedin.com/v2/me', headers=headers)
        
        if response.status_code == 200:
            user_info = response.json()
            return {
                'id': user_info.get('id'),
                'localizedFirstName': user_info.get('localizedFirstName', ''),
                'localizedLastName': user_info.get('localizedLastName', '')
            }
        return None
    except Exception as e:
        print(f"Error verifying LinkedIn token: {e}")
        return None