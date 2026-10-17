"""
JWT Authentication Handler & Role Guard
"""
import base64
import json
import time
import hmac
import hashlib
from typing import Optional, Dict, Any
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.auth.models import UserRole, TokenData

security = HTTPBearer(auto_error=False)

def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    """Creates a signed HMAC-SHA256 JWT string."""
    to_encode = data.copy()
    expire_timestamp = time.time() + (expires_delta or (ACCESS_TOKEN_EXPIRE_MINUTES * 60))
    to_encode.update({"exp": expire_timestamp, "iat": time.time()})
    
    header = {"alg": ALGORITHM, "typ": "JWT"}
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(json.dumps(to_encode).encode()).decode().rstrip("=")
    
    signature_raw = hmac.new(
        SECRET_KEY.encode(),
        f"{header_b64}.{payload_b64}".encode(),
        hashlib.sha256
    ).digest()
    sig_b64 = base64.urlsafe_b64encode(signature_raw).decode().rstrip("=")
    
    return f"{header_b64}.{payload_b64}.{sig_b64}"

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verifies and decodes a signed JWT string."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header_b64, payload_b64, sig_b64 = parts
        
        # Verify signature
        expected_sig_raw = hmac.new(
            SECRET_KEY.encode(),
            f"{header_b64}.{payload_b64}".encode(),
            hashlib.sha256
        ).digest()
        expected_sig_b64 = base64.urlsafe_b64encode(expected_sig_raw).decode().rstrip("=")
        
        if not hmac.compare_digest(sig_b64, expected_sig_b64):
            return None
        
        # Decode payload (add padding back)
        rem = len(payload_b64) % 4
        if rem > 0:
            payload_b64 += "=" * (4 - rem)
        payload_data = json.loads(base64.urlsafe_b64decode(payload_b64.encode()).decode())
        
        if payload_data.get("exp", 0) < time.time():
            return None # Expired
            
        return payload_data
    except Exception:
        return None

def get_current_user_payload(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)) -> Dict[str, Any]:
    if not credentials:
        # Default fallback for demo simplicity if header omitted: Sports Scientist role
        return {
            "sub": "user_demo",
            "role": UserRole.SPORTS_SCIENTIST.value,
            "full_name": "Dr. Aris Thorne (Sports Scientist)"
        }
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload
