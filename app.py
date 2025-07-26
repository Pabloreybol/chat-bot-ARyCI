from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Clave de API de OpenAI tomada desde variables de entorno (Render)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ruta base para confirmar que el bot está corriendo correctamente
@app.route("/", methods=["GET"])
def home():
    return "¡Bot ARyCI está activo y listo para recibir mensajes por WhatsApp!"

# Webhook que Twilio llamará al recibir un mensaje
@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "")
    sender = request.values.get("From", "")

    # Llamada a la API de OpenAI (GPT)
    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un asistente profesional para una empresa de arquitectura llamada ARyCI. Brinda respuestas claras, útiles y profesionales."},
            {"role": "user", "content": incoming_msg}
        ]
    )

    reply = respuesta["choices"][0]["message"]["content"]

    # Crear la respuesta de WhatsApp a través de Twilio
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(reply)
    return str(resp)

# Este bloque permite que el servidor escuche en el puerto necesario (Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render asigna automáticamente el puerto
    app.run(host="0.0.0.0", port=port)

