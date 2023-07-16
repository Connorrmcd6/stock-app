# sinani-stock-app

## set up google service account
- create google service account :https://medium.com/@jb.ranchana/write-and-append-dataframes-to-google-sheets-in-python-f62479460cf0
- enable google drive api: https://medium.com/@matheodaly.md/using-google-drive-api-with-python-and-a-service-account-d6ae1f6456c2
- store the json key as a secret under advanced settings on streamlit cloud

## configs.py
in the configs.py file get the sheet key and parent_folder key from the URL of the sheet and folder respectively. Remember to share the sheet/filder with the service account email address and give EDITOR access