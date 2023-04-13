import os
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from twilio.twiml.messaging_response import MessagingResponse
import openai

load_dotenv()

app = Flask(__name__)
CORS(app)

twilio_account_sid = os.environ['TWILIO_ACCOUNT_SID']
twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']
openai_api_key = os.environ['OPENAI_API_KEY']

openai.api_key = openai_api_key

@app.route('/sms', methods=['POST'])
def sms_reply():
    # Récupérez le message entrant
    incoming_msg = request.values.get('Body', '').strip()

    # Interagissez avec l'API ChatGPT
    chatgpt_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Utilisateur : {incoming_msg}\nAssistant :",
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["Utilisateur :", "Assistant :"]
    )

    # Obtenez la réponse de ChatGPT
    assistant_reply = chatgpt_response.choices[0].text.strip()

    # Créez une réponse Twilio
    response = MessagingResponse()
    response.message(assistant_reply)

    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
