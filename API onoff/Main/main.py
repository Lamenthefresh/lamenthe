import time
import telegram
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from sms_onoff import send_sms_onoff

# Clé API Telegram
TELEGRAM_API_KEY = "votre_clé_api_telegram"

# Numéro OnOff et token API pour envoyer des SMS
ONOFF_NUMBER = "votre_numéro_onoff"
ONOFF_API_TOKEN = "votre_token_api_onoff"

# Fonction pour gérer la commande /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bonjour! Utilisez la commande /sms pour envoyer un SMS.")

# Fonction pour envoyer un SMS via OnOff
def send_sms(update, context):
    # Vérifier si l'utilisateur a bien entré un numéro de téléphone et un message
    if len(context.args) != 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Veuillez entrer un numéro de téléphone et un message.")
        return
    phone_number = context.args[0]
    message = context.args[1]
    # Envoyer le SMS via OnOff
    result = send_sms_onoff(phone_number, message, ONOFF_NUMBER, ONOFF_API_TOKEN)
    # Envoyer un message à l'utilisateur en fonction du résultat de l'envoi
    if result:
        context.bot.send_message(chat_id=update.effective_chat.id, text="SMS envoyé!")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Erreur lors de l'envoi du SMS.")

# Fonction pour gérer les messages non reconnus
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Commande non reconnue. Utilisez la commande /start pour commencer.")

# Créer un Updater pour gérer les mises à jour du bot Telegram
updater = Updater(token=TELEGRAM_API_KEY, use_context=True)

# Récupérer le Dispatcher pour enregistrer les gestionnaires de commandes et de messages
dispatcher = updater.dispatcher

# Enregistrer les gestionnaires de commandes et de messages
start_handler = CommandHandler('start', start)
send_sms_handler = CommandHandler('sms', send_sms)
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(send_sms_handler)
dispatcher.add_handler(unknown_handler)

# Démarrer le bot
updater.start_polling()

# Garder le bot actif
while True:
    time.sleep(1)
