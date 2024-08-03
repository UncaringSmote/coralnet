import json
import logging
import re
import time
from dataclasses import dataclass

from logdecorator import log_on_start, log_on_end

from config import image_extension
from coralnet_load_model import CoralnetLoadModel
from deploy_coralnet_api import send_coralnet_post, get_result, seperate_errors
from generate_json import generate_model_json
from state import StateMachine

logger = logging.getLogger()

@dataclass
class FileName:
    name:str

@log_on_start(logging.INFO, "+ Started error checking for {state_machine.dropbox_path}")
@log_on_end(logging.INFO, "- Finished error checking for {state_machine.dropbox_path}")
def handle_errors(state_machine: StateMachine, files_per_load= 100):
    state = state_machine.get_state()
    if state.error_checking_completed:
        return

    with open(state.deploy_result_file, 'r') as outfile:
        results = json.load(outfile)

    errors = results['errors']
    if len(errors) == 0:
        state.error_checking_completed = True
        state_machine.update_state(state)

    file_list = []
    id_index_mapping = {}
    for i,error in enumerate(errors):
        file_name = get_file_name(error)
        file_list.append(FileName(file_name))
        id_index_mapping[file_name] = i

    model = generate_model_json(file_list, state_machine.dropbox_path)

    successes_combined,errors_combined = [],[]

    for k in range(0,len(errors),files_per_load):
        logger.info(f'K = {k}')

        batch_to_load = CoralnetLoadModel(model.data[k:k+files_per_load])
        post_response = send_coralnet_post(batch_to_load.to_dict())
        time.sleep(60)  # Waits 60 seconds before attempting to retrieve results from the post request
        result = get_result(post_response.headers['Location'])
        successes,errors = seperate_errors(result)

        successes_combined.extend(successes)
        errors_combined.extend(errors)

    results['successes'].extend(successes_combined)
    results['errors']=errors_combined
    with open(state.deploy_result_file, 'w') as outfile:
        json.dump(results, outfile)

    if len(errors_combined)>0:
        logger.error("STILL HAS ERRORS, Check following reasons")
        for error in errors:
            logger.error(f"{error}")
    else:
        logger.error("A - OKAY")
        state.error_checking_completed = True
        state_machine.update_state(state)

def get_file_name(response):
    return re.search(f'^.*[/](.*.{image_extension})', response['id']).group(1)
