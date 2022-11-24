import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class last15daysReport:
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    # Collect first page of artists’ list
    links = {
        "Yamanlar": "https://www.meteoblue.com/tr/hava/historyclimate/weatherarchive/yamanlar-da%c4%9f%c4%b1_t%c3%bcrkiye_297765?fcstlength=15&year="
        + str(currentYear)
        + "&month="
        + str(currentMonth),
        "Balcova": "https://www.meteoblue.com/tr/hava/historyclimate/weatherarchive/bal%c3%a7ova-baraj%c4%b1_t%c3%bcrkiye_9888632?fcstlength=15&year="
        + str(currentYear)
        + "&month="
        + str(currentMonth),
        "Kaynaklar": "https://www.meteoblue.com/tr/hava/historyclimate/weatherarchive/kurudere_t%c3%bcrkiye_305410?fcstlength=15&year="
        + str(currentYear)
        + "&month="
        + str(currentMonth),
    }
    for il in links.keys():
        page = requests.get(links[il])
        # Create a BeautifulSoup object
        soup = BeautifulSoup(page.text, "html.parser")

        # Pull all text from the BodyText div
        name_list = soup.find(id="chart_download")

        # Pull text from all instances of <a> tag within BodyText div
        print(name_list.attrs["href"])
        response = requests.get("https:" + name_list.attrs["href"])
        imageName = "image_" + il + ".png"
        open(imageName, "wb").write(response.content)
        # for parent in name_list.parents:
        #     print(parent.name)

        # for link in soup.find_all('a'):
        #     print(link.get('href'))


if __name__ == "__main__":
    last15daysReport()
