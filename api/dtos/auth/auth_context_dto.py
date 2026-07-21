from dataclasses import dataclass

from api.dtos.users import UserDTO

from .session_dto import SessionDTO


@dataclass(slots=True)
class AuthContextDTO:
    user: UserDTO
    session: SessionDTO
