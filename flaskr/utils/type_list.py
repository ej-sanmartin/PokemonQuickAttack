from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class TypeList:
    '''List of pokemon types.'''

    # List of types.
    types: List[str]
