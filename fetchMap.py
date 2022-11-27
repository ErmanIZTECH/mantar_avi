import requests
from PIL import Image
from io import BytesIO

base = "https://cbs.ogm.gov.tr/arcgis/rest/services/YAYIN/ARAZI_ORTUSU/MapServer/tile/"
layer = 16
xStart = 37591
xEnd = 37605
yStart = 25191
yEnd = 25205


link = base + str(layer) + "/" + str(yStart) + "/" + str(xStart)
img_1 = Image.open(BytesIO(requests.get(link).content)).convert("RGB")
fullImage = Image.new(
    "RGB",
    ((xEnd - xStart + 1) * img_1.size[0], (yEnd - yStart + 1) * img_1.size[1]),
    (250, 250, 250),
)
for x in range(xStart, xEnd + 1):
    for y in range(yStart, yEnd + 1):
        link = base + str(layer) + "/" + str(y) + "/" + str(x)
        fullImage.paste(
            Image.open(BytesIO(requests.get(link).content)).convert("RGB"),
            ((x - xStart) * img_1.size[0], (y - yStart) * img_1.size[1]),
        )
        # Image.fromarray(imgData).show()

fullImage.show()
