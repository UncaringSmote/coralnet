from config import folder_to_use
from generate_json import generate_json
from state import StateMachine
import logging

logging.basicConfig()
state_machine = StateMachine(folder_to_use)
generate_json(state_machine)
