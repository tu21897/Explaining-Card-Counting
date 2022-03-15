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
        d3.csv('data/basic_strategy_data.csv').then(function(data) {
                                    vizgen(data);
                                });
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
        const margin = ({top:20, right:5, bottom:46, left:35});
        const width = 280;
        const height = 700;

        const vizarea = d3.select('svg')
                            .classed('vizarea', true)
                            .attr('width', width)
                            .attr('height', height);

        const xScale = d3.scaleLinear()
                            .domain([48, 52])
                            .range([margin.left, width - margin.right]);

        let start = 9800;
        let frameSize = 50;
        while (start + frameSize < data.length + 1){
            await delay(0.002);
            vizarea.selectAll("*").remove();
            
            let frame = data.filter(function(d,i){ return i >= start && i < start+frameSize});

            start += 1;
            const yScale = d3.scaleBand()
                                .domain(frame.map(framePoint => framePoint['Session ID']))
                                .range([height - margin.bottom, margin.top]);

            let xMargin = xScale.copy().range([margin.left, width - margin.right]);
            let yMargin = yScale.copy().range([height - margin.top, margin.bottom]);

            vizarea.append('path')
                    .datum(frame)
                    .attr('fill', '#ADD8E6')
                    .attr('stroke', 'none')
                    .attr('d', d3.area()
                        .y((frame, i) => {return (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top)})
                        .x0((frame) => { return xScale(frame['Session CI Left'])})
                        .x1((frame) => { return xScale(frame['Session CI Right'])})
                        .curve(d3.curveMonotoneY)
                        )

            vizarea.append('path')
                    .datum(frame)
                    .attr('fill', '#ffcccb')
                    .attr('stroke', 'none')
                    .attr('d', d3.area()
                        .y((frame, i) => {return (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top)})
                        .x0((frame) => { return xScale(frame['Lifetime CI Left'])})
                        .x1((frame) => { return xScale(frame['Lifetime CI Right'])})
                        .curve(d3.curveMonotoneY)
                        )

            // Make the axes
            vizarea.append('g')
                    .attr('transform', `translate(0, ${height - margin.bottom})`)
                    .call(d3.axisBottom(xMargin).ticks(4));

            vizarea.append('g')
                    .attr('transform', `translate(0, ${height - margin.bottom})`)
                    .call(d3.axisBottom(xMargin).tickSize(-(height-margin.top-margin.bottom)).tickFormat('').ticks(1))
                    .style('stroke-dasharray', '10 10');

            vizarea.append('g')
                    .attr('transform', `translate(${margin.left}, 0)`)
                    .call(d3.axisLeft(yScale));

            // Make the mean lines
            vizarea.append('path')
                    .datum(frame)
                    .classed('line', true)
                    .attr('fill', 'none')
                    .attr('stroke', 'tomato')
                    .attr('stroke-width', 0.3)
                    .attr('d', d3.line()
                                    .x((frame) => {return xScale(frame['Lifetime Mean'])})
                                    .y((frame, i) => {return (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top)})
                                    .curve(d3.curveMonotoneY)
                        );

            vizarea.append('path')
                        .datum(frame)
                        .classed('line', true)
                        .attr('fill', 'none')
                        .attr('stroke', 'steelblue')
                        .attr('stroke-width', 0.3)
                        .attr('d', d3.line()
                                        .x((frame, i) => {return xScale(frame['Lifetime winrate (W/L x(Base))'])})
                                        .y((frame, i) => {return (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top)})
                                        .curve(d3.curveMonotoneY)
                            );

            // Plot session winrates
            vizarea.selectAll('.pointSW')
                        .data(frame)
                        .enter()
                        .append('circle')
                        .classed('point', true)
                        .attr('r', 1.3)
                        .attr('cx', frame => xScale(frame['Session winrate (W/L x(Base))']))
                        .attr('cy', (frame, i) => (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top))
                        .style('fill', 'steelblue');
        }
    }
})();
