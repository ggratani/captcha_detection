from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

# importing modules
import urllib.request

# Get an image with text
read_image_url = "https://app.arba.gov.ar/LiqPredet/captcha/imagen?token=6dd237062037c8409631af8a67a89cbace0e85fcb99e9facceeddf3c0c951fc6"

# read_image_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg"

urllib.request.urlretrieve(read_image_url, "gfg.png")
img = Image.open("gfg.png")
newsize = (300, 150)
im1 = img.resize(newsize)
im1 = im1.save("captcha.jpg")
'''
Authenticate
Authenticates your credentials and creates a client.
'''
subscription_key = "3a308f9292504c73bc25af893e669d67"
endpoint = "https://read-captcha.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
'''
END - Authenticate
'''

'''
OCR: Read File using the Read API, extract text - remote
This example will extract text in an image, then print results, line by line.
This API call can also extract handwriting style text (not shown).
'''
print("===== Read File - remote =====")


# Call API with URL and raw response (allows you to get the operation location)
read_response = computervision_client.read(r"C:\Users\gasto\Documents\Azure\captcha-detection\geeks.jpg",  raw=True)

# Get the operation location (URL with an ID at the end) from the response
read_operation_location = read_response.headers["Operation-Location"]
# Grab the ID from the URL
operation_id = read_operation_location.split("/")[-1]

# Call the "GET" API and wait for it to retrieve the results 
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Print the detected text, line by line
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)
            print(line.bounding_box)
print()
'''
END - Read File - remote
'''

print("End of Computer Vision quickstart.")