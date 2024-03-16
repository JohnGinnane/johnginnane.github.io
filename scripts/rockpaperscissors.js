window.addEventListener("load", (event) => {
    console.log("page is fully loaded");
    
    divPlayerSelected = document.getElementById("div-player-selected");
    divCPUSelected = document.getElementById("div-computer-selected");

  });

var playerSelectedMove = "";
var gameInPlay = false;
var computerMoveTime = 1000;

function playerSelected(sender) {
    divCPUSelected.innerHTML = "❓";
    let move = sender.querySelector(".rps-playable").innerHTML;
    playerSelectedMove = move;
    
    divPlayerSelected.innerHTML = move;
    console.log("playerSelectedMove: " + playerSelectedMove);

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
    console.log("computerSelectedMove: " + computerSelectedMove);
    divCPUSelected.innerHTML = computerSelectedMove;

    let playerWin = false;
    if (playerSelectedMove == "✊" && computerSelectedMove == "✌")  {
        playerWin = true;
    } else if (playerSelectedMove == "✋" && computerSelectedMove == "✊") {
        playerWin = true;
    } else if (playerSelectedMove == "✌" && computerSelectedMove == "✋") {
        playerWin = true;
    }

    if (playerWin) {
        randomNum = Math.floor(Math.random() * 5) + 1;
        let audioPath = "../media/sound/party-horn-" + randomNum + ".mp3";
        console.log(audioPath);
        var audio = new Audio(audioPath);
        audio.play();
    }

    gameInPlay = false;
}