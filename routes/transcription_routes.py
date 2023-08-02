from email import utils
from flask import Blueprint, request, make_response
import uuid
import os
import traceback
import requests
import base64
from utils.audioUtil import extract_transcription

transcription_router = Blueprint('transcription', __name__)

@transcription_router.route('/transcribe', methods = ['POST'])
def transcribe():
    try:
        request_body = request.get_json()
        print("request_body:", request_body)
        source = request_body.get("source", "")
        filename = str(uuid.uuid4()) + '.mp3'
        if (source == 'base64_encoded_file'): 
            base64EncodedFile = request_body.get('base64_encoded_file')
            decoded_file = base64.b64decode(base64EncodedFile)
            with open(filename, 'wb') as fp: 
                fp.write(decoded_file)
        elif (source == 'presigned_url'):
            url = request_body.get('presigned_url')
            resp = requests.get(url)
            with open(filename, 'wb') as fp:
                fp.write(resp.content)
        else:
            raise Exception("This source is not supported")

        transcription = extract_transcription(filename)
        
        os.remove(filename)

        response_data = {
            'success' : 1,
            'transcription': transcription['transcription_text'],
            'language': transcription['language']
        }

        status_code = 200

        response = make_response(response_data, status_code)

        return response 
   
    except Exception as e:
        print(e)
        traceback.print_exc()

        #TO-DO remove locally saved file from here as well

        response_data = {
            'success': 0,
            'errorMessage': "Error with /transcribe -> " + str(e)
        }

        status_code = 500

        response = make_response(response_data, status_code)
        
        return response 

