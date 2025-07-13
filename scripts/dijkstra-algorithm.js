// Returns a random UUID of specified length
function generateNewID(length) {
    length = length || 4;

    let newID = "";

    // Functions to check if a specified ID is present
    let checkNodes = x => nodes.find(y => y.id == x);
    let checkLinks = x => links.find(y => y.id == x);

    // Keep generating new IDs until we find one that is unique
    while (newID == "" || checkNodes(newID) || checkLinks(newID)) {
        // Keep appending the new ID until it's long enough
        while (newID.length < length) {
            newID += crypto.randomUUID().replaceAll("-", "");
        }
        
        // Then truncate to match length
        newID = newID.substring(1, length+1); // Add 1 as substring doesn't include last character
    }

    return newID;
}

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

// Structure of NODE object
var nodeTemplate = {
    x:       0,
    y:       0,
    name:    "",
    id:      "",
    divNode: null
}

// Structure of LINK object
var linkTemplate = {
    nodeA:    null,
    nodeB:    null,
    id:       "",
    distance: 0,
    divLink:  null
}

var nodes = [];
var links = []

function getFreeID() {
    let newID = null;

    // Generate ID and check if it's free
    while(true) {
        newID = generateNewID(4);
        let inUse = false;

        // Check nodes
        if (!inUse) {
            for (let node in nodes) {
                if (node.id == newID) {
                    inUse = true;
                    break;
                }
            }   
        }

        // Check links
        if (!inUse) {
            for (let link in links) {
                if (link.id == newID) {
                    inUse = true;
                    break;
                }
            }
        }

        // If the ID definitely isn't in use then
        // break out of the loop
        if (!inUse) { break; }
    }

    return newID;
}

// https://www.w3schools.com/howto/howto_js_draggable.asp
function dragElement(el) {
    var originX = 0, originY = 0, currentX = 0, currentY = 0;

    el.onmousedown = nodeMouseDown;

    function nodeMouseDown(e) {
        e = e || window.event;
        e.preventDefault();

        if (e == null) { return; }
        if (e.target == null) { return; }

        let sender = e.target;

        if (sender.classList.contains("da-node-ring")) {
            // Do linking
            // Set the origin of the line on the node pls
            // originX = e.clientX;
            // originY = e.clientY;
            let offsets = sender.getBoundingClientRect();
            originX = offsets.left + offsets.width / 2;
            originY = offsets.top  + offsets.height / 2;

            currentX = e.clientX;
            currentY = e.clientY;            

            document.onmouseup = closeLinkElement;
            document.onmousemove = elementLink;

            // Find existing link and delete it
            let divLink = document.getElementById("link-div");

            if (divLink) {
                divLink.parentElement.removeChild(divLink);
            }
        
            // Create a line from this node
            divLink = document.createElement("div");
            divLink.id = "link-div";
            divLink.style.left = (currentX + originX) / 2 + "px";
            divLink.style.top = (currentY + originY) / 2 + "px";

            sender.parentElement.append(divLink);

            return
        }

        if (e.target.classList.contains("da-node")) {
            // Do dragging
            currentX = e.clientX;
            currentY = e.clientY;

            document.onmouseup = closeDragElement;
            document.onmousemove = elementDrag;

            return;
        }
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        let divNode = nodes.find((x) => x.id == el.id);
                
        // Calculate new positions
        originX = currentX - e.clientX;
        originY = currentY - e.clientY;
        currentX = e.clientX;
        currentY = e.clientY;

        // Set element top and left position
        el.style.top = (el.offsetTop - originY) + "px";
        el.style.left = (el.offsetLeft - originX) + "px";
    }

    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
    }

    function elementLink(e) {
        // Calculate new positions
        // Use this to draw a line
        // from the first node to
        // the cursor
        
        e = e || window.event;
        e.preventDefault();
        
        // Calculate new positions
        currentX = e.clientX;
        currentY = e.clientY;

        // Place the div between original 
        // node and cursor?
        let divLink = document.getElementById("link-div")

        if (!divLink) { return; }

        divLink.style.left = originX + "px";
        divLink.style.top = originY + "px";
        
        // Calculate angle
        // https://stackoverflow.com/a/15994225
        let dX = currentX - originX;
        let dY = currentY - originY;
        let ang = Math.atan2(dY, dX);

        // Elongate
        divLink.style.width = Math.sqrt(Math.pow((currentX - originX), 2) + Math.pow((currentY - originY), 2)) + "px";
        divLink.style.height = "1px"
        
        divLink.style.rotate = ang + "rad";
    }
    
    function closeLinkElement(e) {
        document.onmouseup = null;
        document.onmousemove = null;

        // Somehow check if we're hovering over
        // another node or node ring
        if (!e) { return; }
        if (!e.target) { return; }

        let divLink = document.getElementById("link-div");
        if (!divLink) { return; }

        // Try to find the node we're attaching to (if any)
        let node;

        if (e.target.classList.contains("da-node")) {
            node = e.target.parentElement;
        } else if (e.target.classList.contains("da-node-ring")) {
            node = e.target;
        }

        if (!node) {
            // Didn't mouseup over node, so delete link
            divLink.parentElement.removeChild(divLink);
            return;
        }
        
        // Attach the other end of the link to the node
        let nodeBounds = node.getBoundingClientRect();

        if (divLink) {
            currentX = nodeBounds.left + nodeBounds.width  / 2
            currentY = nodeBounds.top  + nodeBounds.height / 2
            let dX = currentX - originX;
            let dY = currentY - originY;
            let ang = Math.atan2(dY, dX);

            // Elongate
            divLink.style.width = Math.sqrt(Math.pow((currentX - originX), 2) + Math.pow((currentY - originY), 2)) + "px";
            divLink.style.height = "1px"
            
            divLink.style.rotate = ang + "rad";

            // Give it a new unique ID pls
            //divLink.id = generateNewID(4)
        }
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

        // Ring used to attach links 
        // between nodes
        let nodeRing = document.createElement("div");
        nodeRing.classList.add("da-node-ring");
        
        nodeRing.style.left = x + "px";
        nodeRing.style.top = y + "px";

        let node = document.createElement("div");
        node.classList.add("da-node");
        node.setAttribute("header", "true");

        // Add the node letter inside the
        // node, centered perfectly
        let nodeText = document.createElement("p");
        nodeText.classList.add("da-node-p");
        nodeText.innerHTML = numberToExcel(nextNodeLetter++);
        
        nodeRing.append(node);
        nodeRing.append(nodeText);
        daWorkArea.append(nodeRing);

        
        // Find index, use it to stamp the node for ease of access
        let nodeIndex = nodes.length;
        nodeRing.setAttribute("nodeIndex", nodeIndex);
        
        // Clone the template
        let newNode = {...nodeTemplate};
        newNode.x = x;
        newNode.y = y;
        newNode.divNodeBase = nodeRing;
        newNode.id = getFreeID();

        nodeRing.id = newNode.id;
        newNode.divNode = nodeRing;
        nodes[nodeIndex] = newNode;

        dragElement(nodeRing);
    }

    $("#da-btn-add-node").on("click", createNode);

    createNode();
    createNode(20, 50);
});
