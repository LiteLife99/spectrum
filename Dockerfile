FROM python:3.8-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN apt-get update && \
    apt-get clean && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

CMD ["gunicorn", "wsgi:app", "-w", "4", "-b", "0.0.0.0:8081"]

EXPOSE 8081