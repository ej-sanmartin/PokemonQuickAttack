from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class TypeList:
    '''List of pokemon types.'''

    types: List[str]
