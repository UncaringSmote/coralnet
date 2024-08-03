import json
import logging
import re

import pandas as pd
from logdecorator import log_on_start, log_on_end

from config import image_extension
from state import StateMachine
from utils import generate_save_location


@log_on_start(logging.INFO, "+ Started generate final csv for {state_machine.dropbox_path}")
@log_on_end(logging.INFO, "- Finished generate final csv for {state_machine.dropbox_path}")
def generate_final_csv(state_machine: StateMachine):
    state = state_machine.get_state()
    if state.csv_generated:
        return

    with open(state.deploy_result_file, 'r') as outfile:
        results = json.load(outfile)


    d = results['successes']

    # Creates an empty dictionary used to store the relevant information
    dic = {}
    n = 1
    # Nested loop to extract information from the json dictionary
    for i in range(len(d)):  # loops over the images in the file

        # Extracts information at the image level
        img_id = d[i]['id']  # Pulls out the image url
        attrib = d[i]['attributes']  # Pulls out the attributes dictionary
        img_points = attrib['points']  # Pulls out the information for each point

        for j in range(len(img_points)):  # Loops over the points on each image

            temp_class = img_points[j][
                'classifications']  # Pulls out the information on classifications for each point (each point has 5 suggestions)

            # Creates an empty list used in the next loop (want it overwritten each time)
            temp_lab = []
            temp_conf = []

            for k in range(len(temp_class)):  # Loops over the five machine suggestions
                temp_lab.append(temp_class[k]['label_code'])
                temp_conf.append(temp_class[k]['score'])

            # Now it takes the relevant information and appends it to the output dictionary.  A dictionay is used in this step for efficiency purposes.
            dic[f'row_{n}'] = [re.search(f'^.*[/](.*.{image_extension})', img_id).group(1), img_id, j + 1,
                               img_points[j]['column'], img_points[j]['row'],
                               temp_lab[0], temp_conf[0],
                               temp_lab[1], temp_conf[1],
                               temp_lab[2], temp_conf[2],
                               temp_lab[3], temp_conf[3],
                               temp_lab[4], temp_conf[4]]
            n += 1

    output = pd.DataFrame.from_dict(dic, orient='index')  # Converts the dictionary to a dataframe
    output.columns = ['img_name', 'img_url', 'point', 'column', 'row',
                      'machine_suggestion1', 'confidence1',
                      'machine_suggestion2', 'confidence2',
                      'machine_suggestion3', 'confidence3',
                      'machine_suggestion4', 'confidence4',
                      'machine_suggestion5', 'confidence5']
    # Outputs the csv
    file_path = generate_save_location(state_machine.current_id,"annotated.csv")
    output.to_csv(file_path, index=False)
