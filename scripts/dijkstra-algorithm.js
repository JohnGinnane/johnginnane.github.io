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
        e = e || window.event;
        e.preventDefault();

        pos3 = e.clientX;
        pos4 = e.clientY;

        document.onmouseup = closeDragElement;
        document.onmousedown = elementDrag;
        console.log("dragMouseDown");
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
        console.log("elementDrag");
    }

    function closeDragElement() {
        document.onmouseup = null;
        document.onmousedown = null;
        console.log("closeDragElement");
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
        
        let newNode = document.createElement("div");
        newNode.classList.add("da-node-header");
        newNode.setAttribute("header", "true");

        newNode.style.left = x + "px";
        newNode.style.top = y + "px";

        // Add the node letter inside the
        // node, centered perfectly
        // let divInner = document.createElement("div");
        // divInner.classList.add("da-node-inner");
        
        let pNode = document.createElement("p");
        pNode.classList.add("da-node-p");
        pNode.innerHTML = numberToExcel(nextNodeLetter++);
                
        newNode.append(pNode);
        daWorkArea.append(newNode);

        dragElement(newNode);
    }

    createNode();
    createNode(20, 50);
});
