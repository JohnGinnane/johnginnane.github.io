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

    findMeanAndSum();
}

function findMeanAndSum() {
    let mean = 0;
    let sum = 0;
    
    let taNumberElements = document.getElementsByClassName("ta-lab10-random-number");

    for (element of taNumberElements) {
        let number = Number(element.value);

        sum += number;
    }

    mean = sum / taNumberElements.length;

    let taArrayMean = document.getElementById("input-lab10-array-mean");
    let taArraySum = document.getElementById("input-lab10-array-sum");

    taArrayMean.value = mean.toFixed(1);
    taArrayMean.setAttribute("value", mean.toFixed(1));

    taArraySum.value = sum;
    taArraySum.setAttribute("value", sum);
}