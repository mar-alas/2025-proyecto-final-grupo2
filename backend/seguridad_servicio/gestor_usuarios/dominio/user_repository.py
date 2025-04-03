from dominio.user import User
from dominio.user_mapper import UserMapper

class UserRepository:
    """Repositorio para manejar la persistencia de usuarios."""

    def __init__(self, db_session):
        """Permite inyectar una sesión de base de datos."""
        self.db_session = db_session

    def get_by_email(self, email):
        return self.db_session.query(User).filter_by(email=email).first()

    def save(self, user):
        user_model = UserMapper.to_model(user)
        self.db_session.add(user_model)
        self.db_session.commit()
