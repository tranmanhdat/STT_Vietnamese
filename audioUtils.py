from pydub import AudioSegment
file_name = "/tmp/temp.wav" 
def standard_file(path):
    wav_file = AudioSegment.from_file(file=path)
    wav_file = wav_file.set_frame_rate(16000)
    wav_file = wav_file.set_sample_width(2)
    wav_file = wav_file.set_channels(1)
    wav_file.export(file_name, bitrate="256", format='wav')
    