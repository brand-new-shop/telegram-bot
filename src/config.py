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


@dataclass(frozen=True, slots=True)
class YoomoneyPaymentsConfig:
    is_enabled: bool


@dataclass(frozen=True, slots=True)
class MinerlockPaymentsConfig:
    is_enabled: bool


@dataclass(frozen=True, slots=True)
class CoinpaymentsPaymentsConfig:
    is_enabled: bool


@dataclass(frozen=True, slots=True)
class CoinbasePaymentsConfig:
    is_enabled: bool


@dataclass(frozen=True, slots=True)
class PaymentsConfig:
    crypto_payments: str
    qiwi: QiwiPaymentsConfig
    yoomoney: YoomoneyPaymentsConfig
    minerlock: MinerlockPaymentsConfig
    coinbase: CoinbasePaymentsConfig
    coinpayments: CoinpaymentsPaymentsConfig


@dataclass(frozen=True, slots=True)
class Config:
    backup: BackupConfig
    payments: PaymentsConfig

    @classmethod
    def parse_config(cls, config_parser: ConfigParser) -> 'Config':
        return cls(
            backup=BackupConfig(
                period=config_parser['backup']['backup_period'],
                sending_period=config_parser['backup']['sending_backup_period'],
            ),
            payments=PaymentsConfig(
                crypto_payments=config_parser['payments']['crypto_payments'],
                qiwi=QiwiPaymentsConfig(
                    is_enabled=config_parser['payments.qiwi'].getboolean('is_enabled'),
                    payment_method=config_parser['payments.qiwi']['is_enabled'],
                ),
                coinpayments=CoinpaymentsPaymentsConfig(
                    is_enabled=config_parser['payments.coinpayments'].getboolean('is_enabled'),
                ),
                coinbase=CoinbasePaymentsConfig(
                    is_enabled=config_parser['payments.coinbase'].getboolean('is_enabled'),
                ),
                minerlock=MinerlockPaymentsConfig(
                    is_enabled=config_parser['payments.minerlock'].getboolean('is_enabled'),
                ),
                yoomoney=YoomoneyPaymentsConfig(
                    is_enabled=config_parser['payments.yoomoney'].getboolean('is_enabled'),
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
