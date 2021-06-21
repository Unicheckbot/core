from enum import Enum, IntEnum
from typing import TypeVar, Generic, List, Optional

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

Payload = TypeVar('Payload')
Details = TypeVar('Details')


class ResponseStatus(str, Enum):
    OK = "ok"
    ERROR = "error"


class Emoji(str, Enum):

    OK = "✅"
    ERR = "❌"
    ARROW_UP = "⬆"
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


class HttpCheckerResponse(BaseModel):
    status_code: int
    time: float

    def __str__(self):
        return f"{HTTP_EMOJI.get(self.status_code // 100, '')} " \
               f"{self.status_code}, {Emoji.TIME} {self.time * 1000:.2f}ms"


class ICMPCheckerResponse(BaseModel):
    min_rtt: float
    avg_rtt: float
    max_rtt: float
    packets_sent: int
    packets_received: int

    def __str__(self):
        return f"{Emoji.OK} {self.min_rtt}/{self.max_rtt}/{self.avg_rtt} " \
               f"{Emoji.ARROW_UP}{self.packets_sent} ️{Emoji.ARROW_DOWN}️{self.packets_received} ." \



class ICMPDetails(BaseModel):
    jitter: float
    rtts: List[float]
    loss: float

    def __str__(self):
        return f"{Emoji.LATENCY} Round-trip time: {','.join(map(str, self.rtts))}\n" \
               f"{Emoji.LATENCY} Jitter: {self.jitter}\n" \
               f"Loss: {self.loss}"


class MinecraftResponse(BaseModel):
    latency: float
    max_players: int
    online: int

    def __str__(self):
        return f"{Emoji.OK} {Emoji.PEOPLE}{self.online}/{self.max_players} {Emoji.LATENCY}{self.latency}ms"


class MinecraftDetails(BaseModel):
    version: str
    protocol: int
    port: Optional[int]

    def __str__(self):
        message = f"{Emoji.COMPUTER} Версия: {self.version}\n" \
                  f"{Emoji.TRAFFIC_LIGHTS} Протокол: {self.protocol}\n"
        if self.port:
            message += f"{Emoji.OK} Порт: {self.port}"


class PortResponse(BaseModel):
    open: bool

    def __str__(self):
        return f"{Emoji.OK if self.open else Emoji.ERR}"


class PortDetails(BaseModel):
    service: str

    def __str__(self):
        if self.service != "Неизвестно":
            return f"{Emoji.PHONE} Скорее всего на этом порту располагается сервис {self.service}"
        else:
            return f"{Emoji.SHRUG} На этом порту неизвестный сервис"


class Response(GenericModel, Generic[Payload]):
    status: ResponseStatus
    payload: Payload
    details: Optional[Details] = Field(default=None)


class APINode(BaseModel):
    address: str
    token: str


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
}
