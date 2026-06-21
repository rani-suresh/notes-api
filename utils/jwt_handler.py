from jose import jwt, JWTError
from datetime import datetime, timedelta

SecretKey = "mykey123"
Algorithm = "HS256"

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SecretKey,
        algorithm = Algorithm
    )

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SecretKey, algorithms=[Algorithm]
        )
        return payload
    except JWTError:
        return None