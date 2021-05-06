//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; //stream from getUserMedia()
var recorder; //WebAudioRecorder object
var input; //MediaStreamAudioSourceNode  we'll be recording
var encodingType; //holds selected encoding for resulting audio (file)
var encodeAfterRecord = true; // when to encode


const SILENT_THRESHOLD = 1000;
const SILENT_DURATION = 2;
var isStop = true;
var isDone = false;
var ws;
var buffer;
var result;
var countSilentDuration = 0;
// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //new audio context to help us record

var recordButton = document.getElementById("recordButton");
var streamButton = document.getElementById("streamButton");
//add events to those 2 buttons

var isRecord = false;
var isTrue = true;
var point = 0;
var rangeTest=0;
var data;
$(document).ready(function() {
    //=============VARIABLE
    var lst_ques = $("#lstQues").val();
    var ques_Arr = lst_ques.split("/*?space?*/");
    ques_Arr.pop();
    if (sessionStorage && sessionStorage.getItem("point")) {
        point = sessionStorage.getItem("point");
    } else {
        sessionStorage.setItem("point", point.toString());
    } 
    
    $("#mypoint").text(point);
    $("#progress-bar").css("width", rangeTest.toString() + "%");
    $("#progress-bar").text(point.toString() + "%");
    //=============RANDOM TEXT=====================
    let randTextval = getRandomQues(ques_Arr);
    if (randTextval != false) {
        $("#text-random").val(randTextval);
    } else {
        alert("Hoàn thành bài thi! Bạn đã đạt được" + point + " điểm!");
        sessionStorage.setItem("point", "0");
    }
    //=============
    $("#recordButton").click(function() {
        if (!isRecord) { //record
            $(this).text("Dừng nói");
            isRecord = true;
            $("#recording-group>p").text("Đang thu âm");
            $("#recording-group").css("display", "flex");
            startRecording();
        } else if (isRecord) { //stop record
            $(this).text("Bắt đầu nói");
            isRecord = false;
            stopRecording();
            $("#recording-group").css("display", "none");

            //compare text

            //

        }
    });
    //====================Check

    $("#check").click(function() { //cau khac
        // point = point != 0 ? Number(point) - 10 : 0;
        rangeTest=Number(rangeTest)+10;
        sessionStorage.setItem("point", point.toString());
        $("#mypoint").text(point);
        let randTextval = getRandomQues(ques_Arr);
        if (randTextval != false) {
            $("#text-random").val(randTextval);
        } else {
            sessionStorage.setItem("point", "0");
            alert("Hoàn thành bài thi! Bạn đã đạt được " + point + " điểm!");
            window.parent.location.reload();
        }
        $("#progress-bar").css("width", rangeTest.toString() + "%");
        $("#progress-bar").text(rangeTest.toString() + "%");
        $("#check-div").css("display", "flex");
        $("#footer").css("background", "transparent");
        $("#check-true").css("display", "none");
        $("#check-fail").css("display", "none");
        $("#textTrans").val("");
    });
    //================Continue
    $(".continue").click(function() {
        if (isTrue) {
            point = Number(point) + 10;
            sessionStorage.setItem("point", point.toString());
            $("#mypoint").text(point);
        }
        let randTextval = getRandomQues(ques_Arr);
        if (randTextval != false) {
            $("#text-random").val(randTextval);
        } else {
            sessionStorage.setItem("point", "0");
            alert("Hoàn thành bài thi! Bạn đã đạt được" + point + " điểm!");
            window.parent.location.reload();
        }
        rangeTest=Number(rangeTest)+10;
        $("#progress-bar").css("width", rangeTest.toString() + "%");
        $("#progress-bar").text(rangeTest.toString() + "%");
        $("#check-div").css("display", "flex");
        $("#footer").css("background", "transparent");
        $("#check-true").css("display", "none");
        $("#check-fail").css("display", "none");
        $("#textTrans").val("");
    });
    $(".skip-btn").click(function() { //quay lai
        window.location.href="/selectExams";
    });

});

function getRandomQues(ques_Arr) {
    var indexRand = Math.floor(Math.random() * ques_Arr.length); //get random key
    var res = ques_Arr[indexRand];
    console.log(indexRand);
    if (ques_Arr.length == 0) {
        return false
    }
    ques_Arr.splice(indexRand, 1);
    return res;
}

