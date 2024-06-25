const imgBattleship = new Image();

class Ship {
    constructor(X, Y, Length) {
        this.Position = new Vector2(X, Y);
        this.Length = Length;
        this.GridPosition = new Vector2(0, 0);
        this.ImageType = "";
    }

    draw(ctx) {
        ctx.save();

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

    ball = {
        X: 0,
        Y: 0,
        velX: Math.random(),
        velY: Math.random()
    }

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

        ball.X += ball.velX * delta;
        ball.Y += ball.velY * delta;

        if (ball.X < 0 || ball.X > canvas.width)  { ball.velX *= -1 }
        if (ball.Y < 0 || ball.Y > canvas.height) { ball.velY *= -1; }
    }

    setInterval(update, 1/60);
    setInterval(draw, 1/60);
});