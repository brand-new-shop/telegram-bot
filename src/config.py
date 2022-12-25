import pathlib
from configparser import ConfigParser
from dataclasses import dataclass

__all__ = ('Config',)


@dataclass(frozen=True, slots=True)
class BackupConfig:
    period: str
    sending_period: str


@dataclass(frozen=True, slots=True)
class QiwiPaymentsConfig:
    is_enabled: bool
    payment_method: str
    number: str
    nickname: str
    token: str


@dataclass(frozen=True, slots=True)
class YoomoneyPaymentsConfig:
    is_enabled: bool
    token: str


@dataclass(frozen=True, slots=True)
class MinerlockPaymentsConfig:
    is_enabled: bool
    api_id: str
    api_key: str


@dataclass(frozen=True, slots=True)
class CoinpaymentsPaymentsConfig:
    is_enabled: bool
    public_key: str
    secret_key: str


@dataclass(frozen=True, slots=True)
class CoinbasePaymentsConfig:
    is_enabled: bool
    api_key: str


@dataclass(frozen=True, slots=True)
class PaymentsConfig:
    crypto_payments: str
    qiwi: QiwiPaymentsConfig
    yoomoney: YoomoneyPaymentsConfig
    minerlock: MinerlockPaymentsConfig
    coinbase: CoinbasePaymentsConfig
    coinpayments: CoinpaymentsPaymentsConfig


@dataclass(frozen=True, slots=True)
class TelegramBotConfig:
    token: str
    admin_id_for_backup_sending: int


@dataclass(frozen=True, slots=True)
class ServerConfig:
    base_url: str


@dataclass(frozen=True, slots=True)
class Config:
    telegram_bot: TelegramBotConfig
    server: ServerConfig
    backup: BackupConfig
    payments: PaymentsConfig

    @classmethod
    def parse_config(cls, config_parser: ConfigParser) -> 'Config':
        return cls(
            telegram_bot=TelegramBotConfig(
                token=config_parser['telegram_bot']['token'],
                admin_id_for_backup_sending=config_parser['telegram_bot'].getint('admin_id_for_backup_sending'),
            ),
            server=ServerConfig(
                base_url=config_parser['server']['base_url'],
            ),
            backup=BackupConfig(
                period=config_parser['backup']['backup_period'],
                sending_period=config_parser['backup']['sending_backup_period'],
            ),
            payments=PaymentsConfig(
                crypto_payments=config_parser['payments']['crypto_payments'],
                qiwi=QiwiPaymentsConfig(
                    is_enabled=config_parser['payments.qiwi'].getboolean('is_enabled'),
                    payment_method=config_parser['payments.qiwi'].get('payment_method'),
                    number=config_parser['payments.qiwi'].get('number'),
                    nickname=config_parser['payments.qiwi'].get('nickname'),
                    token=config_parser['payments.qiwi'].get('token'),
                ),
                coinpayments=CoinpaymentsPaymentsConfig(
                    is_enabled=config_parser['payments.coinpayments'].getboolean('is_enabled'),
                    public_key=config_parser['payments.coinpayments'].get('public_key'),
                    secret_key=config_parser['payments.coinpayments'].get('secret_key'),
                ),
                coinbase=CoinbasePaymentsConfig(
                    is_enabled=config_parser['payments.coinbase'].getboolean('is_enabled'),
                    api_key=config_parser['payments.coinbase'].get('api_key'),
                ),
                minerlock=MinerlockPaymentsConfig(
                    is_enabled=config_parser['payments.minerlock'].getboolean('is_enabled'),
                    api_id=config_parser['payments.minerlock'].get('api_id'),
                    api_key=config_parser['payments.minerlock'].get('api_key'),
                ),
                yoomoney=YoomoneyPaymentsConfig(
                    is_enabled=config_parser['payments.yoomoney'].getboolean('is_enabled'),
                    token=config_parser['payments.yoomoney'].get('token'),
                ),
            )
        )

    @classmethod
    def from_file(cls, file_path: str | pathlib.Path) -> 'Config':
        config_parser = ConfigParser()
        config_parser.read(file_path)
        return cls.parse_config(config_parser)

    @classmethod
    def from_string(cls, config_string: str) -> 'Config':
        config_parser = ConfigParser()
        config_parser.read_string(config_string)
        return cls.parse_config(config_parser)
