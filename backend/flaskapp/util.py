import base64
import pandas as pd
import os

NOT_DELETED = 0
DELETED = 1
NOT_EXPIRED = 0
EXPIRED = 1

# Helper function
def objectToJson(record):
    d = {}
    for column in record.__table__.columns:
        d[column.name] = str(getattr(record, column.name))
    return d

def pathToFile(path): 
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        pngFile = encoded_string.decode('UTF-8')
    return pngFile;

# Generate excel file
def generateExcelFile(list):
    df = pd.DataFrame(list)
    df.to_excel('Generated_Credentials.xlsx')
    data = open('Generated_Credentials.xlsx', 'rb').read()
    os.remove("Generated_Credentials.xlsx") # remove file after read
    base64_encoded = base64.b64encode(data).decode('UTF-8') # encode for sending back to front end
    return base64_encoded

# Encode the png image
def encodePng(image):
    with open(image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string.decode('UTF-8')