from random import choice

from action import Action
from action_strategy import ActionStrategy
from orientation import Orientation
from state import State


class Agent:
    def __init__(
        self,
        position: tuple[int, int] = (0, 0),
        orientation: Orientation = Orientation.UP,
        allowed_actions: list[Action] = [Action.NOTHING],
        action_strategy: ActionStrategy = ActionStrategy.FROZEN,
        agent_callback=None,
        action_callback=None,
    ) -> None:
        self.allowed_actions = allowed_actions
        self.action_strategy = action_strategy
        self.position = position
        self.orientation = orientation
        self._agent_callback = agent_callback
        self._action_callback = action_callback

    def __repr__(self):
        return f"Agent[Pos: {self.position}, Dir: {self.orientation.name}]"

    def __str__(self):
        return self.__repr__()

    def _is_action_legal(self, state: State, action: Action) -> bool:
        return True

    def _filter_legal_actions(self, state: State) -> list[Action]:
        return filter(
            lambda action: self._is_action_legal(state, action), self.allowed_actions
        )

    def _action_strategy(self, state: State) -> Action:
        actions = list(self._filter_legal_actions(state))
        if len(actions) == 0:
            return Action.NOTHING

        match self.action_strategy:
            case ActionStrategy.RANDOM:
                return choice(actions)
            case _:
                return Action.NOTHING

    def _resultant_position_and_orientation(
        self, action: Action
    ) -> list[tuple[int, int], tuple[int, int]]:
        if action == Action.NOTHING:
            return [self.position, self.orientation]

        candidate_position = self.position
        candidate_orientation = self.orientation

        if (action & action.TURN_LEFT) == Action.TURN_LEFT:
            match self.orientation:
                case Orientation.UP:
                    candidate_orientation = Orientation.LEFT
                case Orientation.RIGHT:
                    candidate_orientation = Orientation.UP
                case Orientation.DOWN:
                    candidate_orientation = Orientation.RIGHT
                case Orientation.LEFT:
                    candidate_orientation = Orientation.DOWN

        elif (action & action.TURN_RIGHT) == Action.TURN_RIGHT:
            match self.orientation:
                case Orientation.UP:
                    candidate_orientation = Orientation.RIGHT
                case Orientation.RIGHT:
                    candidate_orientation = Orientation.DOWN
                case Orientation.DOWN:
                    candidate_orientation = Orientation.LEFT
                case Orientation.LEFT:
                    candidate_orientation = Orientation.UP

        # FORWARD is intentionally after TURN_...
        # so that TURN_X_AND_MOVE flags can work
        if (action & action.FORWARD) == Action.FORWARD:
            (x, y), (dx, dy) = candidate_position, candidate_orientation.value
            candidate_position = (x + dx, y + dy)

        return [candidate_position, candidate_orientation]

    def act(self, state: State):
        action = self._action_strategy(state)
        if self._action_callback != None:
            self._action_callback(action)

        new_position, new_orientation = self._resultant_position_and_orientation(action)
        if state.record_move(new_position):
            self.position = new_position
            self.orientation = new_orientation

        if self._agent_callback != None:
            self._agent_callback(self)
