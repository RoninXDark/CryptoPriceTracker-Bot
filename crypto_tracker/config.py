import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    request_timeout_seconds: float = 10.0


def load_settings() -> Settings:
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token or token == "YOUR_TOKEN_HERE":
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is missing. Copy .env.example to .env and add "
            "a token created with @BotFather."
        )

    timeout = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "10"))
    return Settings(
        telegram_bot_token=token,
        request_timeout_seconds=timeout,
    )
