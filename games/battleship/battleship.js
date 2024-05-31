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
    dragDetails.X = p.X;
    dragDetails.Y = p.Y;
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
    return (p.X >= b.left && p.X <= b.right &&
            p.Y >= b.top  && p.Y <= b.bottom);
}

function vec2(x, y) {
    return {X: x, Y: y};
}

function debugCoords(p) {
    let spanX = document.getElementById("span-battleship-x");
    let spanY = document.getElementById("span-battleship-y");

    spanX.innerText = p.X;
    spanY.innerText = p.Y;
}

$(document).on("mousemove", function(event) {
    let p = vec2(event.pageX, event.pageY);
    let mouseX = document.getElementById("span-battleship-mouse-x");
    let mouseY = document.getElementById("span-battleship-mouse-y");

    mouseX.innerText = p.X;
    mouseY.innerText = p.Y;
});

$(document).on("touchmove", function(event) {
    let touch = e.changedTouches[1];

    if (touch != null) {
        let p = vec2(touch.pageX, touch.pageY);
        let mouseX = document.getElementById("span-battleship-mouse-x");
        let mouseY = document.getElementById("span-battleship-mouse-y");

        mouseX.innerText = p.X;
        mouseY.innerText = p.Y;
    }
});

$(document).ready(function() {
    // Create grid
    innerHTML = "";
    
    for (let y = 0; y < 10; y++) {
        innerHTML += "<div class='row'>\n";

        for (let x = 0; x < 10; x++) {
            innerHTML += "\t<div class='div-battleship-grid-piece grid-x-" + x + " grid-y-" + y + "'></div>\n";
        }

        innerHTML += "</div>\n";
    }
    
    debugCoords(gameOrigin);

    $("#div-battleship-grid").html(innerHTML);

    gameOrigin.X = $("#div-battleship-grid").offset().left;
    gameOrigin.Y = $("#div-battleship-grid").offset().top;

    // Mark element as "draggable"
    makeDraggable(document.getElementById("div-draggable-root"));

    function makeDraggable(element) {
        var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
        let header = document.getElementById(element.id + "-body")
        if (header) {
            header.onmousedown = dragMouseDown;
            header.touchstart = dragMouseDown;
        } else {
            element.onmousedown = dragMouseDown;
            element.touchstart = dragMouseDown;
        }

        function dragMouseDown(e) {
            clickDetails.startTime = new Date();
            clickDetails.startX = e.clientX;
            clickDetails.startY = e.clientY;
            clickDetails.endTime = null;
            clickDetails.endX = null;
            clickDetails.endY = null;
                
            e = e || window.event;
            e.preventDefault();

            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;
            document.onmousemove = elementDrag;
            document.touchend = closeDragElement;
            document.touchmove = elementDrag;
        }

        function elementDrag(e) {
            e = e || window.event;
            e.preventDefault();

            // Calculate new cursor position
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;

            let x = (element.offsetLeft - pos1);
            let y = (element.offsetTop - pos2);
            debugCoords(vec2(x, y));

            element.style.top = y + "px";
            element.style.left = x + "px";

            let scale = parseInt(getCSSVar("--scale"));
            let centre = vec2(x, y);

            // Subtract the grid origin from the
            // centre of the draggable element
            // Then divide by the scale to get
            // the integer co-ordinate of the grid
            let predictedPlace = {
                X: Math.round((centre.X - gameOrigin.X) / scale),
                Y: Math.round((centre.Y - gameOrigin.Y) / scale)
            };

            setDragDetails(predictedPlace);
            
            // Find piece using co-ords
            let pieceClass = ".div-battleship-grid-piece";
            pieceClass += ".grid-x-" + predictedPlace.X;
            pieceClass += ".grid-y-" + predictedPlace.Y;
            let piece = document.querySelector(pieceClass);
            
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

        function closeDragElement(e) {
            clickDetails.endTime = new Date();
            clickDetails.endX = e.clientX;
            clickDetails.endY = e.clientY;

            document.onmouseup = null;
            document.onmousemove = null;
            document.touchend = null;
            document.touchmove = null;

            if (clickDetails.startX === clickDetails.endX &&
                clickDetails.startY === clickDetails.endY) {
                console.log("rotate");

                element.classList.toggle("div-rotate-90");
            }
        }
    }
});