from iconservice import *
from .custom import RandomClass

TAG = 'DiceScore'

class DiceScore(IconScoreBase):

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)

    def on_install(self) -> None:
        super().on_install()

    def on_update(self) -> None:
        super().on_update()
    
    @external(readonly=True)
    def diceRoll(self, name: str) -> int:
        return RandomClass(name, self.block.timestamp).get_random()