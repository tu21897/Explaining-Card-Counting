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

    function stdev(start, end, frameCol) {
        let mean = 0;
        let variance = 0;
        let datsum = 0;
        for (let i = start; i < end; i++) {
            datsum += frameCol[i];
        }
        mean = datsum/end;
        for (let i = start; i < end; i++) {
            variance += (frameCol[i] - mean) * (frameCol[i] - mean);
        }
        return Math.sqrt(variance/end);
    }

    function generateCI(zVals, frameCol) {
        let rCI = [];
        rCI.push([0, frameCol[0]]);
        for (let i = 1; i < frameCol.length; i++) {
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
            let std = stdev(0, i + 1, frameCol);
            let CI = zVal * (std/Math.sqrt(i + 1));
            rCI.push(CI);
        }
        return rCI;
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
        const margin = ({top:10, right:10, bottom:20, left:20});
        const width = 280;
        const height = 700;

        const twoTailZVal = [12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201,
            2.179, 2.160, 2.145, 2.131, 2.120, 2.110, 2.101, 2.093, 2.086, 2.080, 2.074,
            2.069, 2.064, 2.060, 2.056, 2.052, 2.048, 2.045, 2.042, 2.021, 2.009, 2.000,
            1.994, 1.990, 1.987, 1.984, 1.960];

        const vizarea = d3.select('svg')
                            .classed('vizarea', true)
                            .attr('width', width)
                            .attr('height', height);

        const xScale = d3.scaleLinear()
                            .domain([46, 54])
                            .range([margin.left, width - margin.right]);

        let start = 0;
        let frameSize = 10;
        while (start + frameSize < data.length){
            await delay(0.04);
            vizarea.selectAll("*").remove();
            
            let frame = data.filter(function(d,i){ return i >= start && i < start+frameSize});

            start += 1;
            const yScale = d3.scaleBand()
                                .domain(frame.map(framePoint => framePoint['Session ID']))
                                .range([height - margin.bottom, margin.top]);

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
            for (let i = start; i < start + frameSize; i++) {
                itvlBand.push([parseFloat(lifeWR[i])- 2 * parseFloat(confItvl[i]), parseFloat(lifeWR[i])+ 2 * parseFloat(confItvl[i])]);
            }

            vizarea.append('path')
                    .datum(frame)
                    .attr('fill', '#ADD8E6')
                    .attr('stroke', 'none')
                    .attr('d', d3.area()
                        .y((frame, i) => {return (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top)})
                        .x0((frame, i) => { return xScale(itvlBand[i][0])})
                        .x1((frame, i) => { return xScale(itvlBand[i][1])})
                        .curve(d3.curveMonotoneY)
                        )

            sessWR = [];
            for (let i = 0; i < rows.length; i++) {
                sessWR.push(parseFloat(rows[i]['Session ID']['Lifetime winrate (W/L x(Base))']));
            }
            confItvl = generateCI(twoTailZVal, lifeWR);
            itvlBand = [];
            let meanAll = [];
            let mean = [sessWR[0]]
            for (let i = 1; i < sessWR.length; i++) {
                let datsum = 0;
                for (let j = 0; j <= i; j++) {
                    datsum += sessWR[j];
                }
                if (i >= start && i < start + frameSize) {
                    meanAll.push(datsum/(i+1));
                }
                mean.push(datsum/(i+1));
            }

            for (let i = start; i < start + frameSize; i++) {
                itvlBand.push([parseFloat(mean[i])-parseFloat(confItvl[i]), parseFloat(mean[i])+parseFloat(confItvl[i])]);
            }

            vizarea.append('path')
                    .datum(frame)
                    .attr('fill', '#ffcccb')
                    .attr('stroke', 'none')
                    .attr('d', d3.area()
                        .y((frame, i) => {return (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top)})
                        .x0((frame, i) => { return xScale(itvlBand[i][0])})
                        .x1((frame, i) => { return xScale(itvlBand[i][1])})
                        .curve(d3.curveMonotoneY)
                        )

            // Make the axes
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

            // Make the mean lines
            vizarea.append('path')
                    .datum(frame)
                    .classed('line', true)
                    .attr('fill', 'none')
                    .attr('stroke', 'tomato')
                    .attr('stroke-width', 1.25)
                    .attr('d', d3.line()
                                    .x((frame, i) => {return xScale(meanAll[i])})
                                    .y((frame, i) => {return (height-margin.top) - (i*(yMargin.bandwidth()) + yScale.bandwidth()/2 + margin.top)})
                                    .curve(d3.curveMonotoneY)
                        );

            vizarea.append('path')
                        .datum(frame)
                        .classed('line', true)
                        .attr('fill', 'none')
                        .attr('stroke', 'steelblue')
                        .attr('stroke-width', 1.25)
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
