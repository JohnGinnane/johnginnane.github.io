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
    
    windowWidth = window.innerWidth;
    windowHeight = window.innerHeight;

    canvas.width = windowWidth;
    canvas.height = windowHeight;

    lastUpdate = Date.now();

    confetti = new Array();

    test = false;

    function update() {
        let deltaTime = Date.now() - lastUpdate;
        lastUpdate = Date.now();

        let k = confetti.length;

        while (k > 0) {
            let v = confetti[k-1];

            if (v) {
                v.update(deltaTime);

                if (v.pos.y > window.innerHeight) {
                    confetti[k-1] = null;
                }
            }

            k--;
        }

        context.clearRect(0, 0, windowWidth, windowHeight);
        for (let k = 0; k < confetti.length; k++) {
            let v = confetti[k];
            v.draw(context);

            if (!test) {
                test = true;
                console.log(v);
            }
        }
    }

    setInterval(update, 1);
});

window.addEventListener('resize', function(event) {
    windowWidth = window.innerWidth;
    windowHeight = window.innerHeight;

    canvas.width = windowWidth;
    canvas.height = windowHeight;
}, true);

var ConfettiItem = function(pos, vel, radius, colour) {
    this.pos = pos;
    this.vel = vel;
    this.radius = radius;
    this.colour = colour;

    this.update = function(deltaTime) {
        this.pos = this.pos.add(this.vel);
        let newVel = this.vel;

        // Drag
        //newVel = newVel.add(newVel.mul(-0.1 * deltaTime));
        // Gravity
        //newVel = newVel.add(0, 1 * deltaTime);

        this.vel = newVel;
    }

    this.draw = function(context) {
        context.beginPath();
        context.arc(this.pos.x, this.pos.y, this.radius, 0, Math.PI*2);
        context.fillStyle = this.colour;
        context.fill();
    }
}

function spawnConfetti() {
    let CONFETTI_COUNT = 10;

    for (var i = 0; i < CONFETTI_COUNT; i++) {
        //let pos = new Vector2(windowWidth / 2, window.innerHeight - 10);
        let pos = new Vector2(windowWidth / 2, windowHeight / 2);
        //let vel = new Vector2((Math.random() - 1) * 10, -20 + Math.random() * -10)
        let vel = new Vector2();
        
        //hsl(" + Math.random() * 360 + ", 100%, 50%)
        confetti[i] = new ConfettiItem(pos, vel, 50, "red");
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
    spawnConfetti();

    if (outcome == "win") {
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