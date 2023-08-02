from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str


@dataclass
class Contacts:
    phone: str
    manager: str
    group: str


@dataclass
class Company:
    name: str
    site: str


@dataclass
class Wallet:
    click: str
    pay_com: str
    start_parameter: str
    logo: str


@dataclass
class Db:
    db_user: str
    db_password: str
    db_database: str
    db_host: str
    db_port: int


@dataclass
class Settings:
    bots: Bots
    contacts: Contacts
    company: Company
    wallet: Wallet
    db: Db


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str('TOKEN')
        ),
        contacts=Contacts(
            phone=env.str('PHONE'),
            manager=env.str('MANAGER_LINK'),
            group=env.str('GROUP')
        ),
        company=Company(
            name=env.str('COMPANY_NAME'),
            site=env.str('COMPANY_WEBSITE')
        ),
        wallet=Wallet(
            click=env.str('CLICK'),
            pay_com=env.str('PAY_COM'),
            start_parameter=env.str('START_PARAMETER'),
            logo=env.str('LOGO'),
        ),
        db=Db(
            db_user=env.str('DB_USER'),
            db_password=env.str('DB_PASSWORD'),
            db_database=env.str('DB_DATABASE'),
            db_host=env.str('DB_HOST'),
            db_port=env.int('DB_PORT')
        )
    )


settings = get_settings('input')
