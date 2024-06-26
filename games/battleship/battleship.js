const imgCarrier = new Image();
const imgBattleship = new Image();
const imgCruiser = new Image();
const imgSubmarine = new Image();
const imgDestroyer = new Image();

const RENDER_TARGET = 1000/60;
const UPDATE_TARGET = 1000/60;
const GAME_SCALE = 1;
var MOUSE_POS = new Vector2();

var ClickDetails = {
    pos1: 0,
    pos2: 0,
    pos3: 0,
    pos4: 0,

    StartTime: null,
    StartX: 0,
    StartY: 0,
    EndTime: null,
    EndX: 0,
    EndY: 0
}

function pad(str, len, chr) {
    if (chr == null || chr == "") {
        chr = " ";
    }

    if (len == null || len <= 0) {
        return str;
    }

    str = str.toString();

    while (str.length < len) {
        str = chr + str;
    }

    return str
}

class Ship {
    constructor(X, Y, Length) {
        this.Position = new Vector2(X, Y);
        this.Length = Length;
        this.GridPosition = new Vector2(0, 0);
        this.Image = null;
        this.ImageScale = 1;
    }

    update(ctx, delta) { }

    draw(ctx) {
        if (this.Image == null) {
            return;
        }

        ctx.save();
        
        ctx.imageSmoothingEnabled = false;
        let scaleWidth = this.Image.width * this.ImageScale * GAME_SCALE;
        let scaleHeight = this.Image.height * this.ImageScale * GAME_SCALE;
        
        ctx.translate(this.Position.x, this.Position.y);
        ctx.drawImage(this.Image, -scaleWidth/2, -scaleHeight/2, scaleWidth, scaleHeight);
        
        // Draw hitbox
        ctx.beginPath();
        
        if (this.mouseOver()) {
            ctx.strokeStyle = "green"
        } else {
            ctx.strokeStyle = "red";
        }
        ctx.strokeRect(-scaleWidth/2, -scaleHeight/2, scaleWidth, scaleHeight);

        ctx.restore();
    }

    mouseOver() {
        let scaleWidth = this.Image.width * this.ImageScale * GAME_SCALE;
        let scaleHeight = this.Image.height * this.ImageScale * GAME_SCALE;

        if (MOUSE_POS.x >= this.Position.x - scaleWidth/2 && 
            MOUSE_POS.x <= this.Position.x + scaleWidth/2 &&
            MOUSE_POS.y >= this.Position.y - scaleHeight/2 && 
            MOUSE_POS.y <= this.Position.y + scaleHeight/2) {
            return true;
        } else {
            return false;
        }        
    }
}

class AircraftCarrier extends Ship {
    constructor(X, Y, Length) {
        super(X, Y, Length);

        if (imgCarrier.src == null || imgCarrier.src == "") {
            imgCarrier.src = "img/Carrier/ShipCarrierHull.png"
        }

        this.Image = imgCarrier;
    }
}

class Battleship extends Ship {
    constructor(X, Y, Length) {
        super(X, Y, Length);

        if (imgBattleship.src == null || imgBattleship.src == "") {
            imgBattleship.src = "img/Battleship/ShipBattleshipHull.png"
        }

        this.Image = imgBattleship;
        this.ImageScale = 0.8;
    }
}

class Cruiser extends Ship {
    constructor(X, Y, Length) {
        super(X, Y, Length);

        if (imgCruiser.src == null || imgCruiser.src == "") {
            imgCruiser.src = "img/Cruiser/ShipCruiserHull.png";
        }

        this.Image = imgCruiser;
    }
}

class Submarine extends Ship {
    constructor(X, Y, Length) {
        super(X, Y, Length);

        if (imgSubmarine.src == null || imgSubmarine.src == "") {
            imgSubmarine.src = "img/Submarine/ShipSubMarineHull.png";
        }

        this.Image = imgSubmarine;
    }
}

