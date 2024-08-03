import json
from dataclasses import dataclass
from typing import Dict, Optional
from pathlib import Path
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class State:
    dropbox_path: str
    lastK: int = 0
    maxK: int = -1
    deploy_completed: bool = False
    error_checking_completed: bool = False
    csv_generated: bool = False
    coralnet_load_file: Optional[str] = None
    deploy_result_file: Optional[str] = None



@dataclass_json
@dataclass
class StateData:
    states: Dict[str, State]


class StateMachine:
    def __init__(self, dropbox_path):
        self._get_states()
        self.current_id = '-'.join(dropbox_path.split('/')[1:])
        self.dropbox_path = dropbox_path
        if not self.state_data.states.get(self.current_id):
            self.state_data.states[self.current_id] = State(dropbox_path)
            self._save_states()

    def _get_states(self):
        with open(f"states.json", "r+") as f:
            self.state_data = StateData.from_dict(json.load(f))

    def _save_states(self):
        with open(f'states.json', 'w') as outfile:
            json.dump(self.state_data.to_dict(), outfile)

    def get_state(self) -> State:
        return self.state_data.states[self.current_id]

    def update_state(self, state: State):
        self.state_data.states[self.current_id] = state
        self._save_states()
