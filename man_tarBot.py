from uuid import uuid4
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import main

if __name__ == "__main__":
    api = open("botapi.txt", "r").read()
    updater = Updater(api, use_context=True)

    def start(update: Update, context: CallbackContext):
        update.message.reply_text(
            "Merhaba *man-tar* mantar avlarında kullanılmak üzere yazılmış bir telegram botudur.\n"
            + "Komuları görmek için /help komutunu kullanın."
        )

    def coord(update):
        """Usage: /put value"""
        # Generate ID and separate value from command
        # We don't use context.args here, because the value may contain whitespaces
        value = update.message.text.partition(" ")[2]

        coordN = round(float(value.split()[0][0:7]), 3)
        coordE = round(float(value.split()[1][0:7]), 3)
        update.message.reply_text("Coordinates are: " + str([coordN, coordE]))
        main.getcoordinates(coordN, coordE)
        update.message.reply_photo(photo=open("coordinate_image.png", "rb"))

    def put(update, context):
        """Usage: /put value"""
        # Generate ID and separate value from command
        key = str(uuid4())
        # We don't use context.args here, because the value may contain whitespaces
        value = update.message.text.partition(" ")[2]

        # Store value
        context.user_data[key] = value
        # Send the key to the user
        update.message.reply_text(key)

    def get(update, context):
        """Usage: /get uuid"""
        # Separate ID from command
        key = context.args[0]

        # Load value and send it to the user
        value = context.user_data.get(key, "Not found")
        update.message.reply_text(value)

    def help(update: Update, context: CallbackContext):
        update.message.reply_text(
            "/start : Genel bilgilendirme mesajını gösterir.\n"
            + "/help : Komutları listeler.\n"
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

    def location(update, context):
        user_location = update.message.location
        user_location.latitude
        user_location.longitude
        print(user_location.longitude, user_location.latitude)
        main.getcoordinates(user_location.latitude, user_location.longitude)
        update.message.reply_photo(photo=open("coordinate_image.png", "rb"))

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.dispatcher.add_handler(CommandHandler("yamanlar", yamanlar))
    updater.dispatcher.add_handler(CommandHandler("balcova", balcova))
    updater.dispatcher.add_handler(CommandHandler("kaynaklar", kaynaklar))
    updater.dispatcher.add_handler(CommandHandler("kizilcahamam", kizilcahamam))
    updater.dispatcher.add_handler(CommandHandler("put", put))
    updater.dispatcher.add_handler(CommandHandler("get", get))
    updater.dispatcher.add_handler(CommandHandler("coord", coord))
    location_handler = MessageHandler(Filters.location, location)
    updater.dispatcher.add_handler(location_handler)

    updater.start_polling()
