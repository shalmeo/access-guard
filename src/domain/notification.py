from dataclasses import dataclass
from datetime import datetime


@dataclass
class Notification:
    user_expired_in: datetime
