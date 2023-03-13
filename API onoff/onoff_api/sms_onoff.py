import requests
import json
import time

# Fonction pour envoyer un SMS via l'API OnOff
def send_sms(api_key, api_secret, sender, recipient, message):
    # Configuration de l'URL de l'API OnOff
    url = 'https://api.onoff.app/v1/sms/send'
    
    # Configuration des paramètres de la requête POST
    payload = {
        "sender": sender,
        "recipient": recipient,
        "message": message
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}:{api_secret}"
    }
    
    # Envoi de la requête POST
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    
    # Vérification de la réponse de l'API OnOff
    if response.status_code == 200:
        return True
    else:
        return False


# Fonction pour envoyer des SMS à une liste de destinataires
def send_sms_to_list(api_key, api_secret, sender, recipient_list, message):
    # Envoi des SMS à chaque destinataire de la liste
    for recipient in recipient_list:
        # Envoi du SMS à l'aide de la fonction send_sms
        result = send_sms(api_key, api_secret, sender, recipient, message)
        
        # Vérification du résultat de l'envoi du SMS et affichage d'un message en conséquence
        if result:
            print(f"SMS envoyé à {recipient}")
        else:
            print(f"Erreur lors de l'envoi du SMS à {recipient}")

        # Pause de 7 secondes avant l'envoi du prochain SMS
        time.sleep(7)
