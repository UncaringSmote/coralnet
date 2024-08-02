import json
import random
from typing import List

import dropbox
from dropbox import Dropbox
from dropbox.files import ListFolderResult
from dropbox.sharing import PathLinkMetadata

from coralnet_load_model import Point, Attributes, Data, CoralnetLoadModel
from config import dropbox_token, dropbox_path, folder_to_use, local_path
from state import StateMachine


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

def generate_model_json(dbx:Dropbox,file_list:List[any])->CoralnetLoadModel:
    data = []

    for entry in file_list:
        pathway = f'{dropbox_path}{folder_to_use}/' + entry.name
        tmp_name = dbx.sharing_create_shared_link(path=pathway, short_url=False, pending_upload=None)
        data.append(generate_data_json(tmp_name))

    return CoralnetLoadModel(data)
def get_file_list(dbx:Dropbox)->List[any]:
    # Creates empty list to store the file names within the folder of interest
    file_list = []

    # Pulls out first 2000 files from the folder, adds the names to file_list, then creates a cursor
    # signifying its end location in the folder
    file_list_result = dbx.files_list_folder(f'{dropbox_path}{folder_to_use}')
    file_list.extend(file_list_result.entries)
    while file_list_result.has_more:  # Loops through to retrieve the rest of the images
        file_list_result = dbx.files_list_folder_continue(file_list_result.cursor)
        file_list.extend(file_list_result.entries)
    return file_list

def generate_json(state_machine:StateMachine):
    state = state_machine.get_state()
    if state.coralnet_load_file:
        return
    # Connects to our Dropbox account
    dbx = dropbox.Dropbox(dropbox_token)
    dbx.users_get_current_account()
    file_list = get_file_list(dbx)
    model = generate_model_json(dbx,file_list)

    save_location = f'{folder_to_use}.json'
    with open(save_location, 'w') as outfile:
        json.dump(model.to_dict(), outfile)

    state.coralnet_load_file = save_location
    state.maxK = len(file_list)
    state_machine.update_state(state)
