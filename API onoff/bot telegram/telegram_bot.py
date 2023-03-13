import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from api_onoff import send_sms

# Configurer le bot avec votre token d'API Telegram
updater = Updater(token='5853801750:AAEM4BETpexvRPOX4XRYoG3NT97kkltKeTo', use_context=True)

# Obtenir le gestionnaire de mise à jour à partir de l'updater
dispatcher = updater.dispatcher

# Activer les journaux pour aider à déboguer les problèmes
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Définir la fonction de gestion de la commande /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bonjour! Envoyez /help pour voir les commandes disponibles.")

# Définir la fonction de gestion de la commande /help
def help(update, context):
    help_message = """
    Voici les commandes disponibles:
    /start - Démarrer le bot
    /help - Voir les commandes disponibles
    /sms - Envoyer un SMS avec OnOff
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)

# Définir la fonction de gestion de la commande /sms
def sms(update, context):
    # Vérifier si l'utilisateur a fourni un numéro et un message
    if len(context.args) < 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Veuillez fournir le numéro et le message. Exemple: /sms 0601020304 Bonjour!")
        return

    # Récupérer le numéro et le message
    phone_number = context.args[0]
    message = ' '.join(context.args[1:])

    # Envoyer le message avec l'API OnOff
    response = send_sms(phone_number, message)

    # Vérifier si le message a été envoyé avec succès
    if response.status_code == 200:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Le message a été envoyé avec succès!")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Une erreur s'est produite lors de l'envoi du message. Veuillez réessayer plus tard.")

# Définir la fonction de gestion des messages reçus
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

# Ajouter les gestionnaires de commandes et de messages au dispatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

sms_handler = CommandHandler('sms', sms)
dispatcher.add_handler(sms_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

# Démarrer le bot
updater.start_polling()
