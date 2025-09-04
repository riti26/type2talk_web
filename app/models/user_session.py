from datetime import datetime
from typing import Optional

class UserSession:
    def __init__(
        self,
        session_id: int,
        user_id: int,
        session_token: str,
        created_at: Optional[datetime] = None,
        expires_at: Optional[datetime] = None
    ):
        self.session_id = session_id
        self.user_id = user_id
        self.session_token = session_token
        self.created_at = created_at
        self.expires_at = expires_at

    def is_expired(self) -> bool:
        """Check if the session has expired."""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at
