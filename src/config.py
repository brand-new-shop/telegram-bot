import pathlib
import tomllib
from dataclasses import dataclass

__all__ = ('Config', 'load_config')


@dataclass(frozen=True, slots=True)
class Config:
    telegram_bot_token: str
    server_base_url: str


def load_config(config_file_path: pathlib.Path) -> Config:
    config = tomllib.loads(config_file_path.read_text(encoding='utf-8'))
    return Config(
        telegram_bot_token=config['telegram_bot']['token'],
        server_base_url=config['server']['base_url'],
    )
