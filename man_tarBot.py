import sys
import os
from bs4 import BeautifulSoup
from datetime import datetime
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater
from telegram.update import Update
import requests

def last15daysReport():
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

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Merhaba *man-tar* mantar avlarında kullanılmak üzere yazılmış bir telegram botudur.\n"
        + "Komuları görmek için /help komutunu kullanın."
    )

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

def coord(update, context):
    """Usage: /put value"""
    # Generate ID and separate value from command
    # We don't use context.args here, because the value may contain whitespaces
    value = update.message.text.partition(" ")[2]

    coordN = round(float(value.split()[0][0:7]), 3)
    coordE = round(float(value.split()[1][0:7]), 3)
    update.message.reply_text("Kordinatlar alındı: " + str([coordN, coordE] +" Rapor hazırlanıyor."))
    getcoordinates(coordN, coordE)
    update.message.reply_photo(photo=open("coordinate_image.png", "rb"))

def location(update, context):
    user_location = update.message.location
    lat = round(float(user_location.latitude), 3)
    lon = round(float(user_location.longitude), 3)
    update.message.reply_text("Kordinatlar alındı: " + str([lat, lon])+" Rapor hazırlanıyor.")
    getcoordinates(lat, lon)
    update.message.reply_photo(photo=open("coordinate_image.png", "rb"))

def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        "/start : Genel bilgilendirme mesajını gösterir.\n"
        + "/help : Komutları listeler.\n"
        + "15 günlük meteorolojik raporunu almak istediğiniz lokasyonu direkt gönderin.\n"
        + "/coord verilen koordinatların raporu. [örn: /coord 35.1234 27.2134]\n"
        + "veya halihazırdaki preset edilmiş lokasyonları aşağıdaki komutla çalıştırın.\n"
        + "/yamanlar : Yamanlar bölgesi 15 günlük raporu.\n"
        + "/balcova : Balçova bölgesi 15 günlük raporu.\n"
        + "/kaynaklar : Kaynaklar bölgesi 15 günlük raporu.\n"
        + "/kizilcahamam  : Kızılcahamam bölgesi 15 günlük raporu.\n"
    )

def yamanlar(update: Update, context: CallbackContext):
    update.message.reply_photo(
        photo=open("image_Yamanlar.png", "rb"),
        caption="Yamanlar bölgesi son 15 günün yağış bilgisi",
    )

def balcova(update: Update, context: CallbackContext):
    update.message.reply_photo(
        photo=open("image_Balcova.png", "rb"),
        caption="Balçova bölgesi son 15 günün yağış bilgisi",
    )

def kaynaklar(update: Update, context: CallbackContext):
    update.message.reply_photo(
        photo=open("image_Kaynaklar.png", "rb"),
        caption="Kaynaklar bölgesi son 15 günün yağış bilgisi",
    )

def kizilcahamam(update: Update, context: CallbackContext):
    update.message.reply_photo(
        photo=open("image_Kizilcahamam.png", "rb"),
        caption="Kızılcahamam bölgesi son 15 günün yağış bilgisi",
    )
    

if __name__ == "__main__":

    api = open("botapi.txt", "r").read()
    updater = Updater(api, use_context=True)
    last15daysReport()

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.dispatcher.add_handler(CommandHandler("yamanlar", yamanlar))
    updater.dispatcher.add_handler(CommandHandler("balcova", balcova))
    updater.dispatcher.add_handler(CommandHandler("kaynaklar", kaynaklar))
    updater.dispatcher.add_handler(CommandHandler("kizilcahamam", kizilcahamam))
    updater.dispatcher.add_handler(CommandHandler("coord", coord))
    updater.dispatcher.add_handler(MessageHandler(Filters.location, location))

    updater.start_polling()
    updater.idle()
