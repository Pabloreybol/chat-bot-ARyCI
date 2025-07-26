from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "¡Bot ARyCI listo para recibir mensajes!"

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "")
    sender = request.values.get("From", "")

    # Procesar el mensaje con ChatGPT
    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un asistente profesional para una empresa de arquitectura llamada ARyCI."},
            {"role": "user", "content": incoming_msg}
        ]
    )

    reply = respuesta["choices"][0]["message"]["content"]

    # Crear respuesta para Twilio
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(reply)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

