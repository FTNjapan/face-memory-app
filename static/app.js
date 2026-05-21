
/* =========================================================
   状態管理
========================================================= */
const state = {
    autoMode: false,
    timer: null,
    currentAnswer: ""
};

/* =========================================================
   初期ロード
========================================================= */
window.onload = loadTeams;

/* =========================================================
   チーム一覧取得
========================================================= */
function loadTeams(){

    fetch("/teams")
    .then(res => res.json())
    .then(data => {

        const area = document.getElementById("teamButtons");
        area.innerHTML = "";

        data.forEach(team => {

            const btn = document.createElement("button");
            btn.innerText = team;

            btn.onclick = () => startTeam(team);

            area.appendChild(btn);
        });
    });
}

/* =========================================================
   チーム開始
========================================================= */
function startTeam(team){

    fetch("/team/" + team)
    .then(() => {

        document.getElementById("teamScreen").style.display = "none";
        document.getElementById("quizScreen").style.display = "flex";

        nextImage();

        const autoEnabled =
            document.getElementById("autoToggle").checked;

        /* -----------------------------------------
           自動OFFならボタン全部消す
        ----------------------------------------- */
        if(!autoEnabled){

            document.getElementById("startAutoBtn").style.display = "none";
            document.getElementById("stopAutoBtn").style.display = "none";
        }

        /* -----------------------------------------
           自動ONならスタートボタンだけ表示
        ----------------------------------------- */
        if(autoEnabled){

            document.getElementById("startAutoBtn").style.display = "inline-block";
            document.getElementById("stopAutoBtn").style.display = "none";

            startAuto();
        }
    });
}

/* =========================================================
   次の画像
========================================================= */
function nextImage(){

    fetch("/next")
    .then(res => res.json())
    .then(data => {

        if(data.end){

            document.getElementById("name").innerText = "終了";
            return;
        }

        document.getElementById("img").src = data.image;

        state.currentAnswer = data.answer;

        document.getElementById("name").innerText = "";
    });
}

/* =========================================================
   答え表示
========================================================= */
function showAnswer(){

    document.getElementById("name").innerText =
        state.currentAnswer;
}

/* =========================================================
   カウントダウン
========================================================= */
function countdown(sec){

    let t = sec;

    document.getElementById("timer").innerText = t;

    clearInterval(state.timer);

    state.timer = setInterval(() => {

        t--;

        document.getElementById("timer").innerText = t;

        if(t <= 0){
            clearInterval(state.timer);
        }

    }, 1000);
}

/* =========================================================
   自動送り開始
========================================================= */
function startAuto(){

    state.autoMode = true;

    document.getElementById("manualControls").style.display = "none";

    /* -----------------------------------------
       ボタン制御
       スタート → 消す
       停止 → 出す
    ----------------------------------------- */
    document.getElementById("startAutoBtn").style.display = "none";
    document.getElementById("stopAutoBtn").style.display = "inline-block";

    function loop(){

        if(!state.autoMode) return;

        countdown(5);

        setTimeout(() => {

            if(!state.autoMode) return;

            showAnswer();

            countdown(2);

            setTimeout(() => {

                if(!state.autoMode) return;

                nextImage();

                loop();

            }, 2000);

        }, 5000);
    }

    loop();
}

/* =========================================================
   自動停止
========================================================= */
function stopAuto(){

    state.autoMode = false;

    clearInterval(state.timer);

    document.getElementById("manualControls").style.display = "block";

    document.getElementById("stopAutoBtn").style.display = "none";
    document.getElementById("startAutoBtn").style.display = "inline-block";
}

/* =========================================================
   チーム画面に戻る
========================================================= */
function backToTeam(){

    stopAuto();

    document.getElementById("quizScreen").style.display = "none";
    document.getElementById("teamScreen").style.display = "block";

    document.getElementById("img").src = "";
    document.getElementById("name").innerText = "";
    document.getElementById("timer").innerText = "";
}