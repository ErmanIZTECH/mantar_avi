from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from main import last15daysReport

if __name__ == "__main__" :
    

    last15daysReport() 
    bot_api = open('botapi.txt','rb')
    updater = Updater(bot_api, 
                    use_context=True)

    def start(update: Update, context: CallbackContext):
            update.message.reply_text(
            "Merhaba *man-tar* mantar avlarında kullanılmak üzere yazılmış bir telegram botudur.\n"+
            "Komuları görmek için /help komutunu kullanın.")

    def help(update: Update, context: CallbackContext):
            update.message.reply_text( 
            "/start : Genel bilgilendirme mesajını gösterir.\n"+
            "/help : Komutları listeler.\n"+
            "/yamanlar : Yamanlar bölgesi 15 günlük raporu.\n"+
            "/balcova : balcova bölgesi 15 günlük raporu.\n"+
            "/kaynaklar : kaynaklar bölgesi 15 günlük raporu.\n")

    def yamanlar(update: Update, context: CallbackContext):
            update.message.reply_photo(photo=open('image_Yamanlar.png','rb'), 
            caption = "Yamanlar bölgesi son 15 günün yağış bilgisi")
    def balcova(update: Update, context: CallbackContext):
            update.message.reply_photo(photo=open('image_Balcova.png','rb'),
            caption = "Balçova bölgesi son 15 günün yağış bilgisi")
    def kaynaklar(update: Update, context: CallbackContext):
            update.message.reply_photo(photo=open('image_Kaynaklar.png','rb'),
            caption = "Kaynaklar bölgesi son 15 günün yağış bilgisi")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('yamanlar', yamanlar))
    updater.dispatcher.add_handler(CommandHandler('balcova', balcova))
    updater.dispatcher.add_handler(CommandHandler('kaynaklar', kaynaklar))

    updater.start_polling()