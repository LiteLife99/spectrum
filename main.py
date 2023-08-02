from flask import Flask
from routes.diarization_routes import diarization_router
from routes.transcription_routes import transcription_router

app = Flask(__name__)

@app.route('/healthCheck',methods = ['GET'])
def healthCheck():
   return 'I am healthy!'

app.register_blueprint(diarization_router, url_prefix='/diarization')
app.register_blueprint(transcription_router, url_prefix='/transcription')