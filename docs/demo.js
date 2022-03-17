window.demo = {};
window.demo.deck = [];
window.demo.shuffleArray = function(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
}
window.demo.spawnCard = function() {
    window.demo.shuffleIfLow();
    let card = document.getElementById('demo-card');
    let cardCode = window.demo.deck.pop();
    let values = window.demo.decodeCard(cardCode);
    window.demo.resetCard();
    card.innerHTML = values.r;
    card.classList.toggle(values.s);
    if (values.s === 'diamonds' || values.s === 'hearts') {
        card.classList.add('red');
    }

    // Show arrow
    let id = ['arrow-minus1', 'arrow-zero', 'arrow-plus1'][window.strat.count(cardCode) + 1] // TODO: support other strats lol as if
    document.getElementById(id).classList.remove('hidden');

    // Update counts
    window.demo.recalculateStats();
}
window.demo.shuffleIfLow = function() {
    let numDecks = Number(document.getElementById("decks-input").value);
    let numBeforeShuffle = Number(document.getElementById("shuffle-input").value);
    let cut = (numDecks - numBeforeShuffle) * 52;
    if (window.demo.deck.length  <= cut) {
        window.demo.resetDeck();
    }
}
// also clears the arrow
window.demo.resetCard = function() {
    let card = document.getElementById('demo-card');
    let suits = ['diamonds', 'hearts', 'spades', 'clubs'];
    suits.forEach(s => card.classList.remove(s));
    card.innerHTML = '';
    card.classList.remove('black');
    card.classList.remove('red');

    let arrows = document.getElementsByClassName("count-arrow");
    for (let a of arrows) {
        a.classList.add('hidden');
    }
}

window.demo.recalculateStats = function() {
    let numDecks = Number(document.getElementById("decks-input").value);
    let count = 0 - window.demo.deck.map(c => window.strat.count(c)).reduce((a, b) => a + b);
    let remainingDecks = window.demo.deck.length / 52.0;
    let trueCount = count / remainingDecks;
    let betUnit = Number(document.getElementById("bet-input").value);
    let bet = (trueCount >= 1) ? Math.max(1, (trueCount-1)*betUnit).toFixed(2) : 0;

    document.getElementById('demo-rc').innerHTML = count;
    document.getElementById('demo-dr').innerHTML = remainingDecks.toFixed(1);
    document.getElementById('demo-tc').innerHTML = trueCount.toFixed(2);
    document.getElementById('demo-cr').innerHTML = window.demo.deck.length;
    document.getElementById('demo-bet-unit').innerHTML = betUnit;
    document.getElementById('demo-bet').innerHTML = bet;
}

window.demo.decodeCard = function(cardCode) {
    let suits = ['diamonds', 'hearts', 'spades', 'clubs'];
    let ranks = ['A', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K'];
    let s = suits[cardCode % 4];
    let r = ranks[cardCode % 13];
    return { 'r': r, 's': s };
}

window.demo.resetDeck = function() {
    window.demo.deck = [];
    for (let x = 0; x < 52 * Number(document.getElementById("decks-input").value); x++) {
        window.demo.deck.push(x % 52);
    }
    window.demo.shuffleArray(window.demo.deck);
    window.demo.recalculateStats();
    window.demo.resetCard();
}

//window.addEventListener('load', window.demo.resetDeck);
window.demo.resetDeck();