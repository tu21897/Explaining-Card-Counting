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

    async function vizgen(data) {
        const margin = ({top:10, right:5, bottom:20, left:35, graph: 6});
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

        const xScale = d3.scaleLinear()
                            .domain([46, 54])
                            .range([0, width]);
        let start = 0;
        let frameSize = 50;
        // while (start + frameSize < 50 + 1){
        //     await delay(0.001);
            vizarea.selectAll("*").remove();
            simname.selectAll("*").remove();
            interaction.selectAll("*").remove();
            
            let frame = data.filter(function(d,i){ return i >= start && i < start+frameSize});

            // start += 1;
            const yScale = d3.scaleBand()
                                .domain(frame.map(framePoint => framePoint['Session ID']))
                                .range([height, 0]);

            let xMargin = xScale.copy().range([margin.left, width - margin.right]);
            let yMargin = yScale.copy().range([height - margin.bottom + margin.graph, margin.top]);

            // var area = function(datum, boolean) {
            //     return d3.area()
            //         // .y0((frame, i) => {(height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top)})
            //         .y((frame) => {return boolean ? 0:(height-margin.top) - (frame['Session ID']*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top)})
            //         .x0((frame) => { return xScale(frame['Session CI Left'])})
            //         .x1((frame) => { return xScale(frame['Session CI Right'])})
            //         .curve(d3.curveMonotoneY)
            //     (datum);
            // }

            let g = vizarea.append('g').attr('transform', `translate(${margin.left}, ${-margin.bottom})`);

            let area = d3.area(frame)
                .x0((frame) => { return xScale(frame['Session CI Left'])})
                .x1((frame) => { return xScale(frame['Session CI Right'])})
                .y((frame, i) => {return (height) - i * yMargin.bandwidth()})
                .curve(d3.curveMonotoneY)

            let confitvl = g.append('path')
                    .datum(frame)
                    .attr('stroke', 'none')
                    .attr('d', frame => area(frame))
                    .attr('fill', '#ADD8E6');
                    // .transition()
                    // .duration(2000)
                    // .attr("d", d => area(d,true));;
            
            // Make the mean lines

            let mean = g.append('path')
                        .datum(frame)
                        .classed('line', true)
                        .attr('fill', 'none')
                        .attr('stroke', 'steelblue')
                        .attr('stroke-width', 0.3)
                        .attr('d', d3.line()
                                        .x((frame) => {return xScale(frame['Lifetime winrate (W/L x(Base))'])})
                                        .y((frame, i) => {return height - i * yMargin.bandwidth()})
                                        .curve(d3.curveMonotoneY)
                            );

            // mean.transition()
            //         .duration(2000)
            //         .ease(d3.easePolyIn).attrTween("stroke-dasharray", function() {
            //             const length = this.getTotalLength();
            //             return d3.interpolate(`0,${length}`, `${length},${length}`);
            //             })

            // Plot session winrates
            // let points = vizarea.selectAll('.pointSW')
            //             .data(frame)
            //             .enter()
            //             .append('circle')
            //             .classed('point', true)
            //             .attr('r', 1.3)
            //             .attr('cx', frame => xScale(frame['Session winrate (W/L x(Base))']))
            //             .attr('cy', (frame, i) => (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top))
            //             .style('fill', 'steelblue');
            // Make the axes
            vizarea.append('g')
                    .attr('transform', `translate(0, ${height - margin.bottom})`)
                    .call(d3.axisBottom(xMargin).ticks(4))
                    .append('text')
                        .attr('text-anchor', 'end')
                        .attr('fill', 'black')
                        .attr('font-size', '12px')
                        .attr('font-weight', 'bold')
                        .attr('x', width - margin.right)
                        .attr('y', -margin.top)
                        .text('Winrate (%)');


            g.append('line')
                        .attr('transform', `translate(${(width-margin.left-margin.right)/2}, ${margin.top})`)
                        .attr('fill', 'none')
                        .attr('stroke', 'black')
                        .attr('stroke-width', 1)
                        .attr("x1", 0)
                        .attr("y1", margin.top)
                        .attr("x2", 0)
                        .attr("y2", height - margin.bottom)
                        .style("stroke-dasharray", "10 10"); 

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

            simname.style('text-align', 'center')
                        .text('Wong-Halves Counting Strategy')
                        .style('justify-content', 'center')
                        .style('font-weight', 'bold');

            simcount.style('text-align', 'center')
                        .text(INF.format(1000 * (start+frameSize)) + ' Games Simulated')
                        .style('justify-content', 'center')
                        .style('font-weight', 'bold');
            // interaction.append('text')
            //             .attr('text-anchor', 'center')
            //             .attr('x', 2 * margin.left - 2 * margin.right)
            //             .attr('y', 25)
            //             .attr('font-weight', 'bold')
            //             .attr('font-size',15)
            //             .text('Interactions');
        // }
        update();
        
        function update() {
        }
        return vizarea.node()
    }
})();
