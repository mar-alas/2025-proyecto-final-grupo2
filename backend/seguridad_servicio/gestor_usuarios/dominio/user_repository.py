# from dominio.user import User
# from dominio.user_mapper import UserMapper
from gestor_usuarios.dominio.user_mapper import UserMapper
from gestor_usuarios.dominio.user_dto import UserDTO
from typing import Protocol


class IDatabaseSession(Protocol):
    def query(self, model): ...
    def add(self, instance): ...
    def commit(self): ...


class UserRepository:
    """Repositorio para manejar la persistencia de usuarios."""

    def __init__(self, db_session: IDatabaseSession, user_model_class):
        """Permite inyectar una sesión de base de datos."""
        self.db_session = db_session
        self.user_model_class = user_model_class
        

    def get_by_email(self, email: str):
        return self.db_session.query(self.user_model_class).filter_by(email=email).first()

    def save(self, user: UserDTO):
        user_data = UserMapper.to_model_v2(user)
        user_instance = self.user_model_class(**user_data)
        self.db_session.add(user_instance)
        self.db_session.commit()

        """
        user_model = UserMapper.to_model(user)
        self.db_session.add(user_model)
        self.db_session.commit()
        """