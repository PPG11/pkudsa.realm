from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Tuple

# from base import Action, Chess, Board


class ChessType(Enum):
    Warrior = auto()
    Shooter = auto()
    Protecter = auto()
    Commander = auto()


ChessTypeDict = {
    "W": ChessType.Warrior,
    "S": ChessType.Shooter,
    "P": ChessType.Protecter,
    "C": ChessType.Commander,
}


class PlayerSide(Enum):
    W = auto()
    E = auto()


class ChessBase(ABC):
    def __init__(self, _id: str):
        assert _id in ChessTypeDict, f"unknown chess type: [{_id}]"
        self.id: ChessType = ChessTypeDict[_id]
        self.hp: int = -1
        self.side: PlayerSide = PlayerSide.W
        self.pos: Tuple[int, int] = (-1, -1)
        self.ap: int = -1

    @abstractmethod
    def move(self, mdx: int, mdy: int):
        pass

    @abstractmethod
    def attact(self, adx: int, ady: int):
        pass


class Warrior(ChessBase):
    pass


class Shooter(ChessBase):
    pass


class Protecter(ChessBase):
    pass


class Commander(ChessBase):
    pass
