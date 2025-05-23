from src.entities import User
from src.interfaces import IDataRepository

from src.utils import hash_password, check_password, create_token


class ManageUsersUsecase:
    def __init__(self, users_repository: IDataRepository):
        self._user_repository = users_repository

    def _get_user(self, filters: dict) -> User | None:
        return self._user_repository.get(filters=filters, first_only=True)

    def get_user_by_id(self, id: int) -> User | None:
        filters = {"id": id}
        return self._get_user(filters)

    def get_user_by_email(self, email: str) -> User | None:
        filters = {"email": email}
        return self._get_user(filters)

    def create_user(self, data: dict) -> tuple[User | None, str | None]:
        user_exists = self.get_user_by_email(data["email"])
        if user_exists:
            return None, "Email Already in Use"

        # Hasheamos el password entregado
        user_data = {
            "name": data["name"],
            "email": data["email"],
            "password": hash_password(data["password"]),
        }

        # Insertamos la entidad y almacenamos en una variable.
        try:
            user_created = self._user_repository.insert(user_data)
        except Exception as e:
            return None, str(e)
        return self.get_user_by_id(user_created.id), None

    def update_user(self, user_id: int, data: dict) -> tuple[User | None, str | None]:
        user_exists = self.get_user_by_id(user_id)
        if not user_exists:
            return None, "User Not Found"
        try:
            if data.get("password") and data["password"] != "":
                data["password"] = hash_password(data["password"])
            user_updated = self._user_repository.update(user_id, data)
            return user_updated, None
        except Exception as e:
            return None, str(e)
        
    def user_log_in(self, data: dict) -> tuple[str | None, str | None]:
        user_email = data["email"]
        input_password = data["password"]

        user = self.get_user_by_email(user_email)

        # No deberíamos transparentar
        # si el error está en el email
        # o el password por razones de seguridad
        if not user or not check_password(user.password, input_password):
            return None, None

        return user, create_token(user.id)
