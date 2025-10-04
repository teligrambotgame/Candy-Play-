function rollDice() {
  let rollCount = 0;
  const interval = setInterval(() => {
    const temp = Math.floor(Math.random() * 6) + 1;
    document.getElementById('diceResult').textContent = `Dice: ${temp}`;
    rollCount++;
    if (rollCount === 10) {
      clearInterval(interval);
      showTokenOptions(currentPlayer, temp);
    }
  }, 100);
}

function showTokenOptions(playerIndex, diceValue) {
  const container = document.getElementById('tokenOptions');
  container.innerHTML = '';
  players[playerIndex].tokens.forEach((pos, i) => {
    const btn = document.createElement('button');
    btn.textContent = `Token ${i + 1}`;
    btn.onclick = () => moveToken(playerIndex, i, diceValue);
    container.appendChild(btn);
  });
}
