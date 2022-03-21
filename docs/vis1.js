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
    }

    /**
     * Delay sec seconds
     * @param {number} sec number of seconds to delay
     * @returns a promise that resolved after sec seconds
     */
    function delay(sec) {
        return new Promise((res) => {
        setTimeout(res, sec * 1000);
        });
    }

    async function vizgen(frame, text, button) {
        const margin = ({top:5, right:10, bottom:20, left:35, graph:5.8});
        const width = 300;
        const height = 450;
        const INF = new Intl.NumberFormat('en-US');

        const vizarea = d3.select('#vizarea1')
                            .attr('width', width)
                            .attr('height', height);
        
        const simname = d3.select('#simname')
                            .style('width', width)
                            .style('height', 40);
        
        const simcount = d3.select('#simcount')
                            .style('width', width)
                            .style('height', 10);

        const xScale = d3.scaleLinear()
                            .domain([47,53])
                            .range([0, width]);

        const xMargin = xScale.copy().range([margin.left, width - margin.right]);
        return vizarea.node();
    }
})();
