#https://hub.docker.com/r/nikolaik/python-nodejs
FROM nikolaik/python-nodejs:python3.10-nodejs20

RUN apt update && apt install -y \
    portaudio19-dev \
    llvm

# Install python libraries
RUN pip install numpy==1.26.0
RUN pip install flask==2.3.3 flask_socketio==5.3.6 google-cloud-speech==2.21.0 google-cloud-texttospeech==2.14.1 openai==0.28.0 scipy==1.11.2 pyaudio==0.2.13 librosa==0.10.1  pylint==2.17.5 pytest==7.4.2 pytest-cov==4.1.0
