# spectrum
Spectrum is a Python microservice for speaker diarization and transcription using OpenAI's Whisper model.

Steps to run:

1) Create a new virual env : python3 -m venv spectrumEnv
2) Install dependencies : python3 -m pip install -r requirements.txt
3) Populate config.json as per your aws keys and hugging face token
4) Start the service : gunicorn wsgi:app -b 0.0.0.0:8081
5) Hit the api and enjoy

Recommended to use a gpu instance for faster performance as it will be too heavy for cpu.