function checkSpeaking() {
    let text_random = $("#text-random").val();
    let text_record = $("#textTrans").val();
    $.ajax({
        url: '/compare',
        type: 'post',
        data: {
            text_random: text_random,
            text_record: text_record
        },
        dataType: "json",
        success: function(res) {
            if (res.res1 == 100) {
                $("#check-div").css("display", "none");
                $("#check-true").css("display", "flex");
                $("#footer").css("background", "#d7ffb8");
                isTrue = true;
            } else {
                $("#check-div").css("display", "none");
                $("#check-fail").css("display", "flex");
                $("#footer").css("background", "#ffdfe0");
                $("#accurate").text(res.res1);
                isTrue = false;
            }
        },
        error: function(error) {
            console.log(error);
        }
    })

}

function connect() {
    if (!isStop) {
        closeWS();
        stop();
        return;
    } else {
        document.getElementById("textTrans").value = "";
    }
    start()

    if (!audioContext) {
        // audioContext = new (window.AudioContext || window.webkitAudioContext)();
        audioContext = new AudioContext({ sampleRate: 16000, sampleSize: 16 });
        if (audioContext.state == 'suspended') {
            audioContext.resume();
        }
        navigator.mediaDevices.getUserMedia({ audio: true, video: false }).then(function(stream) {
            var audioInput = audioContext.createMediaStreamSource(stream);

            var bufferSize = 0;

            recorder = audioContext.createScriptProcessor(bufferSize, 1, 1);

            recorder.onaudioprocess = function(e) {
                if (!isStop && ws && ws.readyState == ws.OPEN) {
                    // if (countSilentDuration > SILENT_DURATION) {
                    //   closeWS();
                    //   stop();
                    //   countSilentDuration = 0;
                    //   return;
                    // }

                    buffer = e.inputBuffer.getChannelData(0);
                    // drawBuffer(buffer);
                    var int16ArrayData = convertFloat32ToInt16(buffer);
                    countSilentDuration += int16ArrayData.length / audioContext.sampleRate;
                    for (var i = 0; i < int16ArrayData.length; i++) {
                        if (Math.abs(int16ArrayData[i]) > SILENT_THRESHOLD) {
                            countSilentDuration = 0;
                            break;
                        }
                    }
                    data = new Int16Array(data.length + int16ArrayData.length)
                    data.set(data);
                    data.set(int16ArrayData, data.length)
                    ws.send(int16ArrayData.buffer);
                }
            };
            audioInput.connect(recorder);
            recorder.connect(audioContext.destination);
        }).catch(function(e) { console.log("Error in getUserMedia: ");
            console.log(e) });
    }
    initWebSocket(audioContext.sampleRate)
}

function initWebSocket(sampleRate) {
    start();
    // ws = new WebSocket('wss://172.17.0.1:5555');
    ws = new WebSocket('wss://172.17.0.1:5555');
    ws.onopen = function() {
        console.log("Opened connection to websocket");
    };

    ws.onclose = function() {
        console.log("Websocket closed");
        stop();
    };

    ws.onmessage = function(e) {
        document.getElementById("textTrans").value += e.data
    };

    return ws
}

function start() {
    isStop = false;
    document.getElementById("streamButton").innerHTML = "Stop";
}

function stop() {
    isStop = true;
    document.getElementById("streamButton").innerHTML = "Record";
    // document.getElementById("transcripted-text").value += "\n";
    const blob = new Blob([data], { type: 'audio/wav' });
    const url = URL.createObjectURL(blob);

    // Get DOM elements.
    const audio = document.getElementById('audio');
    const source = document.getElementById('source');

    // Insert blob object URL into audio element & play.
    source.src = url;
    audio.load();
    audio.play();
}

function closeWS() {
    // if (ws && ws.readyState == ws.OPEN) {
    //   ws.send("EOS");
    // }
    ws.close();
}

function convertFloat32ToInt16(float32ArrayData) {
    var l = float32ArrayData.length;
    var int16ArrayData = new Int16Array(l);
    while (l--) {
        int16ArrayData[l] = Math.min(1, float32ArrayData[l]) * 0x7FFF;
    }
    return int16ArrayData;
}



