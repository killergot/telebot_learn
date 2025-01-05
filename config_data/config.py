from dataclasses import dataclass
from environs import Env
from pyowm import OWM


@dataclass
class TgBot:
    token: str
    ID_MY_GIRL: int
    MY_ID: int


@dataclass
class Config:
    tg_bot: TgBot
    mgr: OWM.weather_manager




def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    owm = OWM(env("OWM_TOKEN"))
    mgr = owm.weather_manager()
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               ID_MY_GIRL=int(env('ID_MY_GIRL')),
                               MY_ID=int(env('MY_ID'))),
                 mgr=mgr)

