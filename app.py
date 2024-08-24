import os
import sys

from config import dropbox_paths, SITE
from deploy_coralnet_api import deploy_coralnet_api
from generate_final_csv import generate_final_csv
from generate_json import generate_json
from handle_errors import handle_errors
from state import StateMachine
import logging

from utils import make_output_directory

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)8s]:  %(message)s',
    handlers=[
        logging.FileHandler(f'{os.path.basename(__file__)}.log'),
        logging.StreamHandler(sys.stdout),
    ])
for path in dropbox_paths:
    if SITE not in path:
        raise Exception("SITE MAY NOT MATCH CORALNET ALGO")
    state_machine = StateMachine(path)
    make_output_directory(state_machine.current_id)
    generate_json(state_machine)
    deploy_coralnet_api(state_machine)
    handle_errors(state_machine)
    generate_final_csv(state_machine)