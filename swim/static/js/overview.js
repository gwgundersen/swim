window.SWIM = {};

window.SWIM.visualize = function (series, days) {
    Highcharts.chart('visualization', {
        chart: {
            type: 'area'
        },
        title: {
            text: 'Activity per day'
        },
        xAxis: {
            categories: days,
            tickmarkPlacement: 'on',
            title: {
                enabled: false
            }
        },
        yAxis: {
            title: {
                text: 'Hours'
            }
        },
        tooltip: {
            split: true,
            valueSuffix: ' millions'
        },
        plotOptions: {
            area: {
                stacking: 'normal',
                lineColor: '#666666',
                lineWidth: 1,
                marker: {
                    lineWidth: 1,
                    lineColor: '#666666'
                }
            }
        },
        series: series
    });
};