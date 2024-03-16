window.addEventListener("load", (event) => {
    divPlayerSelected = document.getElementById("div-player-selected");
    divCPUSelected = document.getElementById("div-computer-selected");
    
    // Global vars
    playerSelectedMove = "";
    gameInPlay = false;
    computerMoveTime = 1000;
  });


function playerSelected(sender) {
    divCPUSelected.innerHTML = "❓";
    let move = sender.querySelector(".rps-playable").innerHTML;
    playerSelectedMove = move;
    
    divPlayerSelected.innerHTML = move;

    if (!gameInPlay) {
        play();
    }
}

function play() {
    gameInPlay = true;
    setTimeout(computerSelected, computerMoveTime);
}

function computerSelected() {
    let randomNum = Math.floor(Math.random() * 3);
    let moves = ["✊", "✋", "✌"];
    let computerSelectedMove = moves[randomNum];
    divCPUSelected.innerHTML = computerSelectedMove;

    let playerWin = false;
    if (playerSelectedMove == "✊" && computerSelectedMove == "✌")  {
        playerWin = true;
    } else if (playerSelectedMove == "✋" && computerSelectedMove == "✊") {
        playerWin = true;
    } else if (playerSelectedMove == "✌" && computerSelectedMove == "✋") {
        playerWin = true;
    }

    let audioPath = "";

    if (playerWin) {
        randomNum = Math.floor(Math.random() * 5) + 1;
        audioPath = "../media/sound/party-horn-" + randomNum + ".mp3";
    } else {
        audioPath = "../media/sound/boowomp.mp3"
    }

    if (audioPath !== "") {        
        var audio = new Audio(audioPath);
        audio.play();
    }

    gameInPlay = false;
}