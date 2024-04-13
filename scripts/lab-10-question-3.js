const minValue = 1;
const maxValue = 10;
var guessNumber = 1;
var hideNumbers = true;


document.addEventListener('DOMContentLoaded', function(){ 
    let taGuess = document.getElementById("input-lab10-guess");
    taGuess.value = minValue;
    taGuess.setAttribute("value", minValue);
    generateRandomNumbers();
});

function generateRandomNumbers() {
    let taNumberElements = document.getElementsByClassName("ta-lab10-random-number");

    for (element of taNumberElements) {
        let randomInt = Math.floor(Number(Math.random() * maxValue) + minValue);
        element.value = randomInt;
        element.setAttribute("value", randomInt);
    }

    countOccurrences();
}

function countOccurrences() {
    let occurrences = 0;

    let taNumberElements = document.getElementsByClassName("ta-lab10-random-number");

    for (element of taNumberElements) {
        let randomNumber = Number(element.value);
        if (randomNumber == guessNumber) {
            occurrences++;
        }
    }

    let taOccurrences = document.getElementById("input-lab10-occurrences");
    taOccurrences.value = occurrences;
    taOccurrences.setAttribute("value", occurrences);
}

function guessChanged(sender) {
    if (!sender) { return; }

    guessNumber = Number(sender.value);

    if (guessNumber < minValue) {
        sender.value = minValue;
        sender.setAttribute("value", minValue);
        guessNumber = minValue;
    } else if (guessNumber > maxValue) {
        sender.value = maxValue;
        sender.setAttribute("value", maxValue)
        guessNumber = maxValue;
    }

    countOccurrences();
}

function toggleBlur(sender) {
    let randomNumberClasses = document.getElementsByClassName("ta-lab10-random-number");
    let showHideToggle = document.getElementById("button-lab10-toggle-blur");

    hideNumbers = !hideNumbers;

    if (!hideNumbers) {
        showHideToggle.innerHTML = "Hide";
    } else {
        showHideToggle.innerHTML = "Show";
    }

    for (element of randomNumberClasses) {
        if (hideNumbers) {
            element.style.filter = "blur(5px)";
        } else {
            element.style.filter = "none";
        }
    } 
}