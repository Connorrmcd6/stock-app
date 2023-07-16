# sinani-stock-app
## create  root directory config folders
- create a folder in root directory called image_cache this will temporarily store invoice images
- create a folder in root directory called service_account_configs and store the google service account json file here
- create a folder in root directory called stock_in_configs and add csv files called names.csv, suppliers.csv, and stock_units.csv. this is where you will edit the content displayed in these fields on the app


## set up google service account
- create service account :https://medium.com/@jb.ranchana/write-and-append-dataframes-to-google-sheets-in-python-f62479460cf0
- enable google drive api: https://medium.com/@matheodaly.md/using-google-drive-api-with-python-and-a-service-account-d6ae1f6456c2

## configs.py
in the configs.py file get the sheet key and parent_folder key from the URL of the sheet and folder respectively. Remember to share the sheet/filder with the service account email address and give EDITOR access