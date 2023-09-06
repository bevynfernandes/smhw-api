from dataclasses import dataclass, field
from datetime import datetime

from .tools import convert_datetime


@dataclass(slots=True)
class BearerUser:
    """The class BearerUser has attributes related to user information and activity, and uses a
    post-initialization method to convert datetime objects.
    """

    id: int
    email: str
    last_activity_at: datetime
    username: str
    calendar_token: str
    uid: str
    last_user_activity_at: datetime

    def __post_init__(self):
        self.last_activity_at = convert_datetime(self.last_activity_at)
        self.last_user_activity_at = convert_datetime(self.last_user_activity_at)


@dataclass(slots=True)
class Auth:
    smhw_token: str
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    created_at: int
    user_id: int
    school_id: int
    user_type: str
    account_switch_enabled: bool


@dataclass(slots=True)
class User:
    """The class defines a User object with various attributes and methods, including a full name attribute
    that is automatically generated based on the user's title, forename, and surname.
    """

    id: int
    avatar: str
    forename: str
    school_id: int
    surname: str
    created_at: datetime
    backend_type: str
    updated_at: datetime
    title: str
    user_private_info_id: int
    user_identity_id: int

    disabled: bool = field(default_factory=bool, init=False)
    full_name: str = field(default_factory=str, init=False)

    def __post_init__(self):
        self.created_at = convert_datetime(self.created_at)
        self.updated_at = convert_datetime(self.updated_at)
        self.full_name: str = f"{self.title}. {self.forename} {self.surname}"
