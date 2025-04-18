import html
from enum import Enum, IntEnum
from typing import TypeVar, Generic, List, Optional, Dict, Any

from pydantic import BaseModel, Field, AliasChoices

Payload = TypeVar('Payload')
Details = TypeVar('Details')


class ResponseStatus(str, Enum):
    OK = "ok"
    ERROR = "error"


class Emoji(str, Enum):
    OK = "✅"
    ERR = "❌"
    ARROW_UP = "⬆️"
    ARROW_DOWN = "⬇️"
    PIN = "📌"
    PHONE = "📱"
    TRIANGE_UP = "🔼"
    TRIANGE_DOWN = "🔽"
    PEOPLE = "👤"
    LATENCY = "📶"
    TIME = "⏰"
    COMPUTER = "🖥"
    TRAFFIC_LIGHTS = "🚦"
    SHRUG = "🤷‍♂️"
    INFO = "ℹ️"
    SHIELD = "🛡"
    KEY = "🔑"
    MAP = "🗺"
    GAME = "🎮"

    def __str__(self):
        return self.value


class ErrorCodes(IntEnum):
    ConnectError = 1
    ICMPHostNotAlive = 2
    InvalidHostname = 3


class Error(BaseModel):
    message: str
    code: ErrorCodes

    def __str__(self):
        return f"{Emoji.ERR} {self.message}"


class ToI18nParamsModel(BaseModel):

    def get_i18n_params(self) -> dict[str, Any]:
        raise NotImplementedError


