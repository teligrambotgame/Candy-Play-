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
  // Add token movement logic here
}

drawBoard();
let players = [
  { color: 'red', x: 50, y: 50, position: 0 },
  { color: 'green', x: 550, y: 50, position: 0 },
  { color: 'yellow', x: 50, y: 550, position: 0 },
  { color: 'blue', x: 550, y: 550, position: 0 }
];

let currentPlayer = 0;
