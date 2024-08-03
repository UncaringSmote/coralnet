import json
import logging
import random
from typing import List

import dropbox
from dropbox import Dropbox
from dropbox.sharing import PathLinkMetadata
from logdecorator import log_on_start, log_on_end

from config import dropbox_token
from coralnet_load_model import Point, Attributes, Data, CoralnetLoadModel
from state import StateMachine
from utils import generate_save_location

requests_logger = logging.getLogger('dropbox')
requests_logger.setLevel(logging.WARN)#done to hide the dropbox spam messages
logger = logging.getLogger(__name__)
dbx = dropbox.Dropbox(dropbox_token)
dbx.users_get_current_account()

def get_points_array(r_min=450, r_max=2550, c_min=600, c_max=3400, r_divs=5, c_divs=6) -> List[Point]:
    r_space = (r_max - r_min) / r_divs
    c_space = (c_max - c_min) / c_divs
    points = []
    for r in range(r_divs):
        for c in range(c_divs):
            rl = round(r_min + r * r_space)
            rr = round(r_min + (r + 1) * r_space)
            cl = round(c_min + c * c_space)
            cr = round(c_min + (c + 1) * c_space)
            points.append(
                Point(
                    random.randint(rl, rr),
                    random.randint(cl, cr)
                )
            )
    return points


def generate_data_json(shared_link: PathLinkMetadata) -> Data:
    points = get_points_array()
    return Data(
        Attributes(
            shared_link.url[:-1] + '1',
            points
        )
    )


@log_on_start(logging.INFO, "+ Started Generating Model JSON")
@log_on_end(logging.INFO, "- Finished Generating Model JSON")
def generate_model_json(file_list: List[any], dropbox_folder: str) -> CoralnetLoadModel:
    data = []
    increments = [(len(file_list) // 10) * i for i in range(1, 10)]
    for i, entry in enumerate(file_list):
        pathway = f'{dropbox_folder}/' + entry.name
        tmp_name = dbx.sharing_create_shared_link(path=pathway, short_url=False, pending_upload=None)
        data.append(generate_data_json(tmp_name))
        if i in increments:
            logger.info(f"Percent Complete: {((increments.index(i) + 1) * 10)}")
    return CoralnetLoadModel(data)


@log_on_start(logging.INFO, "+ Started getting File List")
@log_on_end(logging.INFO, "- Finished getting File List")
def get_file_list(dropbox_folder: str) -> List[any]:
    # Creates empty list to store the file names within the folder of interest
    file_list = []

    # Pulls out first 2000 files from the folder, adds the names to file_list, then creates a cursor
    # signifying its end location in the folder
    file_list_result = dbx.files_list_folder(dropbox_folder)
    file_list.extend(file_list_result.entries)
    while file_list_result.has_more:  # Loops through to retrieve the rest of the images
        file_list_result = get_more_files(file_list, file_list_result)
    return file_list


@log_on_start(logging.INFO, f"Loading More Files")
def get_more_files(file_list, file_list_result):
    file_list_result = dbx.files_list_folder_continue(file_list_result.cursor)
    file_list.extend(file_list_result.entries)
    return file_list_result


@log_on_start(logging.INFO, "+ Started Saving Model")
@log_on_end(logging.INFO, "- Finished Saving Model")
def save_model(state_id, model):
    save_location = generate_save_location(state_id,"coralnet.json")
    with open(save_location, 'w') as outfile:
        json.dump(model.to_dict(), outfile)
    return save_location


@log_on_start(logging.INFO, "+ Started Generating json for {state_machine.dropbox_path}")
@log_on_end(logging.INFO, "- Finished Generating json for {state_machine.dropbox_path}")
def generate_json(state_machine: StateMachine):
    state = state_machine.get_state()
    if state.coralnet_load_file:
        logger.info(f"json already generated for {state_machine.dropbox_path}")
        return

    file_list = get_file_list(state_machine.dropbox_path)
    logger.info(f"got file list, length: {len(file_list)}")
    model = generate_model_json(file_list, state_machine.dropbox_path)

    save_location = save_model(state_machine.current_id,model)

    state.coralnet_load_file = save_location
    state.maxK = len(file_list)
    state_machine.update_state(state)
