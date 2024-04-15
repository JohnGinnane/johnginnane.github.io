const minValue = 1;
const maxValue = 10;
var guessNumber = 1;
var hideNumbers = true;


document.addEventListener('DOMContentLoaded', function(){ 
    let taGuess = document.getElementById("input-lab-10-guess");
    taGuess.value = minValue;
    taGuess.setAttribute("value", minValue);

    let generateButtons = document.querySelectorAll("button.button-lab-10-generate");
    console.log(generateButtons);
    for (button of generateButtons) {
        generateRandomNumbers(button);
    }
});

function generateRandomNumbers(sender) {
    let parentDiv = sender.parentElement;
    let taNumberElements = parentDiv.querySelectorAll("textarea");

    for (element of taNumberElements) {
        let randomInt = Math.floor(Number(Math.random() * maxValue) + minValue);
        element.value = randomInt;
        element.setAttribute("value", randomInt);
    }

    countOccurrences();
    findLargestNumber();
    findMeanAndSum();
}

function countOccurrences() {
    let occurrences = 0;

    let taNumberElements = document.querySelectorAll("#div-lab-10-q3 textarea");

    for (element of taNumberElements) {
        let randomNumber = Number(element.value);
        if (randomNumber == guessNumber) {
            occurrences++;
        }
    }

    let taOccurrences = document.getElementById("input-lab-10-occurrences");
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
    let randomNumberClasses = document.querySelectorAll("#div-lab-10-q3 textarea");
    let showHideToggle = document.getElementById("button-lab-10-toggle-blur");

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

function findLargestNumber() {
    let largestNumber = minValue;
    let taNumberElements = document.querySelectorAll("#div-lab-10-q4 textarea");

    for (element of taNumberElements) {
        let number = Number(element.value);

        if (number > largestNumber) {
            largestNumber = number;
        }
    }

    let taLargestNumber = document.getElementById("input-lab-10-largest-number");
    taLargestNumber.value = largestNumber;
    taLargestNumber.setAttribute("value", largestNumber);
}

function findMeanAndSum() {
    let mean = 0;
    let sum = 0;
    
    let taNumberElements = document.querySelectorAll("#div-lab-10-q5 textarea");

    for (element of taNumberElements) {
        let number = Number(element.value);

        sum += number;
    }

    mean = sum / taNumberElements.length;

    let taArrayMean = document.getElementById("input-lab-10-array-mean");
    let taArraySum = document.getElementById("input-lab-10-array-sum");

    taArrayMean.value = mean.toFixed(1);
    taArrayMean.setAttribute("value", mean.toFixed(1));

    taArraySum.value = sum;
    taArraySum.setAttribute("value", sum);
}