from dataclasses import dataclass, asdict
from abc import ABC
from typing import Optional, Any, Dict, Set


@dataclass
class AbstractModel(ABC):
    """
    Base model, from which any domain model should be inherited.
    """

    async def to_dict(
            self,
            exclude: Optional[Set[str]] = None,
            include: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        """
        Create a dictionary representation of the model.

        exclude: set of model fields, which should be excluded from dictionary representation.
        include: set of model fields, which should be included into dictionary representation.
        """

        data: Dict[str, Any] = asdict(self)
        if exclude:
            for key in exclude:
                try:
                    del data[key]
                except KeyError:
                    pass

        if include:
            data.update(include)

        return data
