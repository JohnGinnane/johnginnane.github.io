const imgBattleship = new Image();
const WIDTH = 500;
const HEIGHT = 500;

class Ship {
    constructor(X, Y, Length) {
        this.Position = new Vector2(X, Y);
        this.Length = Length;
        this.GridPosition = new Vector2(0, 0);
        this.ImageType = "";
        this.Velocity = new Vector2(Math.random(), Math.random());
    }

    update(delta) {
        this.Position.x += this.Velocity.x * delta;
        this.Position.y += this.Velocity.y * delta;

        if (this.Position.x < 0 || this.Position.x > WIDTH) {
            this.Velocity.x *= -1;
        }

        if (this.Position.y < 0 || this.Position.y > HEIGHT) {
            this.Velocity.y *= -1;
        }
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
    window.requestAnimationFrame(draw);

    let ships = [new Ship(5, 5, 5)];

    function draw() {
        // Clear the canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "rgb(50, 150, 255)"
        ctx.fillRect(0, 0, canvas.width, canvas.height)
        
        for (let i = 0; i < ships.length; i++) {
            let ship = ships[i];
            ship.draw(ctx);
        }
    }

    function update() {
        delta = new Date() - lastTime;
        lastTime = new Date();

        for (let i = 0; i < ships.length; i++) {
            let ship = ships[i];
            ship.update(delta);
        }
    }

    setInterval(update, 1/60);
    setInterval(draw, 1/60);
});