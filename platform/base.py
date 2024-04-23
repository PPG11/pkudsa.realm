from collections import namedtuple


Action = namedtuple("Action", "id mdx mdy adx ady")
# action = Action(id="R", mdx=0, mdy=0, adx=1, ady=0)


class Chess:
    """
              |  AP |   HP |
    Warrior   | 400 |  800 |
    Shooter   | 500 |  400 |
    Protecter | 200 | 1800 |
    Commander |   - | 2000 |
    """

    def __init__(self):
        self.id = "C"  # Chees ID: ["W", "S", "P", "C"]
        self.hp = 100
        self.side = "W"  # ["W", "E"]
        self.pos = (0, 0)


class Board:
    def __init__(self):
        self.layout = [[None] * 8 for _ in range(8)]
        self.my_side = "W"
        self.my_storage = dict()  # 跨turn存储，字典
        self.total_turn = 60
        self.turn_number = 0  # current turn, [0, total_turn-1]
        self.point = {
            "W": (2000, 3000),
            "E": (2000, 3000),
        }  # current score: (Commander.HP, Total.HP)
        self.action_history = []
