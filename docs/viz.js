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
        d3.csv('data/counting_wong_halves_data.csv').then(function(data) {vizgen(data)});
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

    function vizgen(data) {
        const margin = ({top:5, right:10, bottom:20, left:35, graph:5.8});
        const width = 280;
        const height = 600;
        const INF = new Intl.NumberFormat('en-US');

        const vizarea = d3.select('#vizarea')
                            .attr('width', width)
                            .attr('height', height);
        
        const simname = d3.select('#simname')
                            .style('width', width)
                            .style('height', 70);
        
        const simcount = d3.select('#simcount')
                            .style('width', width)
                            .style('height', 10);
        
        const interaction = d3.select('#interaction')
                            .attr('width', width)
                            .attr('height', 100);

        let start = 0;
        let frameSize = 50;
        // vizarea.selectAll("*").remove();
        // simname.selectAll("*").remove();
        // interaction.selectAll("*").remove();
        
        let frame = data.filter(function(d,i){ return i > start && i < start+frameSize});
        
        renderFrame(frame);

        function renderFrame(frame) {
            const xScale = d3.scaleLinear()
                    .domain([47,53])
                    .range([0, width]);

            const yScale = d3.scaleBand()
                    .domain(frame.map(framePoint => framePoint['Session ID']))
                    .range([height, 0]);

            const xMargin = xScale.copy().range([margin.left, width - margin.right]);
            const yMargin = yScale.copy().range([height - margin.bottom + margin.graph, margin.top]);

            // Make the confidence interval

            let area = d3.area()
                        .x0(frame => {return xMargin(frame['Session CI Left']) + margin.left})
                        .x1(frame => { return xMargin(frame['Session CI Right']) + margin.left})
                        .y((frame, i) => {return (height - margin.bottom - margin.top + margin.graph) - i * yMargin.bandwidth()})
                        .curve(d3.curveMonotoneY)

            vizarea.append('g').datum(frame).append('path')
                        .attr('stroke', 'none')
                        .attr('d', frame => area(frame))
                        .attr('fill', '#ADD8E6')

            // Plot session winrate points
            const g = vizarea.selectAll('g')
                                .data(frame)
                                .enter()
                                .append('g')
                                .attr('transform', `translate(${margin.left}, 0)`);

            g.data(frame).append('circle')
                            .attr('r', 2)
                            .attr('cx', frame => {return xMargin(frame['Session winrate (W/L x(Base))']) + margin.left})
                            .attr('cy', (frame, i) => {return i * yMargin.bandwidth()})
                            .style('fill', 'steelblue')

            // Center guidline
            vizarea.append('line')
                        .attr('transform', `translate(${(width+margin.left-margin.right)/2}, ${margin.top})`)
                        .attr('fill', 'none')
                        .attr('stroke', 'black')
                        .attr('stroke-width', 1)
                        .attr("x1", 0)
                        .attr("y1", -margin.bottom)
                        .attr("x2", 0)
                        .attr("y2", height - margin.top - margin.bottom + margin.graph)
                        .style("stroke-dasharray", "10 10"); 

            // Make the mean line
            let line = d3.line()
                        .x(frame => {return xMargin(frame['Lifetime winrate (W/L x(Base))']) + margin.left})
                        .y((frame,i) => {return (height - margin.bottom - margin.top + margin.graph) - i * yMargin.bandwidth()})
                        .curve(d3.curveMonotoneY)

            vizarea.append('g').append('path')
                        .datum(frame)
                        .classed('line', true)
                        .attr('fill', 'none')
                        .attr('stroke', 'steelblue')
                        .attr('stroke-width', 0.3)
                        .attr('d', line(frame));

            // Make the x-axis
            vizarea.append('g')
                            .attr('transform', `translate(0, ${height - margin.bottom})`)
                            .call(d3.axisBottom(xMargin).ticks(6))
                            .append('text')
                                .attr('text-anchor', 'end')
                                .attr('fill', 'black')
                                .attr('font-size', '12px')
                                .attr('font-weight', 'bold')
                                .attr('x', width - margin.right)
                                .attr('y', -margin.top)
                                .text('Winrate (%)');

            // Make the y-axis
            vizarea.append('g')
                        .attr('transform', `translate(${margin.left}, 0)`)
                        .call(d3.axisLeft(yMargin))
                        .append('text')
                            .attr('transform', `translate(20, ${margin.top}) rotate(-90)`)
                            .attr('text-anchor', 'end')
                            .attr('fill', 'black')
                            .attr('font-size', '12px')
                            .attr('font-weight', 'bold')
                            .text('Number of Sessions');
            
            // Title labels
            simname.style('text-align', 'center')
                        .text('Wong-Halves Counting Strategy')
                        .style('justify-content', 'center')
                        .style('font-weight', 'bold');

            simcount.style('text-align', 'center')
                        .text(INF.format(1000 * (start+frameSize)) + ' Games Simulated')
                        .style('justify-content', 'center')
                        .style('font-weight', 'bold');
        }

        return vizarea.node()
    }
})();
