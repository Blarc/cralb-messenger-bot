import requests, os
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()
TOKEN = os.getenv('TOKEN')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

app = Flask(__name__)


# Adds support for GET requests to our webhook
@app.route('/webhook', methods=['GET'])
def webhook():
    verify_token = request.args.get("hub.verify_token")
    # Check if sent token is correct
    if verify_token == VERIFY_TOKEN:
        # Responds with the challenge token from the request
        return request.args.get("hub.challenge")
    return 'Unable to authorise.'


@app.route('/webhook', methods=['POST'])
def webhook_test():
    data = request.get_json()
    message = data['entry'][0]['messaging'][0]['message']
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    if message['text']:
        request_body = {
            'recipient': {
                'id': sender_id
            },
            'message': {"text": "hello, world!"}
        }
        response = requests.post('https://graph.facebook.com/v12.0/me/messages?access_token=' + TOKEN,
                                 json=request_body).json()
        return response
    return 'ok'


if __name__ == "__main__":
    app.run(threaded=True, port=3000)
