let players = [
  { color: 'red', tokens: [0, 0, 0, 0] },
  { color: 'green', tokens: [0, 0, 0, 0] },
  { color: 'yellow', tokens: [0, 0, 0, 0] },
  { color: 'blue', tokens: [0, 0, 0, 0] }
];

let currentPlayer = 0;

function moveToken(playerIndex, tokenIndex, steps) {
  let player = players[playerIndex];
  let pos = player.tokens[tokenIndex];

  if (pos === 0 && steps !== 6) {
    nextTurn();
    return;
  }

  if (pos === 0 && steps === 6) {
    player.tokens[tokenIndex] = 1;
  } else {
    player.tokens[tokenIndex] += steps;
    if (player.tokens[tokenIndex] >= path.length) {
      player.tokens[tokenIndex] = path.length - 1;
    }
  }

  drawBoard();
  checkCapture(playerIndex, tokenIndex);
  checkWin(playerIndex);
  nextTurn();
}

function checkCapture(playerIndex, tokenIndex) {
  const pos = players[playerIndex].tokens[tokenIndex];
  players.forEach((p, i) => {
    if (i !== playerIndex) {
      p.tokens.forEach((otherPos, j) => {
        if (otherPos === pos && !safeTiles.includes(pos)) {
          p.tokens[j] = 0;
        }
      });
    }
  });
}

function checkWin(playerIndex) {
  const allHome = players[playerIndex].tokens.every(pos => pos === path.length - 1);
  if (allHome) {
    document.getElementById('winnerText').textContent = `${players[playerIndex].color.toUpperCase()} wins!`;
    document.getElementById('gameOver').style.display = 'block';
  }
}

function restartGame() {
  players.forEach(p => p.tokens = [0, 0, 0, 0]);
  currentPlayer = 0;
  document.getElementById('gameOver').style.display = 'none';
  drawBoard();
}

function nextTurn() {
  currentPlayer = (currentPlayer + 1) % players.length;
}
