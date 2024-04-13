const minValue = 1;
const maxValue = 10;
var hideNumbers = true;

document.addEventListener('DOMContentLoaded', function() {
    generateRandomNumbers();
});

function generateRandomNumbers() {
    let taNumberElements = document.getElementsByClassName("ta-lab10-random-number");

    for (element of taNumberElements) {
        let randomInt = Math.floor(Number(Math.random() * maxValue) + minValue);
        element.value = randomInt;
        element.setAttribute("value", randomInt);
    }

    findLargestNumber();
}

function findLargestNumber() {
    let largestNumber = minValue;
    let taNumberElements = document.getElementsByClassName("ta-lab10-random-number");

    for (element of taNumberElements) {
        let number = Number(element.value);

        if (number > largestNumber) {
            largestNumber = number;
        }
    }

    let taLargestNumber = document.getElementById("input-lab10-largest-number");
    taLargestNumber.value = largestNumber;
    taLargestNumber.setAttribute("value", largestNumber);
}