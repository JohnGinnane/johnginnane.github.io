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
window.addEventListener("load", (event) => {
    const daWorkArea = document.getElementById("da-workarea");
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