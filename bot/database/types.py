from dataclasses import dataclass
from typing import Union


@dataclass
class User:
    id: int
    chat_id: int


@dataclass
class Url:
    id: int
    title: str
    url: str


@dataclass
class UserUrl:
    id: int
    user_id: int  # User.id
    url_id: int  # Url.id
    tags: str
    lastupdate: Union[str, None]
    max_news: int


@dataclass
class Timer:
    id: int
    chat_id: int
    timer: str


@dataclass
class Config:
    id: int
    chat_id: int
    max_news: int


@dataclass
class Session:
    chat_id: int
    control_id: int
    started: int


@dataclass
class Style:
    chat_id: int
    title: Union[str, None]
    hour_and_services: Union[str, None]
    description: Union[str, None]


@dataclass
class Error:
    message: str


@dataclass
class Service:
    url_id: int
    title: str
    url: str
    tags: str
    max_news: int
    lastUpdate: Union[str, None]
