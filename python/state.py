BOTTOM_LEFT = 0
TOP_RIGHT = 1
X = 0
Y = 1


class State:
    def __init__(self, step_callback=None):
        self._bounds = ((0, 0), (0, 0))
        self._moves = {}
        self._step_callback = step_callback

    def __repr__(self):
        return f"State[Bounds: {self._bounds}, Moves: {self._moves}]"

    def __str__(self):
        return self.__repr__()

    def bounds(self):
        return self._bounds

    def record_move(self, position: tuple[int, int]) -> bool:
        self._moves.setdefault(position, 0)
        self._moves[position] += 1

        (bounds_x1, bounds_y1), (bounds_x2, bounds_y2) = self._bounds
        if position[X] < bounds_x1:
            bounds_x1 = position[X]
        if position[X] > bounds_x2:
            bounds_x2 = position[X]
        if position[Y] < bounds_y1:
            bounds_y1 = position[Y]
        if position[Y] > bounds_y2:
            bounds_y2 = position[Y]
        self._bounds = ((bounds_x1, bounds_y1), (bounds_x2, bounds_y2))

        if self._step_callback != None:
            self._step_callback(self)

        return True
