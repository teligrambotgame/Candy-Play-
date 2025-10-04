const canvas = document.getElementById('ludoBoard');
const ctx = canvas.getContext('2d');

function drawBoard() {
  ctx.fillStyle = '#fff';
  ctx.fillRect(0, 0, 600, 600);
  ctx.strokeStyle = '#000';
  ctx.strokeRect(0, 0, 600, 600);

  // Example: Draw a simple square for each player
  ctx.fillStyle = 'red';
  ctx.fillRect(0, 0, 200, 200);

  ctx.fillStyle = 'green';
  ctx.fillRect(400, 0, 200, 200);

  ctx.fillStyle = 'yellow';
  ctx.fillRect(0, 400, 200, 200);

  ctx.fillStyle = 'blue';
  ctx.fillRect(400, 400, 200, 200);
}

function rollDice() {
  const result = Math.floor(Math.random() * 6) + 1;
  document.getElementById('diceResult').textContent = `Dice: ${result}`;

  let player = players[currentPlayer];
  player.position += result;

  // Simple movement logic: move right by 30px per step
  player.x = 50 + player.position * 30;

  drawBoard();

  // Switch to next player
  currentPlayer = (currentPlayer + 1) % players.length;
}

function drawBoard() {
  ctx.clearRect(0, 0, 600, 600);
  // Draw base zones
  ctx.fillStyle = 'red';
  ctx.fillRect(0, 0, 200, 200);
  ctx.fillStyle = 'green';
  ctx.fillRect(400, 0, 200, 200);
  ctx.fillStyle = 'yellow';
  ctx.fillRect(0, 400, 200, 200);
  ctx.fillStyle = 'blue';
  ctx.fillRect(400, 400, 200, 200);

  // Draw tokens
  players.forEach(p => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, 15, 0, Math.PI * 2);
    ctx.fillStyle = p.color;
    ctx.fill();
    ctx.stroke();
  });
}
