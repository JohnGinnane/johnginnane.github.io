// https://stackoverflow.com/a/1421988
// Handy JS function to check if value is a number
function isNumber(n) { return !isNaN(parseFloat(n)) && !isNaN(n - 0) }

var nextNodeLetter = 1;

// Takes in a positive non-zero integer
// returns the Excel column equivalent
// eg. 1 -> A
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

// https://www.w3schools.com/howto/howto_js_draggable.asp
function dragElement(el) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

    // If this is the header bit then add handler
    if (el.getAttribute("header") == "true") {
        el.onmousedown = dragMouseDown;
    }

    function dragMouseDown(e) {
        // Make sure we're hovering
        // over the node and not the
        // linking ring
        console.log(e);

        e = e || window.event;
        e.preventDefault();

        if (e == null) { return; }
        if (e.target == null) { return; }

        console.log(e.target);

        pos3 = e.clientX;
        pos4 = e.clientY;

        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        
        // Calculate new positions
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;

        // Set element top and left position
        el.style.top = (el.offsetTop - pos2) + "px";
        el.style.left = (el.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
    }
}
    
window.addEventListener("load", (event) => {
    const daWorkArea = document.getElementById("da-workarea");
    
    // Must define this function here when the page 
    // has finished loading
    function createNode(x, y) {
        // Create div
        // Assign class
        // Assign event handlers
    
        if (!isNumber(x)) { x = 0; }
        if (!isNumber(y)) { y = 0; }

        let nodeBase = document.createElement("div");
        nodeBase.classList.add("da-node-header");
        nodeBase.setAttribute("header", "true");

        nodeBase.style.left = x + "px";
        nodeBase.style.top = y + "px";

        // Ring used to attach links 
        // between nodes
        let nodeRing = document.createElement("div");
        nodeRing.classList.add("da-node-ring");
        
        // Add the node letter inside the
        // node, centered perfectly
        let nodeText = document.createElement("p");
        nodeText.classList.add("da-node-p");
        nodeText.innerHTML = numberToExcel(nextNodeLetter++);
        
        nodeBase.append(nodeText);
        nodeBase.append(nodeRing);
        daWorkArea.append(nodeBase);

        dragElement(nodeBase);
    }

    $("#da-btn-add-node").on("click", createNode);

    createNode();
    createNode(20, 50);
});
