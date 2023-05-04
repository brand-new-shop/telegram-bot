import logging
import pathlib
import tomllib
from dataclasses import dataclass

import structlog

__all__ = ('Config', 'load_config', 'setup_logging')


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


def setup_logging():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt='iso'),
            structlog.dev.ConsoleRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False
    )
