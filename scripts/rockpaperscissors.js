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

    canvas = document.getElementById("canvas");
    context = canvas.getContext("2d");
    
    windowResized(null);
    lastUpdate = Date.now();

    confetti = new Array();

    function update() {
        // DeltaTime is in seconds
        let deltaTime = (Date.now() - lastUpdate) / 1000;
        lastUpdate = Date.now();

        context.clearRect(0, 0, windowWidth, windowHeight);
        for (let k = 0; k < confetti.length; k++) {
            let v = confetti[k];

            if (v) {
                v.update(deltaTime);
                v.draw(context);
            }
        }

        let count = confetti.length;
        // Delete confetti that are off screen
        for (let k = confetti.length - 1; k >= 0; k--) {
            let v = confetti[k];

            if (v) {
                if (v.pos.y > windowHeight) {
                    confetti.splice(k, 1)
                }
            }
        }
    }

    setInterval(update, 1);
    
    window.addEventListener('resize', windowResized, true);

});

function windowResized(event) {
    windowWidth = window.innerWidth;
    windowHeight = window.innerHeight;

    canvas.width = windowWidth;
    canvas.height = windowHeight;
    
}

var ConfettiItem = function(pos, vel, radius, colour) {
    this.pos = pos;
    this.vel = vel;
    this.radius = radius;
    this.colour = colour;

    this.update = function(deltaTime) {
        this.pos = this.pos.add(this.vel.mul(deltaTime));
        let newVel = this.vel;

        // Drag
        newVel = newVel.add(newVel.mul(-0.1 * deltaTime));
        // Gravity
        newVel = newVel.add(0, 981 * deltaTime * 3);

        this.vel = newVel;
    }

    this.draw = function(context) {
        context.beginPath();
        context.arc(this.pos.x, this.pos.y, this.radius, 0, Math.PI*2);
        context.fillStyle = this.colour;
        context.fill();
    }
}

function spawnConfetti(amount) {
    // Would be nice if the confetti was to "spin" and have rotation
    for (var i = 0; i < amount; i++) {
        let pos = new Vector2(windowWidth / 2, windowHeight - 10);
        let vel = new Vector2((Math.random() - 0.5) * windowWidth / 2, (-windowHeight + (Math.random() - 0.5) * -windowHeight / 2) * 1.5);
        
        confetti[i] = new ConfettiItem(pos, vel, 5, "hsl(" + Math.random() * 360 + ", 100%, 50%)");
    }
}
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

    let outcome = "lose";

    if (playerSelectedMove == computerSelectedMove) {
        outcome = "draw";
    } else if (playerSelectedMove == "rock" && computerSelectedMove == "scissors")  {
        outcome = "win";
    } else if (playerSelectedMove == "paper" && computerSelectedMove == "rock") {
        outcome = "win";
    } else if (playerSelectedMove == "scissors" && computerSelectedMove == "paper") {
        outcome = "win";
    }

    let audioPath = "";

    if (outcome == "win") {
        spawnConfetti(Math.floor(25 + Math.random() * 10));

        randomNum = Math.floor(Math.random() * 5) + 1;
        audioPath = "../media/sound/party-horn-" + randomNum + ".mp3";
    } else if (outcome == "lose") {
        audioPath = "../media/sound/boowomp.mp3";
    } else {
        audioPath = "../media/sound/crowd-oooh.wav";
    }

    if (audioPath !== "") {        
        var audio = new Audio(audioPath);
        audio.play();
    }

    gameInPlay = false;
}