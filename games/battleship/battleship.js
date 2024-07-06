const imgCarrier = new Image();
const imgBattleship = new Image();
const imgCruiser = new Image();
const imgSubmarine = new Image();
const imgDestroyer = new Image();

const RENDER_TARGET = 1000/60;
const UPDATE_TARGET = 1000/60;
const GAME_SCALE = 1;
const GRID_SIZE = 32;

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

function calcImageScale(ship) {
    try {
        let width = ship.Image.width;
        let height = ship.Image.height;
        
        let diffWidth = GRID_SIZE / width;
        let diffHeight = (GRID_SIZE * ship.Length) / height;

        if (Math.abs(diffWidth) < Math.abs(diffHeight)) {
            return diffWidth;
        } else {
            return diffHeight;
        }
    } catch (ex) {
        return 1;
    }
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
        let imageScale = calcImageScale(this);
        let scaleWidth = this.Image.width * imageScale * GAME_SCALE;
        let scaleHeight = this.Image.height * imageScale * GAME_SCALE;
        let yOffset = this.Length % 2 == 0 ? GRID_SIZE / 2 : 0;
        
        ctx.translate(this.Position.x, this.Position.y);
        ctx.drawImage(this.Image, -scaleWidth/2, -scaleHeight/2 + yOffset, scaleWidth, scaleHeight);
        
        // Draw hitbox
        ctx.beginPath();
        
        if (this.mouseOver()) {
            ctx.strokeStyle = "green"
        } else {
            ctx.strokeStyle = "red";
        }

        ctx.strokeRect(-scaleWidth/2, -scaleHeight/2 + yOffset, scaleWidth, scaleHeight);

        // Draw center of ship
        ctx.beginPath();
        ctx.fillStyle ="red";
        ctx.arc(0, 0, 2, 0, Math.PI*2);
        ctx.fill();

        // Draw grid tiles the ship occupies
        ctx.beginPath();
        ctx.strokeStyle = "purple";

        for (let i = 0; i < this.Length; i++) {
            let k = Math.ceil(i / 2) * (i % 2 == 0 ? -1 : 1);
            let y = GRID_SIZE/-2 + GRID_SIZE * k;
            ctx.strokeRect(-GRID_SIZE/2, y, GRID_SIZE, GRID_SIZE);
        }

        ctx.restore();
    }

    mouseOver() {
        let scaleWidth = this.Image.width * this.ImageScale * GAME_SCALE;
        let scaleHeight = this.Image.height * this.ImageScale * GAME_SCALE;
        let yOffset = this.Length % 2 == 0 ? GRID_SIZE / 2 : 0;

        let topLeftX = this.Position.x - (GRID_SIZE / 2);
        let topLeftY = this.Position.y - (GRID_SIZE / 2)  - (GRID_SIZE * Math.floor((this.Length - 1)/2));
        let bottomRightX = this.Position.x + (GRID_SIZE / 2);
        let bottomRightY = topLeftY + (GRID_SIZE * this.Length);

        if (MOUSE_POS.x >= topLeftX  && 
            MOUSE_POS.x <= bottomRightX  &&
            MOUSE_POS.y >= topLeftY && 
            MOUSE_POS.y <= bottomRightY) {
            return true;
        } else {
            return false;
        }        
    }
}

class AircraftCarrier extends Ship {
    constructor(X, Y) {
        super(X, Y, 5);

        if (imgCarrier.src == null || imgCarrier.src == "") {
            imgCarrier.src = "img/Carrier/ShipCarrierHull.png"
        }

        this.Image = imgCarrier;
    }
}

class Battleship extends Ship {
    constructor(X, Y) {
        super(X, Y, 4);

        if (imgBattleship.src == null || imgBattleship.src == "") {
            imgBattleship.src = "img/Battleship/ShipBattleshipHull.png"
        }

        this.Image = imgBattleship;
    }
}

class Cruiser extends Ship {
    constructor(X, Y) {
        super(X, Y, 3);

        if (imgCruiser.src == null || imgCruiser.src == "") {
            imgCruiser.src = "img/Cruiser/ShipCruiserHull.png";
        }

        this.Image = imgCruiser;
    }
}

class Submarine extends Ship {
    constructor(X, Y) {
        super(X, Y, 3);

        if (imgSubmarine.src == null || imgSubmarine.src == "") {
            imgSubmarine.src = "img/Submarine/ShipSubMarineHull.png";
        }

        this.Image = imgSubmarine;
    }
}

class Destroyer extends Ship {
    constructor(X, Y) {
        super(X, Y, 2);

        if (imgDestroyer.src == null || imgDestroyer.src == "") {
            imgDestroyer.src = "img/Destroyer/ShipDestroyerHull.png";
        }

        this.Image = imgDestroyer;
    }
}

// https://stackoverflow.com/a/18053642
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

        // https://www.w3schools.com/howto/howto_js_draggable.asp
        // Using the above to implement dragging ships
        if (SelectedShip) {
            ClickDetails.pos1 = ClickDetails.pos3 - e.clientX;
            ClickDetails.pos2 = ClickDetails.pos4 - e.clientY;
            ClickDetails.pos3 = e.clientX;
            ClickDetails.pos4 = e.clientY;
            
            SelectedShip.Position = SelectedShip.Position.add(new Vector2(-ClickDetails.pos1, -ClickDetails.pos2));
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