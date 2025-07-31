const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score');
const livesElement = document.getElementById('lives');

const PADDLE_WIDTH = 100;
const PADDLE_HEIGHT = 10;
const BALL_RADIUS = 8;
const BRICK_ROWS = 5;
const BRICK_COLS = 10;
const BRICK_WIDTH = 75;
const BRICK_HEIGHT = 20;
const BRICK_PADDING = 5;
const BRICK_OFFSET_TOP = 60;
const POWERUP_WIDTH = 20;
const POWERUP_HEIGHT = 20;
const POWERUP_SPEED = 3;
const POWERUP_SPAWN_CHANCE = 0.3;

let gameState = 'ready'; // 'ready', 'playing', 'gameOver', 'won'
let score = 0;
let lives = 3;
let rightPressed = false;
let leftPressed = false;
let mouseX = canvas.width / 2;
let controlMode = 'keyboard'; // 'keyboard' or 'mouse'
let autoPlay = true; // Auto-play mode enabled by default
let powerUps = [];

const paddle = {
    x: (canvas.width - PADDLE_WIDTH) / 2,
    y: canvas.height - PADDLE_HEIGHT - 10,
    width: PADDLE_WIDTH,
    height: PADDLE_HEIGHT,
    speed: 7
};

const ball = {
    x: canvas.width / 2,
    y: canvas.height - 30,
    dx: 5,
    dy: -5,
    radius: BALL_RADIUS
};

const bricks = [];

function initBricks() {
    for (let c = 0; c < BRICK_COLS; c++) {
        bricks[c] = [];
        for (let r = 0; r < BRICK_ROWS; r++) {
            bricks[c][r] = { 
                x: 0, 
                y: 0, 
                status: 1,
                color: `hsl(${r * 60}, 70%, 50%)`
            };
        }
    }
}

function drawBricks() {
    for (let c = 0; c < BRICK_COLS; c++) {
        for (let r = 0; r < BRICK_ROWS; r++) {
            if (bricks[c][r].status === 1) {
                const brickX = (c * (BRICK_WIDTH + BRICK_PADDING)) + BRICK_PADDING;
                const brickY = (r * (BRICK_HEIGHT + BRICK_PADDING)) + BRICK_OFFSET_TOP;
                bricks[c][r].x = brickX;
                bricks[c][r].y = brickY;
                ctx.fillStyle = bricks[c][r].color;
                ctx.fillRect(brickX, brickY, BRICK_WIDTH, BRICK_HEIGHT);
                
                ctx.strokeStyle = '#fff';
                ctx.lineWidth = 1;
                ctx.strokeRect(brickX, brickY, BRICK_WIDTH, BRICK_HEIGHT);
            }
        }
    }
}

function drawBall() {
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = '#fff';
    ctx.fill();
    ctx.closePath();
}

function drawPaddle() {
    ctx.fillStyle = '#0095DD';
    ctx.fillRect(paddle.x, paddle.y, paddle.width, paddle.height);
}

function drawScore() {
    scoreElement.textContent = score;
    livesElement.textContent = lives;
}

function drawGameMessage(message) {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.font = '48px Arial';
    ctx.fillStyle = '#fff';
    ctx.textAlign = 'center';
    ctx.fillText(message, canvas.width / 2, canvas.height / 2);
    
    ctx.font = '24px Arial';
    ctx.fillText('Press SPACE to start', canvas.width / 2, canvas.height / 2 + 60);
}

function collisionDetection() {
    for (let c = 0; c < BRICK_COLS; c++) {
        for (let r = 0; r < BRICK_ROWS; r++) {
            const b = bricks[c][r];
            if (b.status === 1) {
                if (ball.x > b.x && ball.x < b.x + BRICK_WIDTH && 
                    ball.y > b.y && ball.y < b.y + BRICK_HEIGHT) {
                    ball.dy = -ball.dy;
                    b.status = 0;
                    score += 10;
                    
                    if (Math.random() < POWERUP_SPAWN_CHANCE) {
                        spawnPowerUp(b.x + BRICK_WIDTH / 2, b.y + BRICK_HEIGHT);
                    }
                    
                    if (score === BRICK_ROWS * BRICK_COLS * 10) {
                        gameState = 'won';
                    }
                }
            }
        }
    }
}

function movePaddle() {
    if (autoPlay) {
        const paddleCenter = paddle.x + paddle.width / 2;
        const ballCenter = ball.x;
        
        if (Math.abs(ballCenter - paddleCenter) > 5) {
            if (ballCenter > paddleCenter && paddle.x < canvas.width - paddle.width) {
                paddle.x += paddle.speed;
            } else if (ballCenter < paddleCenter && paddle.x > 0) {
                paddle.x -= paddle.speed;
            }
        }
        paddle.x = Math.max(0, Math.min(canvas.width - paddle.width, paddle.x));
    } else {
        if (rightPressed && paddle.x < canvas.width - paddle.width) {
            paddle.x += paddle.speed;
            controlMode = 'keyboard';
        } else if (leftPressed && paddle.x > 0) {
            paddle.x -= paddle.speed;
            controlMode = 'keyboard';
        } else if (controlMode === 'mouse') {
            paddle.x = Math.max(0, Math.min(canvas.width - paddle.width, mouseX - paddle.width / 2));
        }
    }
}

