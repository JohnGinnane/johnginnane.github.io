window.addEventListener("load", (event) => {
    imgPlayerSelectedMove = document.getElementById("img-player-selected-move");
    imgComputerSelectedMove = document.getElementById("img-computer-selected-move");
    
    // Global vars
    playerSelectedMove = "";
    gameInPlay = false;
    computerMoveTime = 1000;

    emojiQuestionMark = "../media/images/emoji-question-mark-w10.png"
    emojiRock         = "../media/images/emoji-raised-fist-w10.png"
    emojiPaper        = "../media/images/emoji-raised-hand-w10.png"
    emojiScissors     = "../media/images/emoji-victory-hand-w10.png"
  });


function playerSelected(sender, move) {
    if (gameInPlay) { return; }
    
    imgComputerSelectedMove.src = emojiQuestionMark;
    
    playerSelectedMove = move;
    imgPlayerSelectedMove.src = getEmojiPicture(move);
    
    if (!gameInPlay) {
        play();
    }
}

function play() {
    gameInPlay = true;
    setTimeout(computerSelected, computerMoveTime);
}

function getEmojiPicture(type) {
    switch (type) {
        case 'rock':
            return emojiRock;
        case 'paper':
            return emojiPaper;
        case 'scissors':
            return emojiScissors;
        default:
            return emojiQuestionMark;
    }

    return emojiQuestionMark;
}

function computerSelected() {
    let randomNum = Math.floor(Math.random() * 3);
    let moves = ["rock", "paper", "scissors"];
    let computerSelectedMove = moves[randomNum];
    imgComputerSelectedMove.src = getEmojiPicture(computerSelectedMove);

    let playerWin = false;
    if (playerSelectedMove == "rock" && computerSelectedMove == "scissors")  {
        playerWin = true;
    } else if (playerSelectedMove == "paper" && computerSelectedMove == "rock") {
        playerWin = true;
    } else if (playerSelectedMove == "scissors" && computerSelectedMove == "paper") {
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