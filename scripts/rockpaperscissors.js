window.addEventListener("load", (event) => {
    // I accidentally scared myself when I played the audio 33 times in one second
    // so I'm implementing a 'watch dog' to stop that from happening again
    SOUND_COOLDOWN = 1000; // ms
    NEXT_SOUND_TIME = Date.now();

    imgPlayerSelectedMove = document.getElementById("img-player-selected-move");
    imgComputerSelectedMove = document.getElementById("img-computer-selected-move");
    useVolumeToggle = document.getElementById("use-volume-toggle");

    computerSelectedMove = 0;
    lastComputerSelectedMove = 0;

    // Global vars
    playerSelectedMove = -1;
    gameInPlay = false;

    computerSelection = Math.random() * 10;
    computerSelectionSpeed = 10;

    moves = ["rock", "paper", "scissors"];

    emojiQuestionMark = "../media/images/emoji-question-mark-w10.png"
    emojiRock         = "../media/images/emoji-raised-fist-w10.png"
    emojiPaper        = "../media/images/emoji-raised-hand-w10.png"
    emojiScissors     = "../media/images/emoji-victory-hand-w10.png"

    divComputerRock     = document.getElementById("rps-div-computer-rock");
    divComputerPaper    = document.getElementById("rps-div-computer-paper");
    divComputerScissors = document.getElementById("rps-div-computer-scissors");

    canvas = document.getElementById("canvas");
    context = canvas.getContext("2d");
    
    windowResized(null);
    lastUpdate = Date.now();

    confetti = new Array();

    function update() {
        // DeltaTime is in seconds
        let deltaTime = (Date.now() - lastUpdate) / 1000;
        lastUpdate = Date.now();

        // Reduce computerSelectionSpeed
        if (gameInPlay) {
            // Cycle through computer's moves like a slot machine almost
            // Apply 'drag' to selection speed
            if (computerSelectionSpeed >= 1) {
                computerSelectionSpeed -= computerSelectionSpeed * 0.98 * deltaTime;
                
                // Iterate up the selection
                computerSelection += computerSelectionSpeed * 2 * deltaTime;

                // Computer can only pick between 0, 1, and 2
                lastComputerSelectedMove = computerSelectedMove;
                computerSelectedMove = Math.floor(computerSelection % 3);
                
                if (lastComputerSelectedMove != computerSelectedMove) {
                    // Apply the 'hover' colour to the computer's move
                    divComputerRock.classList.remove("computer-hover");
                    divComputerPaper.classList.remove("computer-hover");
                    divComputerScissors.classList.remove("computer-hover");

                    // Highlight the hovered piece
                    switch (computerSelectedMove) {
                        case 0:
                            divComputerRock.classList.add("computer-hover");
                            break;

                        case 1:
                            divComputerPaper.classList.add("computer-hover");
                            break;

                        case 2:
                            divComputerScissors.classList.add("computer-hover");
                            break;
                    }

                    if (getVolumeToggle()) {
                        // Credit: https://freesound.org/people/Glitched7777/sounds/723291/
                        audioDing = new Audio("../media/sound/doding.wav");
                        audioDing.volume = 0.3;
                        audioDing.play();
                    }
                }
            }

            // Once we slow down enough then stop the movement and pick this move
            // set speed to -1 so as to not trigger this if statement lots of times
            if (computerSelectionSpeed < 1 && computerSelectionSpeed > 0) {
                computerSelectionSpeed = -1;
                setTimeout(determineWinner, 500, playerSelectedMove, computerSelectedMove % moves.length);
            }

        }
        
        // Render the confetti 
        context.clearRect(0, 0, windowWidth, windowHeight);
        for (let k = 0; k < confetti.length; k++) {
            let v = confetti[k];

            if (v) {
                v.update(deltaTime);
                v.draw(context);
            }
        }

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

function toggleVolume(sender) {
    if (sender.classList.contains("active")) {
        useVolumeToggle.setAttribute("href", "#volume-up-fill");
    } else {
        useVolumeToggle.setAttribute("href", "#volume-mute-fill");
    }
}

function getVolumeToggle() {
    return useVolumeToggle.getAttribute("href") == "#volume-up-fill";
}

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
        
        confetti[confetti.length + i] = new ConfettiItem(pos, vel, 5, "hsl(" + Math.random() * 360 + ", 100%, 50%)");
    }
}

function playerSelected(sender, strMove) {
    if (gameInPlay) { return; }

    playerSelectedMove = 0;
    for (let i = 0; i < moves.length; i++) {
        if (strMove == moves[i]) {
            playerSelectedMove = i;
            break;
        }
    }

    imgPlayerSelectedMove.src = getEmojiPicture(moves[playerSelectedMove]);

    play();
}

function computerSelected(move) {
    // Reveal the computer's selected move
    imgComputerSelectedMove.src = getEmojiPicture(moves[move]);
}

function play() {
    gameInPlay = true;

    computerSelectionSpeed = 10;
    computerSelection = Math.random() * 100;    
    imgComputerSelectedMove.src = emojiQuestionMark;
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

function determineWinner(playerMove, computerMove) {
    if (!gameInPlay) { return; }

    computerSelected(computerMove);

    let outcome = "lose";

    // I know comparing numbers is better for the computer
    // but comparing strings is better for the human
    if (playerMove == computerMove) {
        outcome = "draw";
    } else if (moves[playerMove] == "rock" && moves[computerMove] == "scissors")  {
        outcome = "win";
    } else if (moves[playerMove] == "paper" && moves[computerMove] == "rock") {
        outcome = "win";
    } else if (moves[playerMove] == "scissors" && moves[computerMove] == "paper") {
        outcome = "win";
    }

    let audioPath = "";

    if (outcome == "win") {
        // yippee!
        spawnConfetti(Math.floor(25 + Math.random() * 10));
        randomNum = Math.floor(Math.random() * 5) + 1;
        // Credit for party horn: https://pixabay.com/sound-effects/party-horn-68443/
        audioPath = "../media/sound/party-horn-" + randomNum + ".mp3";
        $("#h1-modal-title").html("You win!");
    } else if (outcome == "lose") {
        audioPath = "../media/sound/boowomp.mp3";
        $("#h1-modal-title").html("You lost!");
    } else {
        audioPath = "../media/sound/crowd-oooh.wav";
        $("#h1-modal-title").html("It's a draw!");
    }

    $("#divGameOutcomeModal").modal('show');

    if (audioPath !== "" && NEXT_SOUND_TIME <= Date.now() && getVolumeToggle()) {
        NEXT_SOUND_TIME = Date.now() + SOUND_COOLDOWN;
        let audio = new Audio(audioPath);
        audio.play();
    }

    gameInPlay = false;
}