class HttpCheckerResponse(ToI18nParamsModel):
    status_code: int
    time: float

    def __str__(self):
        return f"{HTTP_EMOJI.get(self.status_code // 100, '')} " \
               f"{self.status_code}, {Emoji.TIME} {self.time * 1000:.2f}ms"

    def get_i18n_params(self):
        return {
            "status_emoji": HTTP_EMOJI.get(self.status_code // 100, ''),
            "status_code": self.status_code,
            "time": f"{self.time * 1000:.2f}"
        }


class ICMPCheckerResponse(ToI18nParamsModel):
    min_rtt: float
    avg_rtt: float
    max_rtt: float
    packets_sent: int
    packets_received: int

    def __str__(self):
        return f"{Emoji.OK} {self.min_rtt}/{self.max_rtt}/{self.avg_rtt} " \
               f"{Emoji.ARROW_UP}{self.packets_sent} ️{Emoji.ARROW_DOWN}{self.packets_received}"

    def get_i18n_params(self) -> dict[str, Any]:
        return {
            "min_rtt": self.min_rtt,
            "max_rtt": self.max_rtt,
            "avg_rtt": self.avg_rtt,
            "packets_sent": self.packets_sent,
            "packets_received": self.packets_received
        }


class ICMPDetails(ToI18nParamsModel):
    jitter: float
    rtts: List[float]
    loss: float

    def get_rtts(self) -> str:
        return str.join(" \n", map(str, self.rtts))

    def __str__(self):
        rtts = self.get_rtts()
        return f"{Emoji.LATENCY} Round-trip time: \n{rtts}\n" \
               f"{Emoji.LATENCY} Jitter: {self.jitter}\n" \
               f"{Emoji.LATENCY} Loss: {self.loss}"

    def get_i18n_params(self) -> dict[str, Any]:
        return {
            "rtts": self.get_rtts(),
            "jitter": self.jitter,
            "loss": self.loss
        }


class MinecraftResponse(ToI18nParamsModel):
    latency: float

    def __str__(self):
        return f"{Emoji.OK} {Emoji.LATENCY}{self.latency}ms"

    def get_i18n_params(self) -> dict[str, Any]:
        return {
            "latency": self.latency
        }


class MinecraftDetails(ToI18nParamsModel):
    version: str
    protocol: int
    max_players: int
    online: int
    port: Optional[int]

    def __str__(self):
        message = f"{Emoji.COMPUTER} Версия ядра: {self.version}\n" \
                  f"{Emoji.TRAFFIC_LIGHTS} Протокол: {self.protocol}\n" \
                  f"{Emoji.PEOPLE} Онлаин: {self.online}/{self.max_players}"
        if self.port:
            message += f"\n{Emoji.OK} Порт: {self.port}"
        return message

    def get_i18n_params(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "protocol": self.protocol,
            "online": self.online,
            "max_players": self.max_players,
            "port": self.port if self.port else 0
        }


class PortResponse(ToI18nParamsModel):
    open: bool

    def __str__(self):
        return f"{Emoji.OK if self.open else Emoji.ERR}"

    def get_i18n_params(self) -> dict[str, Any]:
        return {
            "open": f"{Emoji.OK if self.open else Emoji.ERR}"
        }


class PortDetails(ToI18nParamsModel):
    service: str

    def __str__(self):
        if self.service != "Неизвестно":
            return f"{Emoji.PHONE} Скорее всего на этом порту располагается сервис {self.service}"
        else:
            return f"{Emoji.SHRUG} На этом порту неизвестный сервис"

    def get_i18n_params(self) -> dict[str, Any]:
        return {
            "service": self.service,
            "available": 1 if self.service else 0
        }


class SourceServerResponse(ToI18nParamsModel):
    ping: float

    def __str__(self):
        return f"{Emoji.OK} {Emoji.LATENCY} {round(self.ping * 1000)}ms"

    def get_i18n_params(self) -> dict[str, Any]:
        return {
            "ping": round(self.ping * 1000)
        }


class SourceServerPlayer(BaseModel):
    name: str
    score: int
    duration: float


class SourceServerDetails(ToI18nParamsModel):
    protocol: int
    server_name: str
    map_name: str
    player_count: int
    max_players: int
    password_protected: bool
    vac_enabled: bool
    version: str
    game: str
    steam_id: Optional[int]
    players: List[SourceServerPlayer]
    rules: Optional[Dict]

    def __str__(self):
        return f"{Emoji.OK} <b>{html.escape(self.server_name)}</b>\n" \
               f"{Emoji.GAME} Игра: {self.game}\n" \
               f"{Emoji.MAP} Карта: {self.map_name}\n" \
               f"{Emoji.PEOPLE} Игроки: {self.player_count}/{self.max_players}\n" \
               f"{Emoji.COMPUTER} Версия: {self.version}\n" \
               f"{Emoji.SHIELD} {'Сервер защищен VAC' if self.vac_enabled else 'Сервер без VAC'}\n" \
               f"{Emoji.KEY} {'Сервер защищен паролем' if self.password_protected else 'Сервер без пароля'}\n" \
               f"{Emoji.INFO} STEAM ID: {self.steam_id}\n"

    def get_i18n_params(self) -> dict[str, Any]:
        return {
            "server_name": self.server_name,
            "game": self.game,
            "map_name": self.map_name,
            "player_count": self.player_count,
            "max_players": self.max_players,
            "version": self.version,
            "vac_enabled": 1 if self.vac_enabled else 0,
            "password_protected": 1 if self.password_protected else 0,
            "steam_id": self.steam_id
        }


# SPT Aki


class SPTConfig(BaseModel):
    backend_url: str = Field(validation_alias=AliasChoices("backendUrl", "backend_url"))
    name: str
    editions: list[str]


class SPTMod(BaseModel):
    name: str
    version: str
    author: str
    license: str

    def __str__(self) -> str:
        return f"- {self.name}: {self.version}"


class SPTResponse(ToI18nParamsModel):
    ok: bool = True

    def __str__(self):
        return f"{Emoji.OK} Сервер доступен"

    def get_i18n_params(self) -> dict[str, Any]:
        return {
            "ok": 1
        }


class SPTDetails(ToI18nParamsModel):
    aki_version: str
    game_version: str
    config: SPTConfig
    mods: list[SPTMod]

    def get_formatted_mods(self) -> str:
        return "\n".join(map(str, self.mods))

    def __str__(self):
        return (
            f"{Emoji.COMPUTER} Сервер {self.config.name}"
            f"{Emoji.COMPUTER} Версия AKI: {self.aki_version}\n"
            f"{Emoji.GAME} Версия игры: {self.game_version}\n\n"
            
            f"{Emoji.INFO} Моды:\n"
            f"{self.get_formatted_mods()}"
        )

    def get_i18n_params(self) -> dict[str, Any]:
        return {
            "name": self.config.name,
            "aki_version": self.aki_version,
            "game_version": self.game_version,
            "formatted_mods": self.get_formatted_mods()
        }

# Vintage Story


class VintageStoryResponse(ToI18nParamsModel):
    ok: bool = True

    def __str__(self):
        return f"{Emoji.OK} Сервер доступен"

    def get_i18n_params(self) -> dict[str, Any]:
        return {
            "ok": 1
        }


class VSMod(BaseModel):
    id: str
    version: str

    def __str__(self):
        return f"- {self.id}: {self.version}"


class VSPlayStyle(BaseModel):
    id: str
    lang_code: str = Field(alias="langCode")


class VintageStoryDetails(ToI18nParamsModel):
    server_name: str = Field(validation_alias=AliasChoices("serverName", "server_name"))
    server_ip: str = Field(validation_alias=AliasChoices("serverIP", "server_ip"))
    mods: list[VSMod]
    max_players: int = Field(validation_alias=AliasChoices("maxPlayers", "max_players"))
    players: int
    game_version: str = Field(validation_alias=AliasChoices("gameVersion", "game_version"))
    has_password: bool = Field(validation_alias=AliasChoices("hasPassword", "has_password"))
    whitelisted: bool
    game_description: str = Field(
        validation_alias=AliasChoices("gameDescription", "game_description")
    )

    def get_i18n_params(self) -> dict[str, Any]:
        return {
            "server_name": self.server_name,
            "server_ip": self.server_ip,
            "players": self.players,
            "max_players": self.max_players,
            "version": self.game_version,
            "whitelisted": 1 if self.whitelisted else 0,
            "has_password": 1 if self.has_password else 0,
        }


class Response(BaseModel, Generic[Payload]):
    status: ResponseStatus
    payload: Payload
    details: Optional[Details] = Field(default=None)


HTTP_EMOJI = {
    2: "✅",
    3: "➡️",
    4: "🔍",
    5: "❌️",
}

COUNTRY_EMOJI = {
    "russia": "🇷🇺",
    "ukraine": "🇺🇦",
    "luxembourg": "🇱🇺",
    "france": "🇫🇷",
    "canada": "🇨🇦",
    "usa": "🇺🇸",
    "germany": "🇩🇪",
    "netherlands": "🇳🇱",
    "finland": "🇫🇮",
    "england": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "switzerland": "🇨🇭",
    "india": "🇮🇳",
    "australia": "🇦🇺",
    "saudi arabia": "🇸🇦",
    "georgia": "🇬🇪",
    "lithuania": "🇱🇹",
    "sweden": "🇸🇪",
    "poland": "🇵🇱",
    "bulgaria": "🇧🇬",
    "moldova": "🇲🇩"
}
