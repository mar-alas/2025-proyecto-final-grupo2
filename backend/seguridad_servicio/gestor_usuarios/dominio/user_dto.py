from dataclasses import dataclass
from typing import Optional

@dataclass
class UserDTO:
    """Representa los datos del usuario que se reciben en la API."""
    name: str
    email: str
    password: str
    role: str = None
    country: str = None
    city: str = None
    address: str = None
    id: Optional[int] = None