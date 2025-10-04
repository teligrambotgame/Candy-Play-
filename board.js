const canvas = document.getElementById('ludoBoard');
const ctx = canvas.getContext('2d');
const tileSize = 40;

// Simplified path (you can expand to full 52-tile path)
const path = [
  { x: 6, y: 0 }, { x: 6, y: 1 }, { x: 6, y: 2 }, { x: 6, y: 3 }, { x: 6, y: 4 },
  { x: 5, y: 5 }, { x: 4, y: 5 }, { x: 3, y: 5 }, { x: 2, y: 5 }, { x: 1, y: 5 },
  { x: 0, y: 6 }, { x: 1, y: 6 }, { x: 2, y: 6 }, { x: 3, y: 6 }, { x: 4, y: 6 },
  { x: 5, y: 7 }, { x: 6, y: 7 }, { x: 6, y: 8 }, { x: 6, y: 9 }, { x: 6, y: 10 },
  { x: 7, y: 10 }, { x: 8, y: 10 }, { x: 9, y: 10 }, { x: 10, y: 10 }, { x: 10, y: 9 },
  { x: 10, y: 8 }, { x: 10, y: 7 }, { x: 9, y: 6 }, { x: 8, y: 6 }, { x: 7, y: 6 },
  { x: 10, y: 6 }, { x: 9, y: 5 }, { x: 8, y: 5 }, { x: 7, y: 5 }, { x: 6, y: 4 },
  // Add more tiles to complete full path if needed
];

const safeTiles = [0, 8, 13, 21, 26, 34]; // Indexes of safe tiles

const players = [
  { color: 'red', tokens: [0, 0, 0, 0] },
  { color: 'green', tokens: [0, 0, 0, 0] },
  { color: 'yellow', tokens: [0, 0, 0, 0] },
  { color: 'blue', tokens: [0, 0, 0, 0] }
];

// Draw avatars (top row)
function drawAvatars() {
  const avatar = new Image();
  avatar.src = 'assets/avatar.png';
  avatar.onload = () => {
    players.forEach((p, i) => {
      ctx.drawImage(avatar, 10 + i * 50, 10, 40, 40);
    });
  };
}

// Main board drawing function
function drawBoard() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw grid
  for (let i = 0; i < 15; i++) {
    for (let j = 0; j < 15; j++) {
      ctx.strokeStyle = '#999';
      ctx.strokeRect(i * tileSize, j * tileSize, tileSize, tileSize);
    }
  }

  // Draw path tiles
  path.forEach(tile => {
    ctx.fillStyle = '#ccc';
    ctx.fillRect(tile.x * tileSize, tile.y * tileSize, tileSize, tileSize);
  });

  // Draw safe tiles
  safeTiles.forEach(index => {
    const tile = path[index];
    ctx.fillStyle = '#aaffaa';
    ctx.fillRect(tile.x * tileSize, tile.y * tileSize, tileSize, tileSize);
  });

  // Draw tokens
  players.forEach(player => {
    player.tokens.forEach(pos => {
      if (pos > 0) {
        const tile = path[pos];
        ctx.beginPath();
        ctx.arc(tile.x * tileSize + tileSize / 2, tile.y * tileSize + tileSize / 2, 15, 0, Math.PI * 2);
        ctx.fillStyle = player.color;
        ctx.fill();
        ctx.strokeStyle = '#000';
        ctx.stroke();
      }
    });
  });

  // Draw avatars
  drawAvatars();
}
