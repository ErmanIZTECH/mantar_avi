import requests
from PIL import Image
from io import BytesIO
import numpy as np
from numpy_da import DynamicArray

base = "https://cbs.ogm.gov.tr/arcgis/rest/services/YAYIN/ARAZI_ORTUSU/MapServer/tile/"
layer = 16
xStart = 37591
xEnd = 37592
yStart = 25193
yEnd = 25193

fullImg = ""
for y in range(yStart, yEnd):
    for x in range(xStart, xEnd):
        link = base + str(layer) + '/' + str(y) + '/' + str(x)
        imgData = np.array(Image.open(BytesIO(requests.get(link).content)).convert('RGB'))
        fullImg = np.concatenate((fullImg, imgData), axis=0)

out = Image.fromarray(fullImg)
out.show()
  
# img.show()

# #out = np.concatenate((npimg, npimg2), axis=1)
# im = Image.fromarray(npimg)
# im = im.convert('RGB')
# im.save("your_file.png")