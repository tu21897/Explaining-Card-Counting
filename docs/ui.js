/**
* This is the js file that specifies the interaction in index.html.
*/

'use strict';

(function() {
  window.addEventListener('load', init);

  /**
  * Initialize the interative elements once the window is loaded.
  */
    function init() {
        // updateCount();
        
        let button = document.getElementsByClassName('fp-controlArrow')[0];
        let button2 = document.getElementsByClassName('fp-controlArrow')[1];
        let fp = document.getElementById('fp-nav');
        let ttn = document.getElementById('tooltipnav');
        button.addEventListener('click', hideshow, false);
        button2.addEventListener('click', hideshow2, false);

        function hideshow() {
            button.style.display = 'none';
            button2.style.display = 'block';
            fp.className = 'fp-left';
            ttn.style.left = null;
            ttn.style.right = '32px';
            ttn.innerText = 'What is Blackjack?';
        };
        
        function hideshow2() {
            button.style.display = 'block';
            button2.style.display = 'none';
            fp.className = 'fp-right';
            ttn.style.right = null;
            ttn.style.left = '32px';
            ttn.innerText = 'Game Strategy';
        };
    }

    function updateCount() {
        let simnum = document.getElementById("simnum");
        let end = parseInt(simnum.getAttribute("end"));
        let incspeed = parseInt(simnum.getAttribute("incspeed"));
        let count = parseInt(simnum.innerText.replace(/,/g, ''));
        let INF = new Intl.NumberFormat('en-US');
        let delay = parseInt(simnum.getAttribute("delay"));
        if (incspeed <= 255) {
            simnum.setAttribute('incspeed', 255);
        } else {
            simnum.setAttribute('incspeed', incspeed*.975);
        }
        let inc = Math.trunc(end / incspeed)
        if (count <= end - inc) {
            simnum.innerText = INF.format(count + inc);
            setTimeout(updateCount, delay);
        } else if (count < end){
            if (count <= end - 1000) {
                count = end - 1000;
            }
            let buffer = end - count;
            if (buffer < 50) {
                simnum.setAttribute('delay', delay + Math.floor(100/buffer));
            }
            simnum.innerText = INF.format(count + Math.floor(buffer/50) + 1);
            setTimeout(updateCount, delay);
        } else {
            simnum.innerText = INF.format(end);
        } 
    };
})();
