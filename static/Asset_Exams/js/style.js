$(document).ready(function() {
    //=============VARIABLE
    var lst_ques = $("#lstQues").val();
    var ques_Arr = lst_ques.split("/*?space?*/");
    ques_Arr.pop();
    var isRecord = false;
    var isTrue = true;
    var point = 0;
    if (sessionStorage && sessionStorage.getItem("point")) {
        point = sessionStorage.getItem("point");
    } else {
        sessionStorage.setItem("point", point.toString());
    }

    $("#mypoint").text(point);
    $("#progress-bar").css("width", point.toString() + "%");
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
            $(".recording-group").css("display", "flex");
        } else if (isRecord) { //stop record
            $(this).text("Bắt đầu nói");
            isRecord = false;
            $(".recording-group").css("display", "none");
            let text_random = $("#text-random").val();
            let text_record = $("#textTrans").val();
            //compare text
            isTrue = compareText(text_random, text_record);
            //

        }
    });
    //====================Check
    $("#check").click(function() {
        if (isTrue) {
            $("#check-div").css("display", "none");
            $("#check-true").css("display", "flex");
            $("#footer").css("background", "#d7ffb8");
        } else {
            $("#check-div").css("display", "none");
            $("#check-fail").css("display", "flex");
            $("#footer").css("background", "#ffdfe0");
        }
    });
    //================Continue
    $(".continue").click(function() {
        if (isTrue) {
            point = Number(point) + 10;
            sessionStorage.setItem("point", point.toString());
            $("#mypoint").text(point);
        }
        //random text here
        let randTextval = getRandomQues(ques_Arr);
        if (randTextval != false) {
            $("#text-random").val(randTextval);
        } else {
            sessionStorage.setItem("point", "0");
            alert("Hoàn thành bài thi! Bạn đã đạt được" + point + " điểm!");
            window.parent.location.reload();
        }
        //end random
        $("#progress-bar").css("width", point.toString() + "%");
        $("#progress-bar").text(point.toString() + "%");
        $("#check-div").css("display", "flex");
        $("#footer").css("background", "transparent");
        $("#check-true").css("display", "none");
        $("#check-fail").css("display", "none");
    });
    $(".skip-btn").click(function() {
        point = point != 0 ? Number(point) - 10 : 0;
        sessionStorage.setItem("point", point.toString());
        $("#mypoint").text(point);
        //random text here
        let randTextval = getRandomQues(ques_Arr);
        if (randTextval != false) {
            $("#text-random").val(randTextval);
        } else {
            sessionStorage.setItem("point", "0");
            alert("Hoàn thành bài thi! Bạn đã đạt được" + point + " điểm!");
            window.parent.location.reload();
        }
        //end random
        $("#progress-bar").css("width", point.toString() + "%");
        $("#progress-bar").text(point.toString() + "%");
        $("#check-div").css("display", "flex");
        $("#footer").css("background", "transparent");
        $("#check-true").css("display", "none");
        $("#check-fail").css("display", "none");
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

function compareText(text_random, text_record) {
    $.ajax({
        url: '/sendPlt',
        type: 'post',
        data: {
            text_random: text_random,
            text_record: text_record
        },
        dataType: "json",
        success: function(res) {

        },
        error: function(error) {
            console.log(error);
        }
    })
    return true;
}