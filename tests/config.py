from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class BaseTestConfig:

    def to_dict(self, to_lower: bool = False) -> Dict[str, Any]:
        base_dict: Dict[str, Any] = asdict(self)
        if to_lower:
            return {k.lower(): v for k, v in base_dict.items()}

        return base_dict


@dataclass
class FakeUserConfig(BaseTestConfig):
    EMAIL: str = 'test@yandex.ru'
    PASSWORD: str = 'test_password'
    USERNAME: str = 'test_username'
