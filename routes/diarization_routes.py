from flask import Blueprint, request, make_response
import uuid
import traceback
import requests
import base64
import os
from utils.audioUtil import diarization

diarization_router = Blueprint('diarization', __name__)

@diarization_router.route('/diarize', methods = ['POST'])
def diarize():
    try:
        request_body = request.get_json()
        print("request_body:", request_body)
        source = request_body.get("source", "")
        min_speakers = request_body.get("min_speakers", 2)
        max_speakers = request_body.get("max_speakers", 2)
        if(min_speakers > max_speakers):
            raise Exception("Min Speakers cannot be greater than max speakers")
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

        #filename = '/home/ubuntu/documents/projects/sample_orig.wav'
        diarization_result = diarization(filename, min_speakers, max_speakers)
        
        os.remove(filename)

        response_data = {
            'success' : 1,
            'diarization': diarization_result['diarize_result'],
            'language': diarization_result['language']
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