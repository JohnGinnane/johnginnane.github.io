$(document).ready(function() {
    var canvas = document.getElementById("canvas-battleship");
    var ctx = canvas.getContext("2d");

    ball = {
        X: 0,
        Y: 0,
        velX: Math.random(),
        velY: Math.random()
    }

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "rgb(50, 150, 255)"
        ctx.fillRect(0, 0, canvas.width, canvas.height)
        ctx.beginPath();
        ctx.arc(ball.X, ball.Y, 30, 0, Math.PI * 2);
        ctx.fillStyle = "rgb(255, 0, 0)"
        ctx.fill();
    }

    function update(dt) {
        ball.X += ball.velX;
        ball.Y += ball.velY;

        if (ball.X < 0 || ball.X > canvas.width)  { ball.velX *= -1 }
        if (ball.Y < 0 || ball.Y > canvas.height) { ball.velY *= -1; }
    }

    setInterval(draw, 1/60);
    setInterval(update, 1/60);
});