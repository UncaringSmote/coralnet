SITE = "BONAIRE"

dropbox_paths = ['/coralnet_AD/BONAIRE/2023/sites/PuntVierkant/large/part2/27_July_2023/Misty']  # This variable is the pathway leading to the folder you want to search for on Dropbox (ex, I have my folder_to_use inside a folder called "CoralNet", so this would be "/CoralNet/")

dropbox_app_key='KEY REPLACE'
dropbox_app_secret='SECRET REPLACE'
dropbox_token = 'TOKEN REPLACE'  # This is the authorization token for your Dropbox account
image_extension = 'JPG'
# IF MOOREA MAKE 5 rows 6 cols
# IF BONAIRE MAKE 6 rows 8 cols
if SITE == "BONAIRE":
    classifier_url = 'https://coralnet.ucsd.edu/api/classifier/34712/deploy/'  # The URL of the CoralNet source you are using to annotate your images
    coralnet_token = 'TOKEN REPLACE'  # Your CoralNet authorization token
    rows = 6
    cols = 8
elif SITE == "MOOREA":
    classifier_url = 'https://coralnet.ucsd.edu/api/classifier/22315/deploy/'  # The URL of the CoralNet source you are using to annotate your images
    coralnet_token = 'TOKEN REPLACE'  # Your CoralNet authorization token
    rows = 5
    cols = 6