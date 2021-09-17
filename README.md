# pnk_speech_command_recognition
Vietnamese speech command recognition

## Setup web demo with docker
```
git clone http://gitlab.phenikaa.local.com/hieuhv/asr
cd asr
sudo docker run -it --net host --name asr_demo -v <path_to_save_data_collection>:/home/asr/files hieuhv94/asr:v1.0
```
Go to ASR web demo at https://0.0.0.0:5000/