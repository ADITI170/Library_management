import jwt
from datetime import datetime, timedelta

# Function to generate a JWT token
def generate_access_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)  # Token expiration time (e.g., 1 hour)
    }
    return jwt.encode(payload, " ", algorithm='HS256')

# Function to validate a JWT token
def validate_access_token(token):
    try:
        payload = jwt.decode(token, " ", algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.InvalidTokenError:
        # Invalid token
        return None
