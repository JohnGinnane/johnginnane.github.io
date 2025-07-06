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

    // Start at 26 and then multiply by 26
    // each iteration. Get the remainder
    // of n/26^x and turn into a letter
    let base = 26;
    let divisor = base;
    let result = "";

    do {
        // Get remainder of base
        // Because n mod n = 0 
        // I need to do || base
        // to return 26 when
        // n = 26
        remainder = n % base || base;

        // Convert to letter
        result = String.fromCodePoint(64 + remainder) + result;
        
        // Divide the parameter value 
        // to "consume it"
        n = Math.floor(n / divisor);
        // Multiply our base to power
        // it up
        divisor *= base;

        // Continue so long as input
        // is > 0 AND the remainder
        // is not the highest value
        // i.e. 26 (Z)
        // This stops us doing one
        // more iteration when the 
        // input number happens to
        // be divisible by 26
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