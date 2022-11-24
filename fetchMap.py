import requests
from PIL import Image
from io import BytesIO
import numpy as np

base = "https://cbs.ogm.gov.tr/arcgis/rest/services/YAYIN/ARAZI_ORTUSU/MapServer/tile/"
layer = 16
xStart = 37591
xEnd = 37592
yStart = 25193
yEnd = 25193

fullImg = ""
for y in range(yStart, yEnd):
    for x in range(xStart, xEnd):
        link = base + str(layer) + "/" + str(y) + "/" + str(x)
        imgData = np.array(
            Image.open(BytesIO(requests.get(link).content)).convert("RGB")
        )
        fullImg = np.concatenate((fullImg, imgData), axis=0)

out = Image.fromarray(fullImg)
out.show()