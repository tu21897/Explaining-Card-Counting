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

        const xScale = d3.scaleBand()
                            .domain(data.map(dataPoint => dataPoint['Session ID']))
                            .rangeRound([margin.left, width])
                            .padding(0.1);

        const yScale = d3.scaleLinear()
                            .domain([40, 60])
                            .range([height, margin.bottom]);

        const vizarea = d3.select('svg')
                            .classed('vizarea', true)
                            .attr('width', width)
                            .attr('height', height);
        
        let color = d3.scaleOrdinal(d3.schemeTableau10).domain(data.map(d => d.key)); 

        let xMargin = xScale.copy().range([margin.left, width - margin.right]);
        let yMargin = yScale.copy().range([height - margin.bottom, margin.top]);

        const g = vizarea.selectAll('g')
        .data(data)
        .enter() 
          .append('g')
            .attr('transform', d => `translate(${margin.left}, ${yMargin(d['Session ID'])})`);
    
        g.append('rect')
            .attr('width', xMargin.bandwidth())
            .attr('height', d => yMargin(d.value) - yMargin(0))
            .style('fill', d => color(d.key))
            .style('stroke', 'white');
        
        g.append('text')
            .attr('x', xMargin.bandwidth())
            .attr('dx', -20)
            .attr('dy', '1em')
            .attr('fill', 'black')
            .style('font-size', 'small')
            .text(d => d['Session ID']);
    
        vizarea.append('g')
        .attr('transform', `translate(0, ${height - margin.bottom})`)
        .call(d3.axisBottom(xMargin));
    
        vizarea.append('g')
        .attr('transform', `translate(${margin.left}, 0)`)
        .call(d3.axisLeft(yMargin));

        vizarea.selectAll('.bar')
            .data(data)
            .enter()
            .append('rect')
            .classed('bar', true)
            .attr('width', xScale.bandwidth())
            .attr('height', data => height - margin.bottom - yScale(data['Lifetime winrate (W/L x(Base))']))
            .attr('x', data => xScale(data['Session ID']))
            .attr('y', data => yScale(data['Lifetime winrate (W/L x(Base))']))
            .style('fill', d => color(d.key));

        return vizarea.node()
    }
})();
