"""// ZeaZDev [OAuth Service] //
// Project: Auto Bot Trader i18n //
// Version: 1.0.0 (Phase 3) //
// Author: ZeaZDev Meta-Intelligence (Generated) //
// --- DO NOT EDIT HEADER --- //"""
import os
from typing import Optional, Dict, Any
from google.oauth2 import id_token
from google.auth.transport import requests
from prisma import Prisma
import secrets

class OAuthService:
    """OAuth service for managing authentication flows"""
    
    def __init__(self):
        self.google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        self.google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        self.prisma = Prisma()
    
    async def verify_google_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify Google ID token and return user info"""
        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                self.google_client_id
            )
            
            # Token is valid, return user information
            return {
                "google_id": idinfo["sub"],
                "email": idinfo["email"],
                "name": idinfo.get("name"),
                "picture": idinfo.get("picture"),
                "email_verified": idinfo.get("email_verified", False)
            }
        except Exception as e:
            print(f"Token verification failed: {e}")
            return None
    
    async def get_or_create_user(self, google_id: str, email: str, profile_picture: Optional[str] = None):
        """Get existing user or create new user from OAuth data"""
        await self.prisma.connect()
        
        # Try to find user by Google ID
        user = await self.prisma.user.find_first(
            where={"googleId": google_id}
        )
        
        if user:
            # Update profile picture if changed
            if profile_picture and user.profilePicture != profile_picture:
                user = await self.prisma.user.update(
                    where={"id": user.id},
                    data={"profilePicture": profile_picture}
                )
        else:
            # Try to find by email (existing user without OAuth)
            user = await self.prisma.user.find_first(
                where={"email": email}
            )
            
            if user:
                # Link Google account to existing user
                user = await self.prisma.user.update(
                    where={"id": user.id},
                    data={
                        "googleId": google_id,
                        "oauthProvider": "google",
                        "profilePicture": profile_picture
                    }
                )
            else:
                # Create new user
                user = await self.prisma.user.create(
                    data={
                        "email": email,
                        "googleId": google_id,
                        "oauthProvider": "google",
                        "profilePicture": profile_picture
                    }
                )
                
                # Create default preferences for new user
                await self.prisma.userpreference.create(
                    data={
                        "userId": user.id,
                        "theme": "auto",
                        "language": "th",
                        "dashboardLayout": "grid",
                        "refreshInterval": 30
                    }
                )
                
                await self.prisma.notificationpreference.create(
                    data={
                        "userId": user.id,
                        "tradeAlerts": True,
                        "riskAlerts": True,
                        "systemAlerts": True,
                        "dailySummary": True
                    }
                )
        
        await self.prisma.disconnect()
        return user
    
    def generate_session_token(self) -> str:
        """Generate a secure session token"""
        return secrets.token_urlsafe(32)
