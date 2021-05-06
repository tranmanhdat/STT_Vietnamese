from subprocess import Popen, PIPE
import os
import signal

model_path = "/root/src/asr/static/resources/model"
w2l_bin = "/root/wav2letter/build/inference/inference/examples/interactive_streaming_asr_example"
w2l_process = Popen(['{} --input_files_base_path={}'.format(w2l_bin, model_path)],
                      stdin=PIPE, stdout=PIPE, stderr=PIPE,
                      shell=True)
def speech2text():
    w2l_process.stdin.write(b"endtoken=DONE\n")
    w2l_process.stdin.write(b"input=/tmp/temp.wav\n")
    w2l_process.stdin.flush()
    trans = []
    while True:
        # read from process stdout
        output = w2l_process.stdout.readline().decode('utf-8').strip()
        if output == 'DONE':
            break
        else:
            seg = output.split(',')
            if seg[0].isnumeric() and seg[1].isnumeric() and seg[2]:
                trans.append(seg[2])
    return ' '.join(trans)