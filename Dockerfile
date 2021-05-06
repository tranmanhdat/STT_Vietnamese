FROM wav2letter/wav2letter:inference-latest
RUN echo "nameserver 8.8.8.8" >> /etc/resolv.conf
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install flask \
    && pip install pydub \
    && pip install pyopenssl
RUN mkdir /home/src
WORKDIR /home/src
COPY . /home/src

# ENTRYPOINT ["python", "server.py"]
