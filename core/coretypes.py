from enum import Enum, IntEnum
from typing import TypeVar, Generic, List

from pydantic import BaseModel
from pydantic.generics import GenericModel

Payload = TypeVar('Payload')


class ResponseStatus(str, Enum):
    OK = "ok"
    ERROR = "error"


class ErrorCodes(IntEnum):
    ConnectError = 1
    ICMPHostNotAlive = 2
    InvalidHostname = 3


class Error(BaseModel):
    message: str
    code: ErrorCodes


class HttpCheckerResponse(BaseModel):
    status_code: int
    time: float


class ICMPCheckerResponse(BaseModel):
    jitter: float
    rtts: List[float]
    min_rtt: float
    avg_rtt: float
    max_rtt: float
    packets_sent: int
    packets_received: int
    loss: float


class MinecraftResponse(BaseModel):
    latency: float
    max_players: int
    online: int
    version: str
    protocol: int


class PortResponse(BaseModel):
    open: bool
    service: str


class Response(GenericModel, Generic[Payload]):
    status: ResponseStatus
    payload: Payload


class APINode(BaseModel):
    address: str
    token: str


HTTP_EMOJI = {
    2: "✅",
    3: "➡️",
    4: "🔍",
    5: "❌️",
}
