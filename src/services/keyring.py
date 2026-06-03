import keyring

from src.config import config


class KeyringService:
    def set_token(self, token: str) -> None:
        keyring.set_password(config.APP_NAME, "token", token)

    def get_token(self) -> str | None:
        return keyring.get_password(config.APP_NAME, "token")

    def delete_token(self) -> None:
        keyring.delete_password(config.APP_NAME, "token")
