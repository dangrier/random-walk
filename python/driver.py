import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from action import Action
from action_strategy import ActionStrategy
from agent import Agent
from state import State
from tqdm import tqdm

ALLOWED_ACTIONS = [
    Action.FORWARD,
    Action.TURN_LEFT_AND_MOVE,
    Action.TURN_RIGHT_AND_MOVE,
]
STRATEGY = ActionStrategy.RANDOM


def state_print(state: State):
    print(state)


def action_print(action: Action):
    print(action.name)


def agent_print(agent: Agent):
    print(agent)


def drive_scenario(max_steps=10):
    agent = Agent(
        allowed_actions=ALLOWED_ACTIONS, action_strategy=STRATEGY
    )  # , action_callback=action_print, agent_callback=agent_print)
    state = State()  # step_callback=state_print)

    for i in tqdm(range(max_steps)):
        agent.act(state)

    df = pd.DataFrame(
        [(item[0][0], item[0][1], item[1]) for item in state._moves.items()],
        columns=["x", "y", "count"],
    )

    print(df)
    sns.scatterplot(data=df, x="x", y="y", size="count")
    plt.scatter(x=0, y=0, s=72, marker="x", color="r")
    plt.show()


if __name__ == "__main__":
    drive_scenario(1_000_000)
