import json

import requests
from retry import retry
from coralnet_load_model import CoralnetLoadModel
from config import local_path, folder_to_use, coralnet_token, classifier_url
from state import StateMachine

post_headers = {"Authorization": f"Token {coralnet_token}",
           "Content-type": "application/vnd.api+json"}

@retry(delay=5)
def send_coralnet_post(data, timeout=120):
    r = requests.post(url=classifier_url, data=data, headers=post_headers, timeout=timeout)

def send_coralnet_get():


def deploy_coralnet_api(state_machine:StateMachine, files_per_load = 100):
    state = state_machine.get_state()
    if state.deploy_completed:
        return

    with open(state.coralnet_load_file, "r") as f:
        model:CoralnetLoadModel = CoralnetLoadModel.from_dict(json.load(f))

    # Saves the classifier URL you will be using and your CoralNet authorization token


    export = {"data": []}  # Sets an empty dictionary that will store the resulting data
    if state.lastK != 0:
        with open(f'{folder_to_use}_export_temp.json', 'r') as outfile:
             export = json.load(outfile)
    # This is the loop that is used to send the many requests to the API.  It will continue until k gets large enough that it will exceed the number of images in the JSON file.
    for k in range(state.lastK,state.maxK,files_per_load):
        print(f'K = {k}')
        state.lastk = k
        state_machine.update_state(state)
        # Pulls out the 100 images
        batch_to_load = CoralnetLoadModel(model.data[k:k+files_per_load])

        print("start post")
        retry = True
        # Sends the post request to the CoralNet API using the temp JSON file and the headers defined earlier
        while retry:
            try:
                r = requests.post(url=classifier_url, data=open(f"{local_path}temp_json.json"), headers=headers, timeout=120)
                retry = False
            except:
                print("post exception")
                time.sleep(5)
        print("stop post")
        time.sleep(60)  # Waits 60 seconds before attempting to retrieve results from the post request
        in_progress = True

        while in_progress:  # This pings CoralNet every 60 seconds to check the status of the job
            print("beat")
            # Sends a get request in an attempt to retrieve the annotations
            try:
                r_status = requests.get(url='https://coralnet.ucsd.edu' + r.headers['Location'],
                                        headers={"Authorization": f"Token {coralnet_token}"})
            except:
                print("get status exception")
                time.sleep(5)
                continue

            if r_status is None or r_status.status_code != 200 or r_status.content is None:
                print("problem getting status")
                time.sleep(5)
                continue

            curr_status = json.loads(r_status.content)  # Extracts the content from the json request

            if 'status' in curr_status['data'][0][
                'attributes'].keys():  # Checks to see if the status key is in the request dictionary - if not it is complete
                print(curr_status['data'][0]['attributes']['successes'])
                time.sleep(60)  # Waits 60s before attempting the next status update

            else:  # If it doesn't find 'status' key, then it sets in_progress to false and saves the request data
                export['data'].extend(curr_status['data'])
                in_progress = False

        # Creates a temp json with the data in case Python crashes -- this provides a way to upload later and avoid losing all the time
        with open(f'{local_path}export_temp.json', 'w') as outfile:
            json.dump(export, outfile)

        k += 100  # Increases k by 100 to allow it to pull the next 100 images (or end the script if it has already pulled all the images)

    # Creates a final json file with the relevant information included
    with open(f'{local_path}{folder_to_use}_export.json', 'w') as outfile:
        json.dump(export, outfile)

    # Removes the two temp json files because they are not needed anymore as the script has completed
    del r  # Deletes the request variable to unlock the temp_json file so it can be deleted
    os.remove(f'{local_path}temp_json.json')
    os.remove(f'{local_path}export_temp.json')
