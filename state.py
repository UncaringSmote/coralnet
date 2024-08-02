import json
from dataclasses import dataclass
from typing import Dict
from pathlib import Path
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class State:
    lastK: int = 0
    maxK: int = -1
    deploy_completed: bool = False
    coralnet_load_file: str = None


@dataclass_json
@dataclass
class StateData:
    states: Dict[str, State]


class StateMachine:
    def __init__(self, current_folder):
        self._get_states()
        self.current_folder = current_folder
        if not self.state_data.states.get(current_folder):
            self.state_data.states[current_folder] = State()
            self._save_states()

    def _get_states(self):
        with open(f"states.json", "r+") as f:
            self.state_data = StateData.from_dict(json.load(f))

    def _save_states(self):
        with open(f'states.json', 'w') as outfile:
            json.dump(self.state_data.to_dict(), outfile)

    def get_state(self) -> State:
        return self.state_data.states[self.current_folder]

    def update_state(self, state: State):
        self.state_data.states[self.current_folder] = state
        self._save_states()
