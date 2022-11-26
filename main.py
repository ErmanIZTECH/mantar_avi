import requests
from bs4 import BeautifulSoup
from datetime import datetime


def getcoordinates(coord1, coord2):
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    page = requests.get(
        "https://www.meteoblue.com/tr/hava/historyclimate/weatherarchive/"
        + str(coord1)
        + "N"
        + str(coord2)
        + "E"
        + "?fcstlength=15&year="
        + str(currentYear)
        + "&month="
        + str(currentMonth)
    )

    soup = BeautifulSoup(page.text, "html.parser")
    response = requests.get("https:" + soup.find(id="chart_download").attrs["href"])
    open("coordinate_image.png", "wb").write(response.content)


class last15daysReport:
    if open("lastupdate.txt", "r").readline() == str(datetime.now().date()):
        print("Images area up to date: " + str(datetime.now().date()))
        pass
    else:
        print("New Day retrieving the data for " + str(datetime.now().date()))
        currentMonth = datetime.now().month
        currentYear = datetime.now().year

        # Collect first page of artists’ list
        links = {
            "Yamanlar": "yamanlar-da%c4%9f%c4%b1_t%c3%bcrkiye_297765",
            "Balcova": "bal%c3%a7ova-baraj%c4%b1_t%c3%bcrkiye_9888632",
            "Kaynaklar": "kurudere_t%c3%bcrkiye_305410",
            "Kizilcahamam": "k%c4%b1z%c4%b1lcahamam_t%c3%bcrkiye_743051",
        }

        for il in links.keys():
            page = requests.get(
                "https://www.meteoblue.com/tr/hava/historyclimate/weatherarchive/"
                + links[il]
                + "?fcstlength=15&year="
                + str(currentYear)
                + "&month="
                + str(currentMonth)
            )
            soup = BeautifulSoup(page.text, "html.parser")
            response = requests.get(
                "https:" + soup.find(id="chart_download").attrs["href"]
            )
            open("image_" + il + ".png", "wb").write(response.content)
        open("lastupdate.txt", "w").write(str(datetime.now().date()))


if __name__ == "__main__":
    pass
