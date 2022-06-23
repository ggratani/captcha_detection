import json
import os
import sys
import requests
import time
# If you are using a Jupyter Notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO

# importing modules
import urllib.request

# Get an image with text
read_image_url = "https://app.arba.gov.ar/LiqPredet/captcha/imagen?token=6dd237062037c8409631af8a67a89cbace0e85fcb99e9facceeddf3c0c951fc6"

urllib.request.urlretrieve(read_image_url, "gfg.png")
img = Image.open("gfg.png")
newsize = (300, 150)
im1 = img.resize(newsize)
im1 = im1.save("captcha.jpg")


subscription_key = "3a308f9292504c73bc25af893e669d67"
endpoint = "https://read-captcha.cognitiveservices.azure.com/"

text_recognition_url = endpoint + "/vision/v3.1/read/analyze"

# Set image_url to the URL of an image that you want to recognize.
headers = {'Ocp-Apim-Subscription-Key': subscription_key,'Content-Type': 'application/octet-stream'}
with open('captcha.jpg', 'rb') as f:
    data = f.read()
response = requests.post(
    text_recognition_url, headers=headers, data=data)
response.raise_for_status()

# Extracting text requires two API calls: One call to submit the
# image for processing, the other to retrieve the text found in the image.

# Holds the URI used to retrieve the recognized text.
operation_url = response.headers["Operation-Location"]

# The recognized text isn't immediately available, so poll to wait for completion.
analysis = {}
poll = True
while (poll):
    response_final = requests.get(
        response.headers["Operation-Location"], headers=headers)
    analysis = response_final.json()
    
    print(json.dumps(analysis, indent=4))

    time.sleep(1)
    if ("analyzeResult" in analysis):
        poll = False
    if ("status" in analysis and analysis['status'] == 'failed'):
        poll = False

polygons = []
if ("analyzeResult" in analysis):
    # Extract the recognized text, with bounding boxes.
    polygons = [(line["boundingBox"], line["text"])
                for line in analysis["analyzeResult"]["readResults"][0]["lines"]]

# Display the image and overlay it with the extracted text.
image = Image.open('./captcha.jpg')
ax = plt.imshow(image)
for polygon in polygons:
    vertices = [(polygon[0][i], polygon[0][i+1])
                for i in range(0, len(polygon[0]), 2)]
    text = polygon[1]
    patch = Polygon(vertices, closed=True, fill=False, linewidth=2, color='y')
    ax.axes.add_patch(patch)
    plt.text(vertices[0][0], vertices[0][1], text, fontsize=20, va="top")
plt.show()

