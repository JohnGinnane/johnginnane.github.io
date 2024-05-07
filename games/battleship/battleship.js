let clickDetails = {
    startTime: new Date(),
    endTime: null,
    startX: null,
    startY: null,
    endX: null,
    endY: null
}

$(document).ready(function() {
    // Create grid
    innerHTML = "";

    for (let y = 0; y < 10; y++) {
        innerHTML += "<div class='row'>\n";

        for (let x = 0; x < 10; x++) {
            innerHTML += "\t<div class='div-battleship-grid-piece'></div>\n";
        }

        innerHTML += "</div>\n";
    }

    $("#div-battleship-grid").html(innerHTML);

    // Mark element as "draggable"
    makeDraggable(document.getElementById("div-draggable-test"));

    function makeDraggable(element) {
        var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
        let header = document.getElementById(element.id + "-header")
        if (header) {
            header.onmousedown = dragMouseDown;
        } else {
            element.onmousedown = dragMouseDown;
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
        }

        function elementDrag(e) {
            e = e || window.event;
            e.preventDefault();

            // Calculate new cursor position
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;

            element.style.top = (element.offsetTop - pos2) + "px";
            element.style.left = (element.offsetLeft - pos1) + "px";
        }

        function closeDragElement(e) {
            clickDetails.endTime = new Date();
            clickDetails.endX = e.clientX;
            clickDetails.endY = e.clientY;

            document.onmouseup = null;
            document.onmousemove = null;

            if (clickDetails.startX === clickDetails.endX &&
                clickDetails.startY === clickDetails.endY) {
                console.log("rotate");

                element.classList.toggle("div-rotate-90");
            }
        }
    }

});