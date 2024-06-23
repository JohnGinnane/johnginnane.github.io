let clickDetails = {
    startTime: new Date(),
    endTime: null,
    startX: null,
    startY: null,
    endX: null,
    endY: null
}

var varRoot = document.querySelector(":root");
var gameOrigin = {};
var ships = [];

let dragDetails = {
    lastX: 0,
    lastY: 0,
    X: 0,
    Y: 0,
    lastPiece: null
}

function setDragDetails(p) {
    dragDetails.lastX = dragDetails.X;
    dragDetails.lastY = dragDetails.Y;
    dragDetails.X = p.x;
    dragDetails.Y = p.y;
}

function checkDragDetails() {
    return (dragDetails.X !=  dragDetails.lastX || dragDetails.Y != dragDetails.lastY);
}

function getCSSVar(field) {
    return getComputedStyle(varRoot).getPropertyValue(field);
}

function setCSSVar(field, value) {
    varRoot.style.setProperty(field, value);
}

function pointInBox(p, b) {
    return (p.x >= b.left && p.x <= b.right &&
            p.y >= b.top  && p.y <= b.bottom);
}

function debugCoords(p) {
    let spanX = document.getElementById("span-battleship-x");
    let spanY = document.getElementById("span-battleship-y");

    spanX.innerText = p.x;
    spanY.innerText = p.y;
}

$(document).on("mousemove", function(event) {
    let p = new Vector2(event.pageX, event.pageY);
    let mouseX = document.getElementById("span-battleship-mouse-x");
    let mouseY = document.getElementById("span-battleship-mouse-y");

    mouseX.innerText = p.x;
    mouseY.innerText = p.y;
});

function isNumber(n) {
    if (!n) { return false; }
    if (typeof n !== "number") { return false; }

    return true;
}

// https://www.w3schools.com/howto/howto_js_draggable.asp
function makeDraggable(element) {
    console.log("make drag: " + element.id);
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    
    function dragMouseDown(e) {
        clickDetails.startTime = new Date();
        clickDetails.startX = e.clientX;
        clickDetails.startY = e.clientY;
        clickDetails.endTime = null;
        clickDetails.endX = null;
        clickDetails.endY = null;
        
        e = e || window.event;
        e.preventDefault();

        console.log("Started drag");

        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();

        // Calculate new cursorspot position
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;

        let pos = new Vector2((element.offsetLeft - pos1), (element.offsetTop - pos2));
        
        debugCoords(pos);

        let scale = parseInt(getCSSVar("--scale"));
        let shipOrigin = pos.add(scale/2, scale/2);

        element.style.top = pos.y + "px";
        element.style.left = pos.x + "px";

        let predictedPlace = globalToGrid(shipOrigin);

        // Move this into the ship class
        // If the ship's grid changes then update
        // the ship's tiles and select them using
        // the below class
        if (predictedPlace) {
            setDragDetails(predictedPlace);
            let piece = getTile(predictedPlace);
            
            if (piece != null) {
                // Change the previous piece to 
                // not be "selected"
                if (dragDetails.lastPiece != null) {
                    dragDetails.lastPiece.style.background = getCSSVar("--water");
                }

                piece.style.background = getCSSVar("--waterSelected");
                dragDetails.lastPiece = piece;
            }
        }
    }

    function closeDragElement(e) {
        clickDetails.endTime = new Date();
        clickDetails.endX = e.clientX;
        clickDetails.endY = e.clientY;

        document.onmouseup = null;
        document.onmousemove = null;

        console.log("Stopped drag");

        // If we didn't move the mouse then rotate
        if (clickDetails.startX === clickDetails.endX &&
            clickDetails.startY === clickDetails.endY) {
            for (let i = 0; i < ships.length; i++) {
                let s = ships[i];
                
                if (s.uuid == element.id) {
                    s.rotate();
                }
            }
        }
    }
    
    element.onmousedown = dragMouseDown;
    element.style.cursor = "move";
}

// https://stackoverflow.com/a/2117523
function uuidv4() {
    return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c =>
      (+c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> +c / 4).toString(16)
    );
}

class ship {
    constructor(len, x, y) {
        if (!isNumber(len) ||
            !isNumber(x)   ||
            !isNumber(y)) {
            return;
        }
        
        if (len < 0 || x < 0 || y < 0) { return; }
        
        this.len = len;
        this.height = 1;
        this.pos = new Vector2(x, y);
        this.uuid = uuidv4();
        this.angle = 0;
        this.tilePosition = new Vector2(0, 0);

        //console.log("Created a ship " + len + " tiles long at [" + x + ", " + y + "]");

        // Add the HTML of the ship to the page
        let group = document.getElementById("div-ships-group");
        let innerHTML = "<div id=\"" + this.uuid + "\" class=\"div-ship\"><div class=\"dot\"></div></div>";
        group.innerHTML += innerHTML;
        
        let element = this.element();
        element.style.top = this.pos.y + "px";
        element.style.left = this.pos.x + "px";
        element.style.width = (parseInt(getCSSVar("--scale")) * this.len) + "px";
    }

    getOrigin() {
        let output = new Vector2();

        return output
    }

    element() {
        return document.getElementById(this.uuid);
    }

    rotate() {
        this.angle = (this.angle + 90) % 360;
        let e = this.element();
        e.classList.toggle("div-rotate-90");
        console.log("rotate");
    }
}

function getTile(p) {
    // Find piece using co-ords
    let pieceClass = ".div-battleship-grid-piece";
    pieceClass += ".grid-x-" + p.x;
    pieceClass += ".grid-y-" + p.y;
    return document.querySelector(pieceClass);
}

function tileUnderPoint(p) {
    let predictedPlace = globalToGrid(p);
    return getTile(predictedPlace);
}

function globalToGrid(p) {
    if (!p) { return; }
    if (!isNumber(p.x)) { return; }
    if (!isNumber(p.y)) { return; }

    let scale = parseInt(getCSSVar("--scale"));

    // Subtract the grid origin from the
    // centre of the draggable element
    // Then divide by the scale to get
    // the integer co-ordinate of the grid
    return new Vector2(Math.floor((p.x - gameOrigin.x) / scale),
                       Math.floor((p.y - gameOrigin.y) / scale));
}

$(document).ready(function() {
    console.log("Started: " + new Date())
    // Create grid
    innerHTML = "";
    
    for (let y = 0; y < 10; y++) {
        innerHTML += "<div class='row'>\n";

        for (let x = 0; x < 10; x++) {
            innerHTML += "\t<div class='div-battleship-grid-piece grid-x-" + x + " grid-y-" + y + "'></div>\n";
        }

        innerHTML += "</div>\n";
    }
    
    $("#div-battleship-grid").html(innerHTML);

    gameOrigin = new Vector2($("#div-battleship-grid").offset().left, 
                              $("#div-battleship-grid").offset().top);

    // Mark element as "draggable"
    //makeDraggable(document.getElementById("div-draggable-root"));

    for (let i = 0; i < 3; i++) {
        let h = 5 + i * (parseInt(getCSSVar("--scale")) + 5)
        ships[i] = new ship(i+2, 5, h)
    }

    for (let i = 0; i < ships.length; i++) {
        // We have to add event handlers AFTER
        // the innerHTML is set
        makeDraggable(ships[i].element());
    }
});
