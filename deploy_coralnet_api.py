import json
import logging
import os
import time

import requests
from logdecorator import log_on_start, log_on_end
from retry import retry
from coralnet_load_model import CoralnetLoadModel
from config import coralnet_token, classifier_url
from state import StateMachine
from utils import generate_save_location

post_headers = {"Authorization": f"Token {coralnet_token}",
           "Content-type": "application/vnd.api+json"}

get_headers = {"Authorization": f"Token {coralnet_token}"}
logger = logging.getLogger()

@log_on_start(logging.INFO, "+ Started Post")
@log_on_end(logging.INFO, "- Finished Post : {result.status_code:d}")
@retry(delay=20)
def send_coralnet_post(data, timeout=120):
    response = requests.post(url=classifier_url, json=data, headers=post_headers, timeout=timeout)
    if not response or response.status_code != 202:
        raise Exception(f"post failed: {response}")
    return response

@log_on_start(logging.INFO, "+ Started Get Status: {url}")
@log_on_end(logging.INFO, "- Finished Get Status : {result.status_code:d}")
@retry(delay=20)
def send_coralnet_get_status(url, timeout =120):
    response = requests.get(url=url,headers=get_headers,timeout=timeout)
    if not response or response.status_code != 200 or response.content is None:
        raise Exception(f"problem getting status: {response}")
    return response


@log_on_end(logging.INFO, "{result[1]}")
def decode_status(response,k):
    curr_status = json.loads(response.content)
    message = None

    if 'status' in curr_status['data'][0]['attributes'].keys():
        attributes = curr_status['data'][0]['attributes']
        s = attributes['successes']
        f = attributes['failures']
        t = attributes['total']
        status = attributes['status']
        ids = curr_status['data'][0]['id'].split(",")
        ids = ''.join(str(_) for _ in ids)
        message = f"K={k}, Status: {status} , Successes: {s} , Failures: {f} , Total {t} , Ids: {ids}"

    return curr_status, message


def get_result(url_location,k):
    while True:  # This pings CoralNet every 60 seconds to check the status of the job
        get_response = send_coralnet_get_status(url='https://coralnet.ucsd.edu' + url_location)
        status , message = decode_status(get_response,k)
        if message:
            time.sleep(60)
        else:
            return status

def seperate_errors(result):
    image_list = result['data']
    successes,errors= [],[]
    for image in image_list:
        attributes = image['attributes']
        if 'error' in attributes.keys() or 'errors' in attributes.keys():
            errors.append(image)
        else:
            successes.append(image)
    return successes,errors

@log_on_start(logging.INFO, f"+ Started Deploying Coralnet Api")
@log_on_end(logging.INFO, f"- Finished Deploying Coralnet Aps")
def deploy_coralnet_api(state_machine:StateMachine, files_per_load = 100):
    state = state_machine.get_state()
    if state.deploy_completed:
        logger.info("already deployed")
        return

    with open(state.coralnet_load_file, "r") as f:
        model:CoralnetLoadModel = CoralnetLoadModel.from_dict(json.load(f))

    output = {'successes':[],
               'errors':[]}
    deploy_results_file_location = generate_save_location(state_machine.current_id,"deploy_results.json")
    if state.lastK != 0 :
        with open(deploy_results_file_location, 'r') as outfile:
             output = json.load(outfile)

    # This is the loop that is used to send the many requests to the API.  It will continue until k gets large enough that it will exceed the number of images in the JSON file.
    for k in range(state.lastK,state.maxK,files_per_load):
        logger.info(f'K = {k} of {state.maxK}')
        state.lastK=k
        state_machine.update_state(state)
        # Pulls out the 100 images
        batch_to_load = CoralnetLoadModel(model.data[k:k+files_per_load])
        post_response = send_coralnet_post(batch_to_load.to_dict())
        time.sleep(60)  # Waits 60 seconds before attempting to retrieve results from the post request
        result = get_result(post_response.headers['Location'],k)
        successes,errors = seperate_errors(result)

        output['successes'].extend(successes)
        output['errors'].extend(errors)
        with open(deploy_results_file_location, 'w') as outfile:
            json.dump(output, outfile)


    state.deploy_completed = True
    state.deploy_result_file = deploy_results_file_location
    state_machine.update_state(state)

