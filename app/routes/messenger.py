import os
import re

import requests
from dotenv import load_dotenv
from fastapi import Request, APIRouter

from app.utils import regexes

load_dotenv()
TOKEN = os.getenv('TOKEN')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

router = APIRouter(
    prefix='/webhook',
    tags=['webhook']
)


@router.get('/')
def webhook(request: Request):
    verify_token = request.query_params.get('hub.verify_token')
    # Check if sent token is correct
    if verify_token == VERIFY_TOKEN:
        # Responds with the challenge token from the request
        print('Responding with the challenge...')
        return int(request.query_params.get('hub.challenge'))
    return 'Unable to authorise.'


@router.post('/')
def webhook(request: dict):
    message = request['entry'][0]['messaging'][0]['message']
    sender_id = request['entry'][0]['messaging'][0]['sender']['id']
    if message['text']:

        response_msg = 'No, you!'

        split = message['text'].split()
        if len(split) >= 2 and split[0] == '!register':
            email = split[1]
            if re.fullmatch(regexes.email, email):
                # TODO create user
                pass
            else:
                response_msg = 'Invalid email!'

        request_body = {
            'recipient': {
                'id': sender_id
            },
            'message': {"text": response_msg}
        }

        response = requests.post(
            url=f'https://graph.facebook.com/v12.0/me/messages?access_token={TOKEN}',
            json=request_body) \
            .json()

        return response
    return 'ok'
