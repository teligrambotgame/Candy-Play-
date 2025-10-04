const canvas = document.getElementById('ludoBoard');
const ctx = canvas.getContext('2d');
const tileSize = 40;

// Define grid path (simplified 52-tile path)
const path = [
  { x: 6, y: 0 }, { x: 6, y: 1 }, { x: 6, y: 2 }, { x: 6, y: 3 }, { x: 6, y: 4 },
  { x: 5, y: 5 }, { x: 4, y: 5 }, { x: 3, y: 5 }, { x: 2, y: 5 }, { x: 1, y: 5 },
  { x: 0, y: 6 }, { x: 1, y: 6 }, { x: 2, y: 6 }, { x: 3, y: 6 }, { x: 4, y: 6 },
  { x: 5, y: 7 }, { x: 6, y: 7 }, { x: 6, y: 8 }, { x: 6, y: 9 }, { x: 6, y: 10 },
  { x: 7, y: 10 }, { x: 8, y: 10 }, { x: 9, y: 10 }, { x: 10, y: 10 }, { x: 10, y: 9 },
  { x: 10, y: 8 }, { x: 10, y: 7 }, { x: 9, y: 6 }, { x: 8, y: 6 }, { x: 7, y: 6 },
  { x: 10, y: 6 }, { x: 9, y: 5 }, { x: 8, y: 5 }, { x: 7, y: 5 }, { x: 6, y: 4 },
  // Continue till 52 tiles...
];

const safeTiles = [0, 8, 13, 21, 26, 34, 39, 47];

function drawBoard() {
  ctx.clearRect(0, 0, 600, 600);

  // Draw grid
  for (let i = 0; i < 15; i++) {
    for (let j = 0; j < 15; j++) {
      ctx.strokeRect(i * tileSize, j * tileSize, tileSize, tileSize);
    }
  }

  // Draw path
  path.forEach(tile => {
    ctx.fillStyle = '#ccc';
    ctx.fillRect(tile.x * tileSize, tile.y * tileSize, tileSize, tileSize);
  });

  // Draw tokens
  players.forEach(p => {
    p.tokens.forEach(pos => {
      if (pos > 0) {
        const tile = path[pos];
        ctx.beginPath();
        ctx.arc(tile.x * tileSize + 20, tile.y * tileSize + 20, 15, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.fill();
        ctx.stroke();
      }
    });
  });
    }
