// https://stackoverflow.com/a/1421988
// Handy JS function to check if value is a number
function isNumber(n) { return !isNaN(parseFloat(n)) && !isNaN(n - 0) }

// Imagine base 27
var nextNodeLetter = 1;

function getNodeLetter() {
    let result = nextNodeLetter;

    nextNodeLetter = String.fromCodePoint(nextNodeLetter);

    // Explode 

    return result;
}

function numberToExcel(n) {
    if (!isNumber(n)) { return ""; }
    if (n == 0) { return ""; }
    
    // Turn integers into Excel counting
    // e.g.  1 ->  A
    //       2 ->  B
    //      ...
    //      25 ->  Y
    //      26 ->  Z
    //      27 -> AA
    //      28 -> AB etc.

    // Start at 26^1 and then increment
    // the power and divide by this value
    // until we consumes the entire input
    let base = 26;
    let divisor = base;
    let result = "";

    do {
        remainder = n % base || base;
        result = String.fromCodePoint(64 + remainder) + result;
        
        n = Math.floor(n / divisor);
        divisor *= base;
    } while (n > 0 && remainder != base);

    return result;
}

window.addEventListener("load", (event) => {
    const daWorkArea = document.getElementById("da-workarea");

    for (let i = 1; i <= 300; i++) {
        console.log(i + " -> " + numberToExcel(i));
    }
});

function createNode(x, y) {
    // Create div
    // Assign class
    // Assign event handlers

    if (!isNumber(x)) { x = 0; }
    if (!isNumber(y)) { y = 0; }

    let radius = 10;

    let newNode = document.createElement("div");
    newNode.classList.add("da-node");
    newNode.setAttribute("width", radius + "px");
    newNode.setAttribute("height", radius + "px");

    daWorkArea.append(newNode);
}