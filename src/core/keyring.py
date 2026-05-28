import keyring

from src.config import config


def set_token(token: str) -> None:
    keyring.set_password(config.APP_NAME, "token", token)


def get_token() -> str | None:
    return keyring.get_password(config.APP_NAME, "token")


def delete_token() -> None:
    keyring.delete_password(config.APP_NAME, "token")
