const imgBattleship = new Image();
const RENDER_TARGET = 1000/60;
const UPDATE_TARGET = 1000/60;

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
        this.ImageType = "";
    }

    update(ctx, delta) {
        
    }

    draw(ctx) {
        ctx.save();

        ctx.translate(this.Position.x, this.Position.y);
        ctx.drawImage(imgBattleship, 0, 0);

        ctx.restore();
    }
}

$(document).ready(function() {
    var canvas = document.getElementById("canvas-battleship");
    var ctx = canvas.getContext("2d");
    var delta = 0;
    var lastTime = new Date();

    imgBattleship.src = "img/Battleship/ShipBattleshipHull.png"
    //window.requestAnimationFrame(draw);

    let ships = [new Ship(5, 5, 5)];
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