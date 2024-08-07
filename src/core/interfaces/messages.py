from typing import Union

from src.core.interfaces.events import AbstractEvent
from src.core.interfaces.commands import AbstractCommand


Message = Union[AbstractEvent, AbstractCommand]
