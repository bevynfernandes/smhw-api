from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class CommentUser:
    id: int
    title: str
    backend_type: str
    forename: str
    surname: str
    avatar: str

    full_name: str = field(default_factory=str, init=False)

    def __post_init__(self):
        self.full_name: str = f"{self.title}. {self.forename} {self.surname}"


@dataclass(slots=True)
class CommentableTask:
    id: int
    type: str


@dataclass(slots=True)
class Comment:
    id: int
    message: str
    created_at: datetime
    commentable: CommentableTask
    user_id: int
    attachment_ids: list[int]


@dataclass(slots=True)
class Comments:
    users: list[CommentUser]
    comments: list[Comment]
