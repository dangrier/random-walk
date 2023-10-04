from enum import IntFlag, auto


class Action(IntFlag):
    NOTHING = auto()
    FORWARD = auto()
    TURN_LEFT = auto()
    TURN_RIGHT = auto()
    TURN_LEFT_AND_MOVE = TURN_LEFT | FORWARD
    TURN_RIGHT_AND_MOVE = TURN_RIGHT | FORWARD