function startRecording() {
    console.log("startRecording() called");
    var constraints = { audio: true, video: false }
    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
        console.log("getUserMedia() success, stream created, initializing WebAudioRecorder...");
        audioContext = new AudioContext({ sampleRate: 16000, sampleSize: 16 });

        //assign to gumStream for later use
        gumStream = stream;

        /* use the stream */
        input = audioContext.createMediaStreamSource(stream);

        recorder = new WebAudioRecorder(input, {
            workerDir: "/static/js/", // must end with slash
            encoding: "wav",
            numChannels: 1, //2 is the default, mp3 encoding supports only 2
            onEncoderLoading: function(recorder, encoding) {
                // show "loading encoder..." display
                console.log("Loading " + encoding + " encoder...");
            },
            onEncoderLoaded: function(recorder, encoding) {
                // hide "loading encoder..." display
                console.log(encoding + " encoder loaded");
            }
        });

        recorder.onComplete = function(recorder, blob) {
            console.log("Encoding complete");
            createDownloadLink(blob, recorder.encoding);
        }

        recorder.setOptions({
            timeLimit: 120,
            encodeAfterRecord: "wav",
            ogg: { quality: 0.5 },
            mp3: { bitRate: 160 }
        });

        //start the recording process
        recorder.startRecording();

        console.log("Recording started");

    }).catch(function(err) {
        //enable the record button if getUSerMedia() fails
        // recordButton.disabled = false;
        // stopButton.disabled = true;

    });

}

function stopRecording() {
    console.log("stopRecording() called");

    //stop microphone access
    gumStream.getAudioTracks()[0].stop();



    //tell the recorder to finish the recording (stop recording + encode the recorded audio)
    recorder.finishRecording();

    console.log('Recording stopped');
    document.getElementById("textTrans").value = "Đang xử lý...Xin chờ trong giây lát";

    var xhr = new XMLHttpRequest();
    xhr.onload = function(e) {
        if (this.readyState === 4) {
            // console.log("Server returned: ",e.target.responseText);
            document.getElementById("textTrans").value = e.target.responseText;
            isDone = true;
            console.log(isDone);
        }
    };
}

function sd() {
    console.log("sd");
}

function createDownloadLink(blob, encoding) {

    var url = URL.createObjectURL(blob);
    var au = document.createElement('audio');
    var li = document.createElement('li');
    var link = document.createElement('a');

    //add controls to the <audio> element
    au.controls = true;
    au.src = url;

    //link the a element to the blob
    filename = new Date().toISOString() + '.' + encoding
    link.href = url;
    link.download = filename;
    link.innerHTML = link.download;

    // excute command
    var xhr = new XMLHttpRequest();
    xhr.onload = function(e) {
        if (this.readyState === 4) {
            console.log("Server returned1: ", e.target.responseText);
            document.getElementById("textTrans").value = e.target.responseText;
            checkSpeaking();
            //document.getElementById("progress").style.display = 'none'
        }
    };
    var fd = new FormData();
    fd.append("the_file", blob, filename);
    xhr.open("POST", "/recog", true);
    xhr.send(fd);
    //document.getElementById("progress").style.display = 'block'
    //add the new audio and a elements to the li element
    li.appendChild(au);
    //add the li element to the ordered list
    // while (recordAudio.hasChildNodes()) {
    // 	recordAudio.removeChild(recordAudio.lastChild);
    // }
    // recordAudio.appendChild(li);
}





function handleUploadFile() {
    const file = this.files[0]
    var au = document.createElement('audio');
    var li = document.createElement('li');
    //add controls to the <audio> element
    au.controls = true;
    au.src = URL.createObjectURL(file);
    li.appendChild(au)
    while (recordAudio.hasChildNodes()) {
        recordAudio.removeChild(recordAudio.lastChild);
    }
    recordAudio.appendChild(li);

    var xhr = new XMLHttpRequest();
    xhr.onload = function(e) {
        if (this.readyState === 4) {
            console.log("Server returnedwebtiengiet: ", e.target.responseText);
            document.getElementById("textTrans").value = e.target.responseText;
            document.getElementById("progress").style.display = 'none'
        }
    };
    var fd = new FormData();
    fd.append("the_file", file);
    xhr.open("POST", "/recog", true);
    xhr.send(fd);
    document.getElementById("progress").style.display = 'block'
}

function uploadWav() {
    document.getElementById("wav").click();
}

function uploadMp3() {
    document.getElementById("mp3").click();
}

function uploadFlac() {
    document.getElementById("flac").click();
}


function compareText(text_random, text_record) {

    return true;
}