window.strat = {};
window.strat.name = "high low";
// input: card (int) the card to count
// take values > 12 mod 13, 0 is Ace
// output: the value by which to adjust the count
window.strat.count = function(card) {
    card = card % 13;
    if (2 <= card && card <= 6) {
        return 1;
    } else if (7 <= card && card <= 9) {
        return 0;
    } else {
        return -1;
    }
}