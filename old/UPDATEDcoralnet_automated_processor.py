# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 17:36:23 2022
.


@author: Ras-ster 2
"""

# Imports necessary libraries
import dropbox
import json
import random
import requests
import time
import os
import re
import pandas as pd

# Defines variables
folder_to_use = 'Temae'  # This variable is the folder you want to search for on Dropbox and will also be how the resulting JSON will be named
local_path = 'C:\\Users\\Ras-ster 2\\Desktop\\Ally\\fish_2023\\'  # This is the pathway on you local machine where these files will be saved and located (ex, for me it is "'C:\\Users\\Ras-ster 2\\Desktop\\Ally\\'" -- note the double slashes)
dropbox_path = '/coralnet_AD/2023_fish/'  # This variable is the pathway leading to the folder you want to search for on Dropbox (ex, I have my folder_to_use inside a folder called "CoralNet", so this would be "/CoralNet/")
dropbox_token = 'token'
classifier_url = 'https://coralnet.ucsd.edu/api/classifier/22315/deploy/'  # The URL of the CoralNet source you are using to annotate your images
coralnet_token = 'token'  # Your CoralNet authorization token
image_extension = 'JPG'


def generate_json(folder_to_use, local_path, dropbox_path, dropbox_token):
    # Connects to our Dropbox account
    dbx = dropbox.Dropbox(dropbox_token)
    dbx.users_get_current_account()

    # Creates empty list to store the file names within the folder of interest
    file_list = []

    # Pulls out first 2000 files from the folder, adds the names to file_list, then creates a cursor
    # signifying its end location in the folder
    file_list_all = dbx.files_list_folder(f'{dropbox_path}{folder_to_use}')
    file_list.extend(file_list_all.entries)
    file_cursor = file_list_all.cursor

    keep_retrieving = True  # Sets this as True, and will change to False when all files retrieved
    while keep_retrieving:  # Loops through to retrieve the rest of the images
        file_list_continue = dbx.files_list_folder_continue(file_cursor)
        file_list.extend(file_list_continue.entries)
        file_cursor = file_list_continue.cursor

        if len(file_list_continue.entries) == 0:
            keep_retrieving = False

    dat = {"data": []}

    for entry in file_list:
        pathway = f'{dropbox_path}{folder_to_use}/' + entry.name
        tmp_name = dbx.sharing_create_shared_link(path=pathway, short_url=False, pending_upload=None)

        to_append = {"type": "image",
                     "attributes": {"url": tmp_name.url[:-1] + '1',
                                    "points": [
                                        {"row": random.randint(450, 870),
                                         "column": random.randint(600, 1067)},
                                        {"row": random.randint(450, 870),
                                         "column": random.randint(1067, 1533)},
                                        {"row": random.randint(450, 870),
                                         "column": random.randint(1533, 2000)},
                                        {"row": random.randint(450, 870),
                                         "column": random.randint(2000, 2467)},
                                        {"row": random.randint(450, 870),
                                         "column": random.randint(2467, 2933)},
                                        {"row": random.randint(450, 870),
                                         "column": random.randint(2933, 3400)},
                                        {"row": random.randint(870, 1290),
                                         "column": random.randint(600, 1067)},
                                        {"row": random.randint(870, 1290),
                                         "column": random.randint(1067, 1533)},
                                        {"row": random.randint(870, 1290),
                                         "column": random.randint(1533, 2000)},
                                        {"row": random.randint(870, 1290),
                                         "column": random.randint(2000, 2467)},
                                        {"row": random.randint(870, 1290),
                                         "column": random.randint(2467, 2933)},
                                        {"row": random.randint(870, 1290),
                                         "column": random.randint(2933, 3400)},
                                        {"row": random.randint(1290, 1710),
                                         "column": random.randint(600, 1067)},
                                        {"row": random.randint(1290, 1710),
                                         "column": random.randint(1067, 1533)},
                                        {"row": random.randint(1290, 1710),
                                         "column": random.randint(1533, 2000)},
                                        {"row": random.randint(1290, 1710),
                                         "column": random.randint(2000, 2467)},
                                        {"row": random.randint(1290, 1710),
                                         "column": random.randint(2467, 2933)},
                                        {"row": random.randint(1290, 1710),
                                         "column": random.randint(2933, 3400)},
                                        {"row": random.randint(1710, 2130),
                                         "column": random.randint(600, 1067)},
                                        {"row": random.randint(1710, 2130),
                                         "column": random.randint(1067, 1533)},
                                        {"row": random.randint(1710, 2130),
                                         "column": random.randint(1533, 2000)},
                                        {"row": random.randint(1710, 2130),
                                         "column": random.randint(2000, 2467)},
                                        {"row": random.randint(1710, 2130),
                                         "column": random.randint(2467, 2933)},
                                        {"row": random.randint(1710, 2130),
                                         "column": random.randint(2933, 3400)},
                                        {"row": random.randint(2130, 2550),
                                         "column": random.randint(600, 1067)},
                                        {"row": random.randint(2130, 2550),
                                         "column": random.randint(1067, 1533)},
                                        {"row": random.randint(2130, 2550),
                                         "column": random.randint(1533, 2000)},
                                        {"row": random.randint(2130, 2550),
                                         "column": random.randint(2000, 2467)},
                                        {"row": random.randint(2130, 2550),
                                         "column": random.randint(2467, 2933)},
                                        {"row": random.randint(2130, 2550),
                                         "column": random.randint(2933, 3400)},
                                    ]
                                    }
                     }
        dat['data'].append(to_append)

    with open(f'{local_path}{folder_to_use}.json', 'w') as outfile:
        json.dump(dat, outfile)


def deploy_coralnet_api(folder_to_use, local_path, classifier_url, coralnet_token, kvalue):
    # Opens the JSON file created by json_generator.py
    with open(f"{local_path}{folder_to_use}.json", "r") as f:
        d = json.load(f)

    # Saves the classifier URL you will be using and your CoralNet authorization token
    headers = {"Authorization": f"Token {coralnet_token}",
               "Content-type": "application/vnd.api+json"}

    # Sets up some variables that will be used in the deployment loop
    k = kvalue  # k is a variable that is initialized at 0 and increases by 100 each loop iteration.  It is used to move along the larger JSON file and mark which images to pull out.
    dat_length = 100  # Initialized at 100, but will change based on how many photos are pulled for each value of k
    export = {"data": []}  # Sets an empty dictionary that will store the resulting data
    if k != 0:
        with open(f'{local_path}export_temp.json', 'r') as outfile:
             export = json.load(outfile)
    # This is the loop that is used to send the many requests to the API.  It will continue until k gets large enough that it will exceed the number of images in the JSON file.
    while dat_length == 100:

        # Pulls out the 100 images
        dat = {"data": d['data'][k:k + 100]}
        dat_length = len(dat['data'])

        if dat_length == 0:
            break
        # Prints k so you can monitor progress in the console
        print(f'K = {k}')
        with open('lastK.txt', 'a') as f:
            f.write(f'K = {k} ,')

        # Writes a temporary JSON file in the same directory as the larger file containing the images pulled out earlier.
        with open(f'{local_path}temp_json.json', 'w') as outfile:
            json.dump(dat, outfile)
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


def check_coralnet_errors(folder_to_use, local_path, dropbox_token, dropbox_path, image_extension, classifier_url,
                          coralnet_token):
    # Sets up headers in case we need to send more requests to CoralNet to fix errors
    headers = {"Authorization": f"Token {coralnet_token}",
               "Content-type": "application/vnd.api+json"}

    # Connects to our Dropbox account
    dbx = dropbox.Dropbox(dropbox_token)
    dbx.users_get_current_account()

    # This script takes the newly-generated json file from coralnet_api_deployer.py, checks for errors, and attempts to correct those errors

    # Opens the new file
    f = open(f"{local_path}{folder_to_use}_export.json", )

    # Converts the json file into a dictionary and extracts the value from the only key
    dat = json.load(f)
    d = dat['data']

    # Checks for images that returned errors instead of data for points
    # If it finds any, it generates a new json file for these images that can be added to
    error_images = []
    error_index = []
    error_dat = {"data": []}

    for i in range(len(d)):

        attrib = d[i]['attributes']

        if ((
                'error' in attrib.keys()) or 'errors' in attrib.keys()):  # Checks to see if the 'error' key is in the image attribute dictionary
            error_images.append(re.search(f'^.*[/](.*.{image_extension})', d[i]['id']).group(
                1))  # If it is, it adds the image name to the error_images list
            error_index.append(i)  # And it saves the index to be removed later
            print(attrib)

    if len(error_images) > 0:

        # Now that we know which elements are errors, we want to remove these from the lists so they can be replaced
        for ele in sorted(error_index, reverse=True):
            del dat['data'][
                ele]  # Deletes the entries from the shorter list we're working with and from the larger json

        # Now, we take the images that threw errors and generate a new json file for them
        error_dat = {"data": []}

        for entry in error_images:
            pathway = f'{dropbox_path}{folder_to_use}/' + entry
            tmp_name = dbx.sharing_create_shared_link(path=pathway, short_url=False, pending_upload=None)

            to_append = {"type": "image",
                         "attributes": {"url": tmp_name.url[:-1] + '1',
                                        "points": [
                                            {"row": random.randint(450, 870),
                                             "column": random.randint(600, 1067)},
                                            {"row": random.randint(450, 870),
                                             "column": random.randint(1067, 1533)},
                                            {"row": random.randint(450, 870),
                                             "column": random.randint(1533, 2000)},
                                            {"row": random.randint(450, 870),
                                             "column": random.randint(2000, 2467)},
                                            {"row": random.randint(450, 870),
                                             "column": random.randint(2467, 2933)},
                                            {"row": random.randint(450, 870),
                                             "column": random.randint(2933, 3400)},
                                            {"row": random.randint(870, 1290),
                                             "column": random.randint(600, 1067)},
                                            {"row": random.randint(870, 1290),
                                             "column": random.randint(1067, 1533)},
                                            {"row": random.randint(870, 1290),
                                             "column": random.randint(1533, 2000)},
                                            {"row": random.randint(870, 1290),
                                             "column": random.randint(2000, 2467)},
                                            {"row": random.randint(870, 1290),
                                             "column": random.randint(2467, 2933)},
                                            {"row": random.randint(870, 1290),
                                             "column": random.randint(2933, 3400)},
                                            {"row": random.randint(1290, 1710),
                                             "column": random.randint(600, 1067)},
                                            {"row": random.randint(1290, 1710),
                                             "column": random.randint(1067, 1533)},
                                            {"row": random.randint(1290, 1710),
                                             "column": random.randint(1533, 2000)},
                                            {"row": random.randint(1290, 1710),
                                             "column": random.randint(2000, 2467)},
                                            {"row": random.randint(1290, 1710),
                                             "column": random.randint(2467, 2933)},
                                            {"row": random.randint(1290, 1710),
                                             "column": random.randint(2933, 3400)},
                                            {"row": random.randint(1710, 2130),
                                             "column": random.randint(600, 1067)},
                                            {"row": random.randint(1710, 2130),
                                             "column": random.randint(1067, 1533)},
                                            {"row": random.randint(1710, 2130),
                                             "column": random.randint(1533, 2000)},
                                            {"row": random.randint(1710, 2130),
                                             "column": random.randint(2000, 2467)},
                                            {"row": random.randint(1710, 2130),
                                             "column": random.randint(2467, 2933)},
                                            {"row": random.randint(1710, 2130),
                                             "column": random.randint(2933, 3400)},
                                            {"row": random.randint(2130, 2550),
                                             "column": random.randint(600, 1067)},
                                            {"row": random.randint(2130, 2550),
                                             "column": random.randint(1067, 1533)},
                                            {"row": random.randint(2130, 2550),
                                             "column": random.randint(1533, 2000)},
                                            {"row": random.randint(2130, 2550),
                                             "column": random.randint(2000, 2467)},
                                            {"row": random.randint(2130, 2550),
                                             "column": random.randint(2467, 2933)},
                                            {"row": random.randint(2130, 2550),
                                             "column": random.randint(2933, 3400)},
                                        ]
                                        }
                         }
            error_dat['data'].append(to_append)

        # Now that we have identified error images, deleted them from the master json structure, and created a new json for them
        # We need to query coralnet again to attempt to get actual data from them

        k = 0
        dat_length = 100
        export = {"data": []}

        while dat_length == 100:

            error_data = {"data": error_dat['data'][k:k + 100]}
            dat_length = len(error_data['data'])

            if dat_length == 0:
                break

            # This writes the error json to a file so it can be used by the coralnet post request
            with open(f'{local_path}error_json.json', 'w') as outfile:
                json.dump(error_data, outfile)

            # Sends the initial post request to coralnet
            r = requests.post(url=classifier_url, data=open(f"{local_path}error_json.json"), headers=headers)

            time.sleep(60)
            in_progress = True

            while in_progress:  # This pings CoralNet every 60 seconds to check the status of the job

                r_status = requests.get(url='https://coralnet.ucsd.edu' + r.headers['Location'],
                                        headers={"Authorization": f"Token {coralnet_token}"})

                curr_status = json.loads(r_status.content)  # Extracts the content from the json request
                print(r_status)
                if 'status' in curr_status['data'][0][
                    'attributes'].keys():  # Checks to see if the status key is in the request dictionary - if not it is complete
                    print(curr_status['data'][0]['attributes']['successes'])
                    time.sleep(60)  # Waits 60s before attempting the next status update

                else:  # If it doesn't find 'status' key, then it sets in_progress to false and saves the request data
                    export['data'].extend(curr_status['data'])
                    in_progress = False

            k += 100

        # Now checks the new data from coralnet for new errors
        # If it finds any, it alerts the user that there's STILL issues
        # Otherwise, it adds the new data to the old json, and exports a new file with all the data to be parsed by json_parser
        exp_dat = export['data']

        error_images = []
        error_index = []
        error_dat = {"data": []}

        for i in range(len(exp_dat)):

            attrib = exp_dat[i]['attributes']

            if 'error' in attrib.keys() or 'errors' in attrib.keys():  # Checks to see if the 'error' key is in the image attribute dictionary
                error_images.append(re.search(f'^.*[/](.*.{image_extension})', exp_dat[i]['id']).group(
                    1))  # If it is, it adds the image name to the error_images list
                error_index.append(i)  # And it saves the index to be removed later
                print(attrib)

        if len(error_images) > 0:
            print(error_images)
            print('STILL HAVE ISSUES!!!!')
            errors_present = True
        else:
            dat['data'].extend(exp_dat)
            print('A-OK!')
            errors_present = False

            # Now, we export the error-checked file!
            with open(f'{local_path}{folder_to_use}_export.json', 'w') as outfile:
                json.dump(dat, outfile)

            # ...and we delete the error_json.json file
            del r
            os.remove(f'{local_path}error_json.json')

    else:
        print('No errors!')
        errors_present = False

    return errors_present


def generate_coralnet_csv(folder_to_use, local_path, image_extension):
    # Loads the json file
    f = open(f"{local_path}{folder_to_use}_export.json", )

    # Converts the json file into a dictionary and extracts the value from the only key
    dat = json.load(f)
    d = dat['data']

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
    output.to_csv(f'{local_path}{folder_to_use}.csv', index=False)


# folders_to_use = ["Batch16", "Batch17", "Batch18"]

'''
for folder_to_use in folders_to_use:
    generate_json(folder_to_use, local_path, dropbox_path, dropbox_token)

    deploy_coralnet_api(folder_to_use, local_path, classifier_url, coralnet_token)

    errors_present = check_coralnet_errors(folder_to_use, local_path, dropbox_token, dropbox_path, image_extension, classifier_url, coralnet_token)
    if errors_present:
        print(f"{folder_to_use} still has errors!!")
    else:
        generate_coralnet_csv(folder_to_use, local_path, image_extension)
'''

# folders_to_use = ["Batch01", "Batch02"]

folders_to_use = ["Temae"]

for folder_to_use in folders_to_use:
    k = 0
    skip_to_error = False
    if not skip_to_error:
        if k == 0:
            generate_json(folder_to_use, local_path, dropbox_path, dropbox_token)
        deploy_coralnet_api(folder_to_use, local_path, classifier_url, coralnet_token,k)
    errors_present = check_coralnet_errors(folder_to_use, local_path, dropbox_token, dropbox_path, image_extension,
                                       classifier_url, coralnet_token)
    if errors_present:
        print(f"{folder_to_use} still has errors!!")
    else:
        generate_coralnet_csv(folder_to_use, local_path, image_extension)
