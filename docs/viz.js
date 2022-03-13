/**
* This is the js file that specifies the interaction in index.html.
*/

"use strict";

(function() {
  window.addEventListener("load", init);

  /**
  * Initialize the interative elements once the window is loaded.
  */
    function init() {
        d3.csv("data/test.csv").then(function(data) {
                                    vizgen(data);
                                });
    }

    function vizgen(data) {
        const margin = ({top:10, right:10, bottom:20, left:20});
        const width = 280;
        const height = 700;
        console.log(data);
        const xScale = d3.scaleLinear()
                            .domain([46, 52])
                            .range([margin.left, width - margin.right]);

        const yScale = d3.scaleBand()
                            .domain(data.map(dataPoint => dataPoint['Session ID']))
                            .range([height - margin.bottom, margin.top]);

        // yScale.range([height - margin.bottom, yScale.bandwidth()])
        const vizarea = d3.select('svg')
                            .classed('vizarea', true)
                            .attr('width', width)
                            .attr('height', height)
                            .style('border', '1px dotted black');

        let color = d3.scaleOrdinal(d3.schemeTableau10); 
        let xMargin = xScale.copy().range([margin.left, width - margin.right]);
        let yMargin = yScale.copy().range([height - margin.top, margin.bottom]);

        vizarea.append('g')
                .attr('transform', `translate(0, ${height - margin.bottom})`)
                .call(d3.axisBottom(xMargin));
    
        vizarea.append('g')
                .attr('transform', `translate(${margin.left}, 0)`)
                .call(d3.axisLeft(yScale));

        vizarea.selectAll('.bar')
                .data(data)
                .enter()
                .append('circle')
                .classed('bar', true)
                .attr('r', 3)
                .attr('cx', data => xScale(data['Session winrate (W/L x(Base))']))
                .attr('cy', (data, i) => (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top))
                .style('fill', d => color());

        vizarea.selectAll('.bar2')
                .data(data)
                .enter()
                .append('circle')
                .classed('bar2', true)
                .attr('r', 3)
                .attr('cx', data => xScale(data['Lifetime winrate (W/L x(Base))']))
                .attr('cy', (data, i) => (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top))
                .style('fill', red);

        return vizarea.node()
    }
})();
