from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Substitua pelos seus dados
TOKEN = 'YOUR_ACCESS_TOKEN'
PHONE_NUMBER_ID = 'YOUR_PHONE_NUMBER_ID'
API_URL = f'https://graph.facebook.com/v15.0/{PHONE_NUMBER_ID}/messages'

# Função para enviar mensagens
def enviar_mensagem(telefone, mensagem):
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json',
    }

    data = {
        "messaging_product": "whatsapp",
        "to": telefone,
        "text": {
            "body": mensagem
        }
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Erro ao enviar mensagem: {response.status_code}, {response.text}")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Processar a mensagem recebida
    numero_remetente = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    mensagem_recebida = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']

    # Resposta automática
    if 'oi' in mensagem_recebida.lower():
        resposta = "Olá! Como posso ajudar?"
    else:
        resposta = "Desculpe, não entendi. Pode reformular?"

    # Enviar resposta
    enviar_mensagem(numero_remetente, resposta)

    return jsonify({"status": "sucesso"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
