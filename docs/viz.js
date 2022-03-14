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
        mean = datsum/end;
        for (let i = start; i < end; i++) {
            variance += (dataCol[i] - mean) * (dataCol[i] - mean);
        }
        return Math.sqrt(variance/end);
    }

    function generateCI(zVals, dataCol) {
        let rCI = [];
        rCI.push([0, dataCol[0]]);
        for (let i = 1; i < dataCol.length; i++) {
            let zVal;
            if (i >= 100) {
                zVal = zVals[zVals.length-1]
            } else if (i >= 90) {
                zVal = zVals[zVals.length-2]
            } else if (i >= 80) {
                zVal = zVals[zVals.length-3]
            } else if (i >= 70) {
                zVal = zVals[zVals.length-4]
            } else if (i >= 60) {
                zVal = zVals[zVals.length-5]
            } else if (i >= 50) {
                zVal = zVals[zVals.length-6]
            } else if (i >= 40) {
                zVal = zVals[zVals.length-7]
            } else if (i >= 30) {
                zVal = zVals[zVals.length-8]
            } else {
                zVal = zVals[i-1]
            }
            let std = stdev(0, i + 1, dataCol);
            let CI = zVal * (std/Math.sqrt(i + 1));
            rCI.push(CI);
        }
        return rCI;
    }

    function vizgen(data) {
        const margin = ({top:10, right:10, bottom:20, left:20});
        const width = 280;
        const height = 700;
        const twoTailZVal = [12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201,
            2.179, 2.160, 2.145, 2.131, 2.120, 2.110, 2.101, 2.093, 2.086, 2.080, 2.074,
            2.069, 2.064, 2.060, 2.056, 2.052, 2.048, 2.045, 2.042, 2.021, 2.009, 2.000,
            1.994, 1.990, 1.987, 1.984, 1.960];

        const xScale = d3.scaleLinear()
                            .domain([46, 54])
                            .range([margin.left, width - margin.right]);

        const yScale = d3.scaleBand()
                            .domain(data.map(dataPoint => dataPoint['Session ID']))
                            .range([height - margin.bottom, margin.top]);

        const vizarea = d3.select('svg')
                            .classed('vizarea', true)
                            .attr('width', width)
                            .attr('height', height);

        let xMargin = xScale.copy().range([margin.left, width - margin.right]);
        let yMargin = yScale.copy().range([height - margin.top, margin.bottom]);

        // Make confidence band
        let rows = [];
        for (let row = 0; row < data.length; row++) {
            rows.push({'Session ID': data[row]});
        }
        let sessWR = [];
        let lifeWR =[];
        for (let i = 0; i < rows.length; i++) {
            sessWR.push(parseFloat(rows[i]['Session ID']['Session winrate (W/L x(Base))']));
            lifeWR.push(parseFloat(rows[i]['Session ID']['Lifetime winrate (W/L x(Base))']));
        }

        let confItvl = generateCI(twoTailZVal, sessWR);
        let itvlBand = [];
        for (let i = 0; i < confItvl.length; i++) {
            itvlBand.push([parseFloat(lifeWR[i])- 2 * parseFloat(confItvl[i]), parseFloat(lifeWR[i])+ 2 * parseFloat(confItvl[i])]);
        }

        vizarea.append('path')
                .datum(data)
                .attr('fill', '#ADD8E6')
                .attr('stroke', 'none')
                .attr('d', d3.area()
                    .y((data, i) => {return (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top)})
                    .x0((data, i) => { return xScale(itvlBand[i][0])})
                    .x1((data, i) => { return xScale(itvlBand[i][1])})
                    .curve(d3.curveMonotoneY)
                    )

        sessWR = [];
        for (let i = 0; i < rows.length; i++) {
            sessWR.push(parseFloat(rows[i]['Session ID']['Lifetime winrate (W/L x(Base))']));
        }
        confItvl = generateCI(twoTailZVal, lifeWR);
        itvlBand = [];
        let mean = [sessWR[0]];
        for (let i = 1; i < sessWR.length; i++) {
            let datsum = 0;
            for (let j = 0; j <= i; j++) {
                datsum += sessWR[j];
            }
            mean.push(datsum/(i+1));
        }
        for (let i = 0; i < confItvl.length; i++) {
            itvlBand.push([parseFloat(mean[i])-parseFloat(confItvl[i]), parseFloat(mean[i])+parseFloat(confItvl[i])]);
        }

        vizarea.append('path')
                .datum(data)
                .attr('fill', '#ffcccb')
                .attr('stroke', 'none')
                .attr('d', d3.area()
                    .y((data, i) => {return (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top)})
                    .x0((data, i) => { return xScale(itvlBand[i][0])})
                    .x1((data, i) => { return xScale(itvlBand[i][1])})
                    .curve(d3.curveMonotoneY)
                    )
        
        vizarea.append('g')
                .attr('transform', `translate(0, ${height - margin.bottom})`)
                .call(d3.axisBottom(xMargin).ticks(6));
        
        vizarea.append('g')
                .attr('transform', `translate(0, ${height - margin.bottom})`)
                .call(d3.axisBottom(xMargin).tickSize(-(height-margin.top)).tickFormat('').ticks(1))
                .style('stroke-dasharray', '10 10');
    
        vizarea.append('g')
                .attr('transform', `translate(${margin.left}, 0)`)
                .call(d3.axisLeft(yScale));

        vizarea.append('path')
                .datum(data)
                .classed('line', true)
                .attr('fill', 'none')
                .attr('stroke', 'tomato')
                .attr('stroke-width', 1.25)
                .attr('d', d3.line()
                                .x((data, i) => {return xScale(mean[i])})
                                .y((data, i) => {return (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top)})
                                .curve(d3.curveMonotoneY)
                    );

        vizarea.append('path')
                    .datum(data)
                    .classed('line', true)
                    .attr('fill', 'none')
                    .attr('stroke', 'steelblue')
                    .attr('stroke-width', 1.25)
                    .attr('d', d3.line()
                                    .x((data, i) => {return xScale(data['Lifetime winrate (W/L x(Base))'])})
                                    .y((data, i) => {return (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top)})
                                    .curve(d3.curveMonotoneY)
                        );
        
        vizarea.selectAll('.pointSW')
                    .data(data)
                    .enter()
                    .append('circle')
                    .classed('point', true)
                    .attr('r', 1.3)
                    .attr('cx', data => xScale(data['Session winrate (W/L x(Base))']))
                    .attr('cy', (data, i) => (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top))
                    .style('fill', 'steelblue');

        return vizarea.node()
    }
})();
