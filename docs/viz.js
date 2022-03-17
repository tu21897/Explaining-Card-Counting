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
        const strategies = { 'Basic Strategy': 'basic_strategy',
                             'Hi-Lo Counting Strategy': 'counting_hi_lo',
                             'Hi-Opt 1 Counting Strategy':'counting_hi_opt1',
                             'Hi-Opt 2 Counting Strategy':'counting_hi_opt2' ,
                             'Omega 2 Counting Strategy':'counting_omega2' ,
                             'Zen Count Counting Strategy': 'counting_zen_count' ,
                             'Halves Counting Strategy': 'counting_halves',
                             'Wong Halves Counting Strategy': 'counting_wong_halves',
                             'Silver Fox Counting Strategy':'counting_silver_fox',
                             'Revere Point Count Counting Strategy':'counting_revere_point_count',
                             'Canfield Expert Counting Strategy': 'counting_canfield_expert'}

        let button = document.getElementById('button');
        button.addEventListener('click', animation, false);
        let text = 'Basic Strategy';
        function animation() {
            let mylist = document.getElementById("dropdown");
            text = mylist.options[mylist.selectedIndex].text;
            d3.csv('data/' + strategies[text] + '_data.csv').then(function(data) {vizgen(data, text, button)});
            button.style.display = 'none';
        }
        d3.csv('data/' + strategies[text] + '_data.csv').then(function(data) {vizgen(data.slice(1, 31), text)});
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
        const height = 520;
        const INF = new Intl.NumberFormat('en-US');

        const vizarea = d3.select('#vizarea')
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
        
        // Strategy name
        simname.style('text-align', 'center')
                .text(text)
                .style('justify-content', 'center')
                .style('font-weight', 'bold');
        
        let start = 0;
        let speed = 1;
        let dataSize = 30;
        let data = frame.slice(start, start + dataSize);

        while (start + dataSize < frame.length) {
            render(data, start+dataSize);
            await delay(0.005);
            d3.selectAll(".rerender").remove();
            simcount.selectAll("*").remove();
            if (start % 50 == 0) {
                speed++;
            }
            start+=speed;
            data = frame.slice(start, start + dataSize);
        }

        render(frame.slice(frame.length-dataSize, frame.length), frame.length);

        button.style.display = 'block';

        function render(data, end) {

            const yScale = d3.scaleBand()
                    .domain(data.map((dataPoint) => dataPoint['Session ID']))
                    .range([height, 0]);

            const yMargin = yScale.copy().range([height - margin.bottom + margin.graph, margin.top]);
        
            // Make the confidence interval

            let area = d3.area()
                        .x0(data => {return xMargin(data['Session CI Left'])})
                        .x1(data => { return xMargin(data['Session CI Right'])})
                        .y((data, i) => {return (height - margin.bottom - margin.top + margin.graph) - i * yMargin.bandwidth()})
                        .curve(d3.curveMonotoneY)

            vizarea.append('g').datum(data).append('path')
                        .classed('rerender', true)
                        .attr('stroke', 'none')
                        .attr('d', data => area(data))
                        .attr('fill', '#ADD8E6')
            
            // Center guidline
            vizarea.append('line')
                .classed('rerender', true)
                .attr('transform', `translate(${(width+margin.left-margin.right)/2}, ${margin.top})`)
                .attr('fill', 'none')
                .attr('stroke', 'black')
                .attr('stroke-width', 1)
                .attr("x1", 0)
                .attr("y1", -margin.bottom)
                .attr("x2", 0)
                .attr("y2", height - margin.top - margin.bottom + margin.graph)
                .style("stroke-dasharray", "10 10"); 

            // Plot session winrate points
            // const g = vizarea.selectAll('g')
            //                     .classed('rerender', true)
            //                     .data(data)
            //                     .enter()
            //                     .append('g');

            // g.data(data).append('circle')
            //                 .attr('r', 2)
            //                 .attr('cx', data => {return xMargin(data['Session winrate (W/L x(Base))'])})
            //                 .attr('cy', (data, i) => {return i * yMargin.bandwidth()})
            //                 .style('fill', 'steelblue')

            // Make the mean line
            let line = d3.line()
                        .x(data => {return xMargin(data['Lifetime winrate (W/L x(Base))'])})
                        .y((data,i) => {return (height - margin.bottom - margin.top + margin.graph) - i * yMargin.bandwidth()})
                        .curve(d3.curveMonotoneY)

            vizarea.append('g').append('path')
                        .datum(data)
                        .classed('rerender', true)
                        .attr('fill', 'none')
                        .attr('stroke', 'steelblue')
                        .attr('stroke-width', 0.3)
                        .attr('d', line(data));

            // Make the x-axis
            vizarea.append('g')
                    .classed('rerender', true)
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
                        .classed('rerender', true)
                        .attr('transform', `translate(${margin.left}, 0)`)
                        .call(d3.axisLeft(yMargin))
                        .append('text')
                            .attr('transform', `translate(20, ${margin.top}) rotate(-90)`)
                            .attr('text-anchor', 'end')
                            .attr('fill', 'black')
                            .attr('font-size', '12px')
                            .attr('font-weight', 'bold')
                            .text('Number of Sessions');

            // Number of games simulated
            simcount.style('text-align', 'center')
                        .text(INF.format(1000 * (end)) + ' Games Simulated')
                        .style('justify-content', 'center')
                        .style('font-weight', 'bold');
            
            let colors = d3.scaleLinear()
                            .domain([49.5, 50.2])
                            .range(["red", "green"]);

            // Winrate
            vizarea.append('text')
                .classed('rerender', true)
                .data(data)
                .attr('x', (width - margin.left) * 3 / 4 + 2)
                .attr('y', margin.top + 40)
                .attr('fill', function(d){ return colors(d['Lifetime winrate (W/L x(Base))'])})
                .attr('font-family', 'helvetica, arial')
                .attr('font-weight', 'bold')
                .attr('font-size', 40)
                .text(data => data['Lifetime winrate (W/L x(Base))']);
        }

        return vizarea.node();
    }
})();