class Destroyer extends Ship {
    constructor(X, Y, Length) {
        super(X, Y, Length);

        if (imgDestroyer.src == null || imgDestroyer.src == "") {
            imgDestroyer.src = "img/Destroyer/ShipDestroyerHull.png";
        }

        this.Image = imgDestroyer;
    }
}

function getCursorPosition(canvas, event) {
    const rect = canvas.getBoundingClientRect()
    MOUSE_POS = new Vector2(event.clientX - rect.left, event.clientY - rect.top);
}

$(document).ready(function() {
    const canvas = document.getElementById("canvas-battleship");
    const ctx = canvas.getContext("2d");
    var delta = 0;
    var lastTime = new Date();
    var SelectedShip = null;

    canvas.addEventListener("mousemove", function(e) {
        getCursorPosition(canvas, e)

        if (SelectedShip) {
            ClickDetails.pos1 = ClickDetails.pos3 - e.clientX;
            ClickDetails.pos2 = ClickDetails.pos4 - e.clientY;
            ClickDetails.pos3 = e.clientX;
            ClickDetails.pos4 = e.clientY;
            
            SelectedShip.Position = new Vector2(ClickDetails.pos1, ClickDetails.pos2);
        }
    });

    canvas.addEventListener("mousedown", function(e) {
        ClickDetails.StartTime = new Date();
        ClickDetails.StartX = e.clientX;
        ClickDetails.StartY = e.clientY;
        ClickDetails.EndTime = null;
        ClickDetails.EndX = null;
        ClickDetails.EndY = null;

        ClickDetails.pos3 = e.clientX;
        ClickDetails.pos4 = e.clientY;

        SelectedShip = null;
        for (let i = 0; i < ships.length; i++) {
            if (ships[i].mouseOver()) {
                SelectedShip = ships[i];
                break;
            }
        }
    });

    canvas.addEventListener("mouseup", function(e) {
        ClickDetails.StartTime = null;
        ClickDetails.StartX = null;
        ClickDetails.StartY = null;
        ClickDetails.EndTime = new Date();
        ClickDetails.EndX = e.clientX;
        ClickDetails.EndY = e.clientY;
        SelectedShip = null;
    });

    //window.requestAnimationFrame(draw);
    let Y = 250;
    let ships = [
        new AircraftCarrier(0, Y),
        new Battleship(80, Y),
        new Cruiser(160, Y),
        new Submarine(240, Y),
        new Destroyer(320, Y)
    ];

    let updateTime = 0.0
    let renderTime = 0.0

    function update() {
        let startUpdate = new Date();
        delta = new Date() - lastTime;
        lastTime = new Date();

        for (let i = 0; i < ships.length; i++) {
            let ship = ships[i];
            ship.update(ctx, delta);
        }

        updateTime = (new Date() - startUpdate);
    }

    function draw() {
        let startRender = new Date();

        // Clear the canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "rgb(50, 150, 255)"
        ctx.fillRect(0, 0, canvas.width, canvas.height)
        
        for (let i = 0; i < ships.length; i++) {
            let ship = ships[i];
            ship.draw(ctx);
        }
        
        renderTime = Math.abs(new Date() - startRender);

        // Draw debug figures
        ctx.font = "16px Consolas";

        if (updateTime > UPDATE_TARGET) {
            ctx.fillStyle = "rgb(255, 0, 0)";
        } else {
            ctx.fillStyle = "rgb(0, 0, 0)";
        }

        ctx.fillText("Update: " + pad(updateTime, 4) + "ms / " + Math.floor(UPDATE_TARGET).toFixed(0) + "ms", 4, 20);

        if (renderTime > RENDER_TARGET) {
            ctx.fillStyle = "rgb(255, 0, 0)";
        } else {
            ctx.fillStyle = "rgb(0, 0, 0)";
        }

        ctx.fillText("Render: " + pad(renderTime, 4) + "ms / " + Math.floor(RENDER_TARGET).toFixed(0) + "ms", 4, 40);
    }

    setInterval(update, UPDATE_TARGET);
    setInterval(draw, RENDER_TARGET);
});