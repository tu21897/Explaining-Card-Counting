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
        d3.csv('data/test.csv').then(function(data) {
                                    vizgen(data);
                                });
    }

    function stdev(start, end, dataCol) {
        let mean = 0;
        let variance = 0;
        let datsum = 0;
        for (let i = start; i < end; i++) {
            datsum += dataCol[i];
        }
        mean = datsum/(end-1);
        for (let i = start; i < end; i++) {
            variance += (dataCol[i] - mean) ^ 2;
        }
        return (sqrt(variance), mean);
    }

    function generateCI(confidence, start, end, dataCol) {
        let CI;
        let rCI = [];
        let std;
        if (start != 0) {
            for (let i = 0; i < end - start; i++) {
                std = stdev(0, start + i, dataCol);
                CI = std[1] + confidence * (std[0]/sqrt(end - 1))
                rCI.push((-CI, CI))
            }
        } else {
            rCI.push((0,0))
            for (let i = start + 1; i < end; i++) {
                std = stdev(start, end, dataCol);
                CI = std[1] + confidence * (std[0]/sqrt(end - 1))
                rCI.push((-CI, CI))
            }
        }
        return rCI
    }

    function vizgen(data) {
        const margin = ({top:10, right:10, bottom:20, left:20});
        const width = 280;
        const height = 700;
        console.log(data);
        const xScale = d3.scaleLinear()
                            .domain([44, 56])
                            .range([margin.left, width - margin.right]);

        const yScale = d3.scaleBand()
                            .domain(data.map(dataPoint => dataPoint['Session ID']))
                            .range([height - margin.bottom, margin.top]);

        // yScale.range([height - margin.bottom, yScale.bandwidth()])
        const vizarea = d3.select('svg')
                            .classed('vizarea', true)
                            .attr('width', width)
                            .attr('height', height);

        let xMargin = xScale.copy().range([margin.left, width - margin.right]);
        let yMargin = yScale.copy().range([height - margin.top, margin.bottom]);

        vizarea.append('g')
                .attr('transform', `translate(0, ${height - margin.bottom})`)
                .call(d3.axisBottom(xMargin).ticks(6));
        
        vizarea.append('g')
                .attr('transform', `translate(0, ${height - margin.bottom})`)
                .call(d3.axisBottom(xMargin).tickSize(-(height-margin.top)).tickFormat('').ticks(1))
                .style("stroke-dasharray", "10 10");
    
        vizarea.append('g')
                .attr('transform', `translate(${margin.left}, 0)`)
                .call(d3.axisLeft(yScale));

        vizarea.selectAll('.pointSW')
                .data(data)
                .enter()
                .append('circle')
                .classed('point', true)
                .attr('r', 3)
                .attr('cx', data => xScale(data['Session winrate (W/L x(Base))']))
                .attr('cy', (data, i) => (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top))
                .style('fill', 'steelblue');

        // vizarea.selectAll('.pointLW')
        //         .data(data)
        //         .enter()
        //         .append('circle')
        //         .classed('point', true)
        //         .attr('r', 4)
        //         .attr('cx', data => xScale(data['Lifetime winrate (W/L x(Base))']))
        //         .attr('cy', (data, i) => (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top))
        //         .style('fill', 'steelblue');
        
        // let arr = [];
        // for (let row = 1; row <= data.length; row++) {
        //     arr.push(data[row]['Session ID'])
        // }

        // console.log(arr);
        // let confItvl = generateCI(.95, 0, 21, arr);
        // console.log(confItvl);

        vizarea.append('path')
                .datum(data)
                .classed('line', true)
                .attr('fill', 'none')
                .attr('stroke', 'tomato')
                .attr('stroke-width', 2.5)
                .attr('d', d3.line()
                                .x(data => {return xScale(data['Lifetime winrate (W/L x(Base))'])})
                                .y((data, i) => {return (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top)})
                                .curve(d3.curveMonotoneY)
                    );

        return vizarea.node()
    }
})();
