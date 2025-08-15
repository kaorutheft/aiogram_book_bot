from environs import Env
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str
    admin_id: int


@dataclass
class LogSettings:
    format: str
    level: str


@dataclass
class Config:
    bot: TgBot
    log: LogSettings


def load_config(path: str):
    env = Env()
    env.read_env(path)
    token = env('TOKEN')
    admin_id = list(map(int, env.list('ADMIN_ID')))
    return Config(bot=TgBot(token, admin_id),
                  log=LogSettings(env('LOG_FORMAT'), env('LOG_LEVEL')))
