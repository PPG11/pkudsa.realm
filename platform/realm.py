from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Tuple, List, Dict, Optional
import utils
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
    def __init__(self, _id: str, _hp: int, _ap: int):
        assert _id in ChessTypeDict, f"unknown chess type: [{_id}]"

        self.id: ChessType = ChessTypeDict[_id]
        self.hp_max: int = _hp
        self.hp: int = _hp
        self.ap: int = _ap
        self.side: Optional[PlayerSide] = None
        self.pos: Optional[Tuple[int, int]] = None
        self.commander_ref: Optional[ChessBase] = None

    @abstractmethod
    def init_side(self, _side: str):
        pass

    def recover(self, _chess_hp: int, _commander_hp: int, _is_commander: bool = False):
        self.hp += _chess_hp
        if not _is_commander:
            self.hp = self.hp_max if self.hp > self.hp_max else self.hp
            assert self.commander_ref is not None
            self.commander_ref.recover(_commander_hp, 0, True)

    def move(self, mdx: int, mdy: int):
        self.move_check(mdx, mdy)
        pass

    def attact(self, adx: int, ady: int):
        self.attact(adx, ady)
        pass

    @abstractmethod
    def move_check(self, mdx: int, mdy: int) -> bool:
        pass

    @abstractmethod
    def attact_check(self, adx: int, ady: int) -> bool:
        pass


class Warrior(ChessBase):
    def __init__(self, _side: str):
        super().__init__("W", 800, 400)
        self.init_side(_side)

    def init_side(self, _side: str):
        assert _side in ["W", "E"], f"unknown side: {_side}"
        if _side == "W":
            self.side = PlayerSide.W
            self.pos = (0, 1)
        elif _side == "E":
            self.side = PlayerSide.E
            self.pos = (7, 6)

    def move_check(self, mdx: int, mdy: int) -> bool:
        return (utils.abs(mdx) + utils.abs(mdy)) <= 2

    def attact_check(self, adx: int, ady: int) -> bool:
        return (utils.abs(adx) + utils.abs(ady)) <= 1


class Shooter(ChessBase):
    def __init__(self, _side: str):
        super().__init__("S", 400, 500)
        self.init_side(_side)

    def init_side(self, _side: str):
        assert _side in ["W", "E"], f"unknown side: {_side}"
        if _side == "W":
            self.side = PlayerSide.W
            self.pos = (1, 0)
        elif _side == "E":
            self.side = PlayerSide.E
            self.pos = (6, 7)

    def move_check(self, mdx: int, mdy: int) -> bool:
        return (utils.abs(mdx) + utils.abs(mdy)) <= 1

    def attact_check(self, adx: int, ady: int) -> bool:
        return (utils.abs(adx) + utils.abs(ady)) <= 2


class Protecter(ChessBase):
    def __init__(self, _side: str):
        super().__init__("P", 1800, 200)
        self.init_side(_side)

    def init_side(self, _side: str):
        assert _side in ["W", "E"], f"unknown side: {_side}"
        if _side == "W":
            self.side = PlayerSide.W
            self.pos = (1, 1)
        elif _side == "E":
            self.side = PlayerSide.E
            self.pos = (6, 6)

    def move_check(self, mdx: int, mdy: int) -> bool:
        return (utils.abs(mdx) + utils.abs(mdy)) <= 1

    def attact_check(self, adx: int, ady: int) -> bool:
        return (utils.abs(adx) <= 1) and (utils.abs(ady) <= 1)


class Commander(ChessBase):
    def __init__(self, _side: str):
        super().__init__("C", 2000, 0)
        self.init_side(_side)

    def init_side(self, _side: str):
        assert _side in ["W", "E"], f"unknown side: {_side}"
        if _side == "W":
            self.side = PlayerSide.W
            self.pos = (0, 0)
        elif _side == "E":
            self.side = PlayerSide.E
            self.pos = (7, 7)

    def move_check(self, mdx: int, mdy: int) -> bool:
        return False

    def attact_check(self, adx: int, ady: int) -> bool:
        return False


class Game:
    def __init__(self):
        self.layout: List[List[Optional[ChessBase]]] = [[None] * 8 for _ in range(8)]
        self.next_side: PlayerSide = PlayerSide.W
        self.total_turn: int = 60
        self.turn_number: int = 0  # current turn, [0, total_turn-1]
        self.point: Dict[PlayerSide, Tuple[int, int]] = {
            "W": (2000, 3000),
            "E": (2000, 3000),
        }  # current score: (Commander.HP, Total.HP)
        self.action_history: List[Tuple] = []  # (E/W, Chess, mdx, mdy, adx, ady)

        self.recover_range: list[Tuple] = [
            (3, 3),
            (3, 4),
            (4, 3),
            (4, 4),
        ]
        self.recover_chess: int = 50
        self.recover_commander: int = 20

    def turn_recover(self):
        for x, y in self.recover_range:
            chess = self.layout[x][y]
            if chess is not None:
                chess.recover(self.recover_chess, self.recover_commander, False)