function moveBall() {
    ball.x += ball.dx;
    ball.y += ball.dy;
    
    if (ball.x + ball.dx > canvas.width - ball.radius || ball.x + ball.dx < ball.radius) {
        ball.dx = -ball.dx;
    }
    if (ball.y + ball.dy < ball.radius) {
        ball.dy = -ball.dy;
    } else if (ball.y + ball.dy > canvas.height - ball.radius) {
        if (ball.x > paddle.x && ball.x < paddle.x + paddle.width) {
            const hitPos = (ball.x - paddle.x) / paddle.width;
            const angle = (hitPos - 0.5) * Math.PI / 3;
            const speed = Math.sqrt(ball.dx * ball.dx + ball.dy * ball.dy);
            ball.dx = Math.sin(angle) * speed;
            ball.dy = -Math.cos(angle) * speed;
        } else {
            lives--;
            if (lives === 0) {
                gameState = 'gameOver';
            } else {
                resetBall();
            }
        }
    }
}

function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height - 30;
    ball.dx = 5 * (Math.random() > 0.5 ? 1 : -1);
    ball.dy = -5;
}

function spawnPowerUp(x, y) {
    powerUps.push({
        x: x - POWERUP_WIDTH / 2,
        y: y,
        width: POWERUP_WIDTH,
        height: POWERUP_HEIGHT,
        speed: POWERUP_SPEED,
        points: 20
    });
}

function drawPowerUps() {
    ctx.fillStyle = '#FFD700';
    for (let i = 0; i < powerUps.length; i++) {
        const powerUp = powerUps[i];
        ctx.fillRect(powerUp.x, powerUp.y, powerUp.width, powerUp.height);
        
        ctx.strokeStyle = '#FFA500';
        ctx.lineWidth = 2;
        ctx.strokeRect(powerUp.x, powerUp.y, powerUp.width, powerUp.height);
        
        ctx.fillStyle = '#000';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('+20', powerUp.x + powerUp.width / 2, powerUp.y + powerUp.height / 2 + 4);
        ctx.fillStyle = '#FFD700';
    }
}

function movePowerUps() {
    for (let i = powerUps.length - 1; i >= 0; i--) {
        powerUps[i].y += powerUps[i].speed;
        
        if (powerUps[i].y > canvas.height) {
            lives--;
            powerUps.splice(i, 1);
            if (lives === 0) {
                gameState = 'gameOver';
            }
        }
    }
}

function powerUpCollision() {
    for (let i = powerUps.length - 1; i >= 0; i--) {
        const powerUp = powerUps[i];
        if (powerUp.x < paddle.x + paddle.width &&
            powerUp.x + powerUp.width > paddle.x &&
            powerUp.y < paddle.y + paddle.height &&
            powerUp.y + powerUp.height > paddle.y) {
            
            score += powerUp.points;
            powerUps.splice(i, 1);
        }
    }
}

function resetGame() {
    score = 0;
    lives = 3;
    gameState = 'playing';
    paddle.x = (canvas.width - PADDLE_WIDTH) / 2;
    resetBall();
    initBricks();
    powerUps = [];
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    drawBricks();
    drawBall();
    drawPaddle();
    drawPowerUps();
    drawScore();
    
    ctx.fillStyle = autoPlay ? '#00FF00' : '#FF0000';
    ctx.font = '14px Arial';
    ctx.textAlign = 'left';
    ctx.fillText(`Auto-play: ${autoPlay ? 'ON' : 'OFF'} (Press 'A' to toggle)`, 10, 25);
    
    if (gameState === 'playing') {
        collisionDetection();
        moveBall();
        movePaddle();
        movePowerUps();
        powerUpCollision();
    } else if (gameState === 'ready') {
        drawGameMessage('BRICK BREAKER');
    } else if (gameState === 'gameOver') {
        drawGameMessage('GAME OVER');
    } else if (gameState === 'won') {
        drawGameMessage('YOU WIN!');
    }
    
    requestAnimationFrame(draw);
}

document.addEventListener('keydown', keyDownHandler);
document.addEventListener('keyup', keyUpHandler);
document.addEventListener('mousemove', mouseMoveHandler);

function keyDownHandler(e) {
    if (e.key === 'Right' || e.key === 'ArrowRight') {
        rightPressed = true;
        autoPlay = false;
    } else if (e.key === 'Left' || e.key === 'ArrowLeft') {
        leftPressed = true;
        autoPlay = false;
    } else if (e.key === ' ' || e.key === 'Spacebar') {
        e.preventDefault();
        if (gameState !== 'playing') {
            resetGame();
        }
    } else if (e.key === 'a' || e.key === 'A') {
        autoPlay = !autoPlay;
        controlMode = autoPlay ? 'auto' : 'keyboard';
    }
}

function keyUpHandler(e) {
    if (e.key === 'Right' || e.key === 'ArrowRight') {
        rightPressed = false;
    } else if (e.key === 'Left' || e.key === 'ArrowLeft') {
        leftPressed = false;
    }
}

function mouseMoveHandler(e) {
    const relativeX = e.clientX - canvas.offsetLeft;
    if (relativeX > 0 && relativeX < canvas.width) {
        mouseX = relativeX;
        controlMode = 'mouse';
    }
}

initBricks();
draw